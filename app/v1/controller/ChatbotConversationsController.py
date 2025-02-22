from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.v1.repository.ChatbotConversationsRepository import ChatbotConversationsRepository
from app.v1.repository.UsersRepository import UsersRepository
from app.v1.repository.AttendanceRepository import AttendanceRepository
from app.v1.repository.ActivitiesRepository import ActivitiesRepository
from app.v1.repository.BehaviorRecordsRepository import BehaviorRecordsRepository
from app.v1.repository.AcademicRecordsRepository import AcademicRecordsRepository
from app.config.postgres_orm_config import scoped_session_factory
from app.config.logger_config import LogConfig
from app.constants.intent_classification import INTENT_CLASSIFICATION_PROMPT
from app.constants.llm_prompts import FINAL_ANSWER_PROMPT
import requests
import uuid
import os

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

chatbot_conversations_bp = Blueprint('chatbot_conversations', __name__)
chatbot_conversations_repository = ChatbotConversationsRepository(scoped_session_factory)
users_repository = UsersRepository(scoped_session_factory)
attendance_repository = AttendanceRepository(scoped_session_factory)
activities_repository = ActivitiesRepository(scoped_session_factory)
behavior_records_repository = BehaviorRecordsRepository(scoped_session_factory)
academic_records_repository = AcademicRecordsRepository(scoped_session_factory)

class ChatbotConversationsController:
    @staticmethod
    @chatbot_conversations_bp.route('/api/chatbot/conversation', methods=['POST'])
    @jwt_required()
    def create_conversation():
        """Create a new chatbot conversation."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user:
                return jsonify({'error': 'Unauthorized access'}), 403

            query = data.get('query')
            if not query:
                return jsonify({'error': 'Query is required'}), 400

            conversation_id = data.get('conversation_id')

            if conversation_id:
                previous_messages = chatbot_conversations_repository.get_last_n_conversations(user_id, conversation_id, 5)
                messages = [{'role': 'user', 'content': query}]
                for message in previous_messages:
                    messages.insert(0, {'role': 'assistant', 'content': message.response})
                    messages.insert(0, {'role': 'user', 'content': message.query})
            else:
                messages = [{'role': 'user', 'content': query}]
                conversation_id = uuid.uuid4()
            
            
            logger.info(f"Starting new conversation with ID: {conversation_id} for user ID: {user_id}")
            print("==========================================")

            # Call the external chatbot API for intent classification
            intent_classification_prompt = INTENT_CLASSIFICATION_PROMPT.format(query=query)
            
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {os.getenv("GROQ_API_KEY")}'
                },
                json={
                    'model': 'llama-3.3-70b-versatile',
                    'messages': [{'role': 'user', 'content': intent_classification_prompt}]
                }
            )
            
            print(response.json())
            if response.status_code != 200:
                logger.error(f"Error calling chatbot API for intent classification: {response.text}")
                return jsonify({'error': 'An error occurred while calling the chatbot API for intent classification'}), 500

            response_data = response.json()
            intent_response = response_data['choices'][0]['message']['content']
            try:
                intent = eval(intent_response).get('intent')
                if not intent:
                    raise ValueError("Intent not found in response")
            except (SyntaxError, ValueError) as e:
                logger.error(f"Error parsing intent response: {e}")
                return jsonify({'error': 'An error occurred while parsing the intent response'}), 500
            print("==========================================")
            logger.info(f"Identified intent: {intent}")
            print("==========================================")

            # Fetch the corresponding data based on the intent
            student_id = user.student_id
            if intent == 'attendance':
                attendance_records = attendance_repository.get_attendance_by_student_id(student_id)
                data_response = [{'date': record.attendance_date, 'status': record.status, 'notes': record.notes} for record in attendance_records]
            elif intent == 'activity':
                activities = activities_repository.get_activities_by_student_id(student_id)
                data_response = [{'activity_name': activity.activity_name, 'badge': activity.badge, 'description': activity.description} for activity in activities]
            elif intent == 'behaviour':
                behavior_records = behavior_records_repository.get_records_by_student_id(student_id)
                data_response = [{'behavior_type': record.behaviour_type, 'sentiment_score': record.sentiment_score, 'comment': record.comment, 'date': record.record_date} for record in behavior_records]
            elif intent == 'grade':
                grades = academic_records_repository.get_records_by_student_id(student_id)
                data_response = [{'subject': grade.subject, 'grade': grade.grade, 'date': grade.record_date} for grade in grades]
            elif intent == 'general_question':
                # Directly call the external chatbot API for the final response
                response = requests.post(
                    'https://api.groq.com/openai/v1/chat/completions',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {os.getenv("GROQ_API_KEY")}'
                    },
                    json={
                        'model': 'llama-3.3-70b-versatile',
                        'messages': messages
                    }
                )

                if response.status_code != 200:
                    logger.error(f"Error calling chatbot API for final response: {response.text}")
                    return jsonify({'error': 'An error occurred while calling the chatbot API for final response'}), 500

                response_data = response.json()
                chatbot_response = response_data['choices'][0]['message']['content']

                conversation_data = {
                    'user_id': user_id,
                    'chat_id': uuid.uuid4(),
                    'conversation_id': conversation_id,
                    'query': query,
                    'response': chatbot_response,
                    'emotion': data.get('emotion')
                }

                conversation = chatbot_conversations_repository.create_conversation(conversation_data)
                logger.info(f"Conversation with ID: {conversation_id} created successfully.")
                return jsonify({'conversation_id': conversation.conversation_id, 'response': chatbot_response}), 201
            else:
                data_response = "I'm here to help with your questions. How can I assist you today?"

            # Call the external chatbot API for the final response
            final_answer_prompt = FINAL_ANSWER_PROMPT.format(query=query, data_response=data_response)
            if len(messages) > 1:
                messages.append({'role': 'assistant', 'content': final_answer_prompt})
            else:
                messages = [{'role': 'user', 'content': query}, {'role': 'assistant', 'content': final_answer_prompt}]
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {os.getenv("GROQ_API_KEY")}'
                },
                json={
                    'model': 'llama-3.3-70b-versatile',
                    'messages': messages
                }
            )

            if response.status_code != 200:
                logger.error(f"Error calling chatbot API for final response: {response.text}")
                return jsonify({'error': 'An error occurred while calling the chatbot API for final response'}), 500

            response_data = response.json()
            chatbot_response = response_data['choices'][0]['message']['content']

            conversation_data = {
                'user_id': user_id,
                'chat_id': uuid.uuid4(),
                'conversation_id': conversation_id,
                'query': query,
                'response': chatbot_response,
                'emotion': data.get('emotion')
            }

            conversation = chatbot_conversations_repository.create_conversation(conversation_data)
            logger.info(f"Conversation with ID: {conversation_id} created successfully.")
            return jsonify({'conversation_id': conversation.conversation_id, 'response': chatbot_response}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error creating conversation: {e}")
            return jsonify({'error': 'An error occurred while creating the conversation'}), 500

    @staticmethod
    @chatbot_conversations_bp.route('/api/chatbot/conversation/<uuid:conversation_id>', methods=['GET'])
    @jwt_required()
    def get_conversation(conversation_id):
        """Retrieve a chatbot conversation by its ID."""
        try:
            conversation = chatbot_conversations_repository.get_conversation_by_id(conversation_id)
            if conversation:
                return jsonify({
                    'conversation_id': conversation.conversation_id,
                    'user_id': conversation.user_id,
                    'chat_id': conversation.chat_id,
                    'query': conversation.query,
                    'response': conversation.response,
                    'emotion': conversation.emotion,
                    'created_at': conversation.created_at
                }), 200
            return jsonify({'error': 'Conversation not found'}), 404
        except Exception as e:
            logger.error(f"Error retrieving conversation: {e}")
            return jsonify({'error': 'An error occurred while retrieving the conversation'}), 500

    @staticmethod
    @chatbot_conversations_bp.route('/api/chatbot/conversations', methods=['GET'])
    @jwt_required()
    def get_conversations_by_user():
        """Retrieve chatbot conversations by user ID."""
        try:
            user_id = get_jwt_identity()
            conversations = chatbot_conversations_repository.get_conversations_by_user_id(user_id)
            response = [{
                'conversation_id': conversation.conversation_id,
                'user_id': conversation.user_id,
                'chat_id': conversation.chat_id,
                'query': conversation.query,
                'response': conversation.response,
                'emotion': conversation.emotion,
                'created_at': conversation.created_at
            } for conversation in conversations]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving conversations: {e}")
            return jsonify({'error': 'An error occurred while retrieving conversations'}), 500

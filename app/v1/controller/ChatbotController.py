from flask import Blueprint, request, jsonify
from app.config.logger_config import LogConfig
from app.v1.service.ChatbotService import ChatbotService
from app.v1.service.LLMService import LLMService

chatbot_bp = Blueprint('chatbot', __name__)
logger = LogConfig.setup_logger(__name__)

# Initialize services
llm_service = LLMService()
chatbot_service = ChatbotService(llm_service)

@chatbot_bp.route('/api/chatbot/query', methods=['POST'])
def handle_text_query():
    """
    Handle text-based queries to the chatbot
    """
    try:
        data = request.get_json()
        query = data.get('query')
        child_id = data.get('child_id')
        
        if not query or not child_id:
            return jsonify({
                'error': 'Missing required fields'
            }), 400
            
        response = chatbot_service.process_query(query, child_id)
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing chatbot query: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@chatbot_bp.route('/api/chatbot/voice-query', methods=['POST'])
def handle_voice_query():
    """
    Handle voice-based queries to the chatbot
    """
    try:
        data = request.get_json()
        audio_data = data.get('audio_data')
        child_id = data.get('child_id')
        
        if not audio_data or not child_id:
            return jsonify({
                'error': 'Missing required fields'
            }), 400
            
        response = chatbot_service.process_voice_query(audio_data, child_id)
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing voice query: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@chatbot_bp.route('/api/chatbot/history', methods=['GET'])
def get_chat_history():
    """
    Retrieve chat history for a user
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                'error': 'Missing user_id parameter'
            }), 400
            
        history = chatbot_service.get_history(user_id)
        
        return jsonify({
            'history': history
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        return jsonify({
            'error': 'Internal server error'
        }), 500
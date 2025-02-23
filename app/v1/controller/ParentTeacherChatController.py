from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.v1.repository.ParentTeacherChatRepository import ParentTeacherChatRepository
from app.v1.repository.UsersRepository import UsersRepository
from app.config.postgres_orm_config import scoped_session_factory
from app.config.logger_config import LogConfig

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

parent_teacher_chat_bp = Blueprint('parent_teacher_chat', __name__)
parent_teacher_chat_repository = ParentTeacherChatRepository(scoped_session_factory)
users_repository = UsersRepository(scoped_session_factory)

class ParentTeacherChatController:
    @staticmethod
    @parent_teacher_chat_bp.route('/api/chat', methods=['POST'])
    @jwt_required()
    def create_chat():
        """Create a new chat message."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role not in ['parent', 'teacher']:
                return jsonify({'error': 'Unauthorized access'}), 403

            if user.role == 'parent':
                parent_id = user.id
                teacher_id = data['teacher_id']
            else:
                parent_id = data['parent_id']
                teacher_id = user.id

            chat_data = {
                'teacher_id': teacher_id,
                'parent_id': parent_id,
                'sender': user.role,
                'message': data['message']
            }

            chat = parent_teacher_chat_repository.create_chat(chat_data)
            return jsonify({'chat_id': chat.chat_id, 'message': 'Chat message created successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error creating chat message: {e}")
            return jsonify({'error': 'An error occurred while creating the chat message'}), 500

    @staticmethod
    @parent_teacher_chat_bp.route('/api/chat/<int:chat_id>', methods=['GET'])
    @jwt_required()
    def get_chat(chat_id):
        """Retrieve a chat message by its ID."""
        try:
            chat = parent_teacher_chat_repository.get_chat_by_id(chat_id)
            if chat:
                return jsonify({
                    'chat_id': chat.chat_id,
                    'teacher_id': chat.teacher_id,
                    'parent_id': chat.parent_id,
                    'sender': chat.sender,
                    'message': chat.message,
                    'is_read': chat.is_read,
                    'created_at': chat.created_at
                }), 200
            return jsonify({'error': 'Chat message not found'}), 404
        except Exception as e:
            logger.error(f"Error retrieving chat message: {e}")
            return jsonify({'error': 'An error occurred while retrieving the chat message'}), 500

    @staticmethod
    @parent_teacher_chat_bp.route('/api/chat/teacher/<int:teacher_id>', methods=['GET'])
    @jwt_required()
    def get_chats_by_teacher(teacher_id):
        """Retrieve chat messages by teacher ID."""
        try:
            chats = parent_teacher_chat_repository.get_chats_by_teacher_id(teacher_id)
            response = [{
                'chat_id': chat.chat_id,
                'teacher_id': chat.teacher_id,
                'parent_id': chat.parent_id,
                'sender': chat.sender,
                'message': chat.message,
                'is_read': chat.is_read,
                'created_at': chat.created_at
            } for chat in chats]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving chat messages: {e}")
            return jsonify({'error': 'An error occurred while retrieving chat messages'}), 500

    @staticmethod
    @parent_teacher_chat_bp.route('/api/chat/parent/<int:parent_id>', methods=['GET'])
    @jwt_required()
    def get_chats_by_parent(parent_id):
        """Retrieve chat messages by parent ID."""
        try:
            chats = parent_teacher_chat_repository.get_chats_by_parent_id(parent_id)
            response = [{
                'chat_id': chat.chat_id,
                'teacher_id': chat.teacher_id,
                'parent_id': chat.parent_id,
                'sender': chat.sender,
                'message': chat.message,
                'is_read': chat.is_read,
                'created_at': chat.created_at
            } for chat in chats]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving chat messages: {e}")
            return jsonify({'error': 'An error occurred while retrieving chat messages'}), 500

    @staticmethod
    @parent_teacher_chat_bp.route('/api/chat/teacher/<int:teacher_id>/parent/<int:parent_id>', methods=['GET'])
    @jwt_required()
    def get_chats_by_teacher_and_parent(teacher_id, parent_id):
        """Retrieve chat messages by both teacher ID and parent ID."""
        try:
            chats = parent_teacher_chat_repository.get_chats_by_teacher_id_parent_id(teacher_id, parent_id)
            response = [{
                'chat_id': chat.chat_id,
                'teacher_id': chat.teacher_id,
                'parent_id': chat.parent_id,
                'sender': chat.sender,
                'message': chat.message,
                'is_read': chat.is_read,
                'created_at': chat.created_at
            } for chat in chats]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving chat messages: {e}")
            return jsonify({'error': 'An error occurred while retrieving chat messages'}), 500

    @staticmethod
    @parent_teacher_chat_bp.route('/api/chat/<int:chat_id>', methods=['PUT'])
    @jwt_required()
    def update_chat(chat_id):
        """Update an existing chat message."""
        data = request.json
        try:
            chat_data = {
                'message': data.get('message'),
                'is_read': data.get('is_read')
            }
            chat = parent_teacher_chat_repository.update_chat(chat_id, chat_data)
            if chat:
                return jsonify({'chat_id': chat.chat_id, 'message': 'Chat message updated successfully.'}), 200
            return jsonify({'error': 'Chat message not found'}), 404
        except Exception as e:
            logger.error(f"Error updating chat message: {e}")
            return jsonify({'error': 'An error occurred while updating the chat message'}), 500

    @staticmethod
    @parent_teacher_chat_bp.route('/api/chat/<int:chat_id>', methods=['DELETE'])
    @jwt_required()
    def delete_chat(chat_id):
        """Delete a chat message by its ID."""
        try:
            success = parent_teacher_chat_repository.delete_chat(chat_id)
            if success:
                return jsonify({'message': 'Chat message deleted successfully.'}), 200
            return jsonify({'error': 'Chat message not found'}), 404
        except Exception as e:
            logger.error(f"Error deleting chat message: {e}")
            return jsonify({'error': 'An error occurred while deleting the chat message'}), 500

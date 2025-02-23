from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.v1.repository.AudioResourceRepository import AudioResourceRepository
from app.v1.repository.UsersRepository import UsersRepository
from app.v1.repository.StudentsRepository import StudentsRepository
from app.config.postgres_orm_config import scoped_session_factory
from app.config.logger_config import LogConfig
from datetime import datetime
import base64

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

audio_resource_bp = Blueprint('audio_resource', __name__)
audio_resource_repository = AudioResourceRepository(scoped_session_factory)
users_repository = UsersRepository(scoped_session_factory)
students_repository = StudentsRepository(scoped_session_factory)

class AudioResourceController:
    @staticmethod
    @audio_resource_bp.route('/api/audio_resources', methods=['POST'])
    @jwt_required()
    def create_audio_resource():
        """Create a new audio resource."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'teacher':
                return jsonify({'error': 'Unauthorized access'}), 403

            audio_data = base64.b64decode(data['audio_data'])

            resource_data = {
                'title': data['title'],
                'description': data.get('description'),
                'audio_data': audio_data,
                'teacher_id': user_id,
                'class_value': data['class_value'],
                'section': data['section']
            }

            resource = audio_resource_repository.create_audio_resource(resource_data)
            return jsonify({'resource_id': resource.id, 'message': 'Audio resource created successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error creating audio resource: {e}")
            return jsonify({'error': 'An error occurred while creating the audio resource'}), 500

    @staticmethod
    @audio_resource_bp.route('/api/audio_resources', methods=['GET'])
    @jwt_required()
    def get_audio_resources():
        """Retrieve audio resources filtered by class value and section."""
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user:
                return jsonify({'error': 'Unauthorized access'}), 403

            if user.role == 'teacher':
                class_value = request.args.get('class_value')
                section = request.args.get('section')
                if not class_value or not section:
                    return jsonify({'error': 'class_value and section are required'}), 400
            elif user.role == 'parent':
                student_id = user.student_id
                student = students_repository.get_student_by_id(student_id)
                if not student:
                    return jsonify({'error': 'Student not found'}), 404
                class_value = student.class_value
                section = student.section
            else:
                return jsonify({'error': 'Unauthorized access'}), 403

            resources = audio_resource_repository.get_audio_resources_by_class_and_section(class_value, section)
            response = [{
                'id': resource.id,
                'title': resource.title,
                'description': resource.description,
                'audio_data': base64.b64encode(resource.audio_data).decode('utf-8'),
                'teacher_id': resource.teacher_id,
                'class_value': resource.class_value,
                'section': resource.section,
                'created_at': resource.created_at,
                'updated_at': resource.updated_at
            } for resource in resources]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving audio resources: {e}")
            return jsonify({'error': 'An error occurred while retrieving audio resources'}), 500

    @staticmethod
    @audio_resource_bp.route('/api/audio_resources/<int:resource_id>', methods=['DELETE'])
    @jwt_required()
    def delete_audio_resource(resource_id):
        """Delete an audio resource."""
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'teacher':
                return jsonify({'error': 'Unauthorized access'}), 403

            resource = audio_resource_repository.get_audio_resource_by_id(resource_id)
            if not resource:
                return jsonify({'error': 'Audio resource not found'}), 404

            if resource.teacher_id != int(user_id):
                return jsonify({'error': 'Unauthorized access'}), 403

            audio_resource_repository.delete_audio_resource(resource_id)
            return jsonify({'message': 'Audio resource deleted successfully.'}), 200
        except Exception as e:
            logger.error(f"Error deleting audio resource: {e}")
            return jsonify({'error': 'An error occurred while deleting the audio resource'}), 500

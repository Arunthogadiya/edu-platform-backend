from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.v1.repository.UsersRepository import UsersRepository
from app.v1.repository.BehaviorRecordsRepository import BehaviorRecordsRepository
from app.config.postgres_orm_config import scoped_session_factory
from app.config.logger_config import LogConfig
from datetime import datetime

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

social_emotional_tracker_bp = Blueprint('social_emotional_tracker', __name__)
users_repository = UsersRepository(scoped_session_factory)
behavior_records_repository = BehaviorRecordsRepository(scoped_session_factory)

class SocialEmotionalDevelopmentTrackerController:
    @staticmethod
    @social_emotional_tracker_bp.route('/api/behavior/school', methods=['POST'])
    @jwt_required()
    def log_behavior_school():
        """Log a behavioral milestone from the teacher side."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'teacher':
                return jsonify({'error': 'Unauthorized access'}), 403

            record_data = {
                'student_id': data['student_id'],
                'logged_by': user_id,
                'source': 'school',
                'behaviour_type': data.get('behavior_type', 'General'),
                'sentiment_score': data['sentiment_score'],
                'comment': data['comment'],
                'record_date': datetime.strptime(data['record_date'], '%Y-%m-%d').date()
            }

            record = behavior_records_repository.create_record(record_data)
            return jsonify({'record_id': record.id, 'message': 'Behavior record logged.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error logging behavior record: {e}")
            return jsonify({'error': 'An error occurred while logging the behavior record'}), 500

    @staticmethod
    @social_emotional_tracker_bp.route('/api/behavior/teacher/<int:student_id>', methods=['GET'])
    @jwt_required()
    def get_behavior_teacher(student_id):
        """Retrieve teacher-logged behavior records."""
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'teacher':
                return jsonify({'error': 'Unauthorized access'}), 403

            behavior_records = behavior_records_repository.get_records_by_student_id(student_id)
            response = {
                'student_id': student_id,
                'behavior_records': [{'behavior_type': record.behaviour_type, 'sentiment_score': record.sentiment_score, 'comment': record.comment, 'date': record.record_date} for record in behavior_records]
            }

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving behavior records: {e}")
            return jsonify({'error': 'An error occurred while retrieving behavior records'}), 500

    @staticmethod
    @social_emotional_tracker_bp.route('/api/behavior/home', methods=['POST'])
    @jwt_required()
    def log_behavior_home():
        """Log a behavioral observation from the parent side."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'parent':
                return jsonify({'error': 'Unauthorized access'}), 403

            record_data = {
                'student_id': user.student_id,
                'logged_by': user_id,
                'source': 'home',
                'behaviour_type': 'Observation',
                'sentiment_score': None,
                'comment': data['observation_text'],
                'record_date': datetime.now().date()
            }

            record = behavior_records_repository.create_record(record_data)
            return jsonify({'record_id': record.id, 'message': 'Observation recorded successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error logging observation: {e}")
            return jsonify({'error': 'An error occurred while logging the observation'}), 500

    @staticmethod
    @social_emotional_tracker_bp.route('/api/behavior/analysis', methods=['GET'])
    @jwt_required()
    def get_behavior_analysis():
        """Retrieve AI-powered behavioral analysis."""
        user_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'parent':
                return jsonify({'error': 'Unauthorized access'}), 403

            student_id = user.student_id
            if not student_id:
                return jsonify({'error': 'Student ID not found for parent'}), 404

            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            # Placeholder for AI-powered analysis logic
            analysis = {
                'trend_graph': 'URL_TO_GRAPH_IMAGE',
                'flags': ['Prolonged low collaboration'],
                'suggestions': ['Engage in group board games']
            }

            response = {
                'student_id': student_id,
                'analysis': analysis
            }

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving behavior analysis: {e}")
            return jsonify({'error': 'An error occurred while retrieving behavior analysis'}), 500

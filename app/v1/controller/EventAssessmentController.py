from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.v1.repository.EventRepository import EventRepository
from app.v1.repository.AssessmentRepository import AssessmentRepository
from app.v1.repository.UsersRepository import UsersRepository
from app.v1.repository.StudentsRepository import StudentsRepository
from app.config.postgres_orm_config import scoped_session_factory
from app.config.logger_config import LogConfig
from datetime import datetime

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

event_assessment_bp = Blueprint('event_assessment', __name__)
event_repository = EventRepository(scoped_session_factory)
assessment_repository = AssessmentRepository(scoped_session_factory)
users_repository = UsersRepository(scoped_session_factory)
students_repository = StudentsRepository(scoped_session_factory)

class EventAssessmentController:
    @staticmethod
    @event_assessment_bp.route('/api/events', methods=['POST'])
    @jwt_required()
    def create_event():
        """Create a new event."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'teacher':
                return jsonify({'error': 'Unauthorized access'}), 403

            event_data = {
                'title': data['title'],
                'description': data.get('description'),
                'event_date': datetime.strptime(data['event_date'], '%Y-%m-%dT%H:%M:%S'),
                'teacher_id': user_id,
                'class_value': data['class_value'],
                'section': data['section']
            }

            event = event_repository.create_event(event_data)
            return jsonify({'event_id': event.id, 'message': 'Event created successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error creating event: {e}")
            return jsonify({'error': 'An error occurred while creating the event'}), 500

    @staticmethod
    @event_assessment_bp.route('/api/assessments', methods=['POST'])
    @jwt_required()
    def create_assessment():
        """Create a new assessment."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'teacher':
                return jsonify({'error': 'Unauthorized access'}), 403

            assessment_data = {
                'title': data['title'],
                'description': data.get('description'),
                'assessment_date': datetime.strptime(data['assessment_date'], '%Y-%m-%dT%H:%M:%S'),
                'teacher_id': user_id,
                'class_value': data['class_value'],
                'section': data['section']
            }

            assessment = assessment_repository.create_assessment(assessment_data)
            return jsonify({'assessment_id': assessment.id, 'message': 'Assessment created successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error creating assessment: {e}")
            return jsonify({'error': 'An error occurred while creating the assessment'}), 500

    @staticmethod
    @event_assessment_bp.route('/api/events/upcoming', methods=['GET'])
    @jwt_required()
    def get_upcoming_events():
        """Retrieve upcoming events."""
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

            events = event_repository.get_upcoming_events(class_value, section)
            response = [{
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'event_date': event.event_date
            } for event in events]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving upcoming events: {e}")
            return jsonify({'error': 'An error occurred while retrieving upcoming events'}), 500

    @staticmethod
    @event_assessment_bp.route('/api/assessments/upcoming', methods=['GET'])
    @jwt_required()
    def get_upcoming_assessments():
        """Retrieve upcoming assessments."""
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

            assessments = assessment_repository.get_upcoming_assessments(class_value, section)
            response = [{
                'id': assessment.id,
                'title': assessment.title,
                'description': assessment.description,
                'assessment_date': assessment.assessment_date
            } for assessment in assessments]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving upcoming assessments: {e}")
            return jsonify({'error': 'An error occurred while retrieving upcoming assessments'}), 500

    @staticmethod
    @event_assessment_bp.route('/api/events/previous', methods=['GET'])
    @jwt_required()
    def get_previous_events():
        """Retrieve previous events."""
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

            events = event_repository.get_previous_events(class_value, section)
            response = [{
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'event_date': event.event_date
            } for event in events]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving previous events: {e}")
            return jsonify({'error': 'An error occurred while retrieving previous events'}), 500

    @staticmethod
    @event_assessment_bp.route('/api/assessments/previous', methods=['GET'])
    @jwt_required()
    def get_previous_assessments():
        """Retrieve previous assessments."""
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

            assessments = assessment_repository.get_previous_assessments(class_value, section)
            response = [{
                'id': assessment.id,
                'title': assessment.title,
                'description': assessment.description,
                'assessment_date': assessment.assessment_date
            } for assessment in assessments]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving previous assessments: {e}")
            return jsonify({'error': 'An error occurred while retrieving previous assessments'}), 500

    @staticmethod
    @event_assessment_bp.route('/api/reminders', methods=['GET'])
    @jwt_required()
    def get_event_assessment_reminders():
        """Retrieve reminders for upcoming events and assessments."""
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

            events = event_repository.get_upcoming_events(class_value, section)
            assessments = assessment_repository.get_upcoming_assessments(class_value, section)
            response = {
                'events': [{
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'event_date': event.event_date
                } for event in events],
                'assessments': [{
                    'id': assessment.id,
                    'title': assessment.title,
                    'description': assessment.description,
                    'assessment_date': assessment.assessment_date
                } for assessment in assessments]
            }
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving reminders: {e}")
            return jsonify({'error': 'An error occurred while retrieving reminders'}), 500

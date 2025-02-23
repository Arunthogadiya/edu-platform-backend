from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.v1.repository.StudentsRepository import StudentsRepository
from app.v1.repository.UsersRepository import UsersRepository
from app.config.postgres_orm_config import scoped_session_factory
from app.config.logger_config import LogConfig

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

students_bp = Blueprint('students', __name__)
students_repository = StudentsRepository(scoped_session_factory)
users_repository = UsersRepository(scoped_session_factory)

class StudentsController:
    @staticmethod
    @students_bp.route('/api/students', methods=['GET'])
    @jwt_required()
    def get_students_by_class_and_section():
        """Retrieve students by class value and section."""
        user_id = get_jwt_identity()
        user = users_repository.get_user_by_id(user_id)
        if not user or user.role != 'teacher':
            return jsonify({'error': 'Unauthorized access'}), 403

        class_value = request.args.get('class_value')
        section = request.args.get('section')
        try:
            if not class_value or not section:
                return jsonify({'error': 'class_value and section are required'}), 400

            students = students_repository.get_students_by_class_and_section(class_value, section)
            response = [{
                'student_id': student.student_id,
                'student_name': student.student_name,
                'parent_name': student.parent_name,
                'parent_phone': student.parent_phone,
                'class_value': student.class_value,
                'section': student.section,
                'date_of_birth': student.date_of_birth,
                'gender': student.gender
            } for student in students]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving students: {e}")
            return jsonify({'error': 'An error occurred while retrieving students'}), 500

    @staticmethod
    @students_bp.route('/api/students', methods=['POST'])
    @jwt_required()
    def add_student():
        """Add a new student with all details."""
        user_id = get_jwt_identity()
        user = users_repository.get_user_by_id(user_id)
        if not user or user.role != 'teacher':
            return jsonify({'error': 'Unauthorized access'}), 403

        data = request.json
        try:
            student_data = {
                'student_id': data['student_id'],
                'student_name': data['student_name'],
                'parent_name': data['parent_name'],
                'parent_phone': data['parent_phone'],
                'class_value': data['class_value'],
                'section': data['section'],
                'date_of_birth': data['date_of_birth'],
                'gender': data['gender']
            }

            student = students_repository.create_student(student_data)
            return jsonify({'message': 'Student created successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except ValueError as e:
            logger.error(f"Invalid value: {e}")
            return jsonify({'error': f"Invalid value: {e}"}), 400
        except Exception as e:
            logger.error(f"Error creating student: {e}")
            return jsonify({'error': 'An error occurred while creating the student'}), 500

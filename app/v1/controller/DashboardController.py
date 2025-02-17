from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.v1.repository.UsersRepository import UsersRepository
from app.v1.repository.AcademicRecordsRepository import AcademicRecordsRepository
from app.v1.repository.AttendanceRepository import AttendanceRepository
from app.v1.repository.ActivitiesRepository import ActivitiesRepository
from app.v1.repository.BehaviorRecordsRepository import BehaviorRecordsRepository
from app.v1.repository.StudentsRepository import StudentsRepository
from app.config.postgres_orm_config import scoped_session_factory
from app.config.logger_config import LogConfig
from datetime import datetime

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

dashboard_bp = Blueprint('dashboard', __name__)
users_repository = UsersRepository(scoped_session_factory)
academic_records_repository = AcademicRecordsRepository(scoped_session_factory)
attendance_repository = AttendanceRepository(scoped_session_factory)
activities_repository = ActivitiesRepository(scoped_session_factory)
behavior_records_repository = BehaviorRecordsRepository(scoped_session_factory)
students_repository = StudentsRepository(scoped_session_factory)

class DashboardController:
    @staticmethod
    @dashboard_bp.route('/api/dashboard/grades', methods=['GET'])
    @jwt_required()
    def get_grades():
        """Retrieve academic grade trends."""
        user_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role not in ['parent', 'teacher']:
                return jsonify({'error': 'Unauthorized access'}), 403

            if user.role == 'parent':
                student_id = user.student_id
                if not student_id:
                    return jsonify({'error': 'Student ID not found'}), 404
                student_ids = [student_id]
            else:
                class_value = request.args.get('class_value')
                section = request.args.get('section')
                if not class_value or not section:
                    return jsonify({'error': 'class_value and section are required for teachers'}), 400
                student_ids = [student.student_id for student in students_repository.get_students_by_class_and_section(class_value, section)]

            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            response = {'students': []}
            for student_id in student_ids:
                student = students_repository.get_student_by_id(student_id)
                grades = academic_records_repository.get_records_by_student_id(student_id)
                student_data = {
                    'student_id': student_id,
                    'student_name': student.student_name,
                    'gender': student.gender,
                    'subjects': []
                }

                subjects = {}
                for grade in grades:
                    if start_date and grade.record_date < datetime.strptime(start_date, '%Y-%m-%d').date():
                        continue
                    if end_date and grade.record_date > datetime.strptime(end_date, '%Y-%m-%d').date():
                        continue
                    if grade.subject not in subjects:
                        subjects[grade.subject] = {'subject': grade.subject, 'grades': [], 'alert': False}
                    subjects[grade.subject]['grades'].append({'date': grade.record_date, 'grade': grade.grade})
                    if grade.grade in ['D', 'F']:
                        subjects[grade.subject]['alert'] = True

                student_data['subjects'] = list(subjects.values())
                response['students'].append(student_data)

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving grades: {e}")
            return jsonify({'error': 'An error occurred while retrieving grades'}), 500

    @staticmethod
    @dashboard_bp.route('/api/dashboard/grades', methods=['POST'])
    @jwt_required()
    def post_grades():
        """Post academic grade details."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'teacher':
                return jsonify({'error': 'Unauthorized access'}), 403

            record_data = {
                'student_id': data['student_id'],
                'subject': data['subject'],
                'grade': data['grade'],
                'record_date': datetime.strptime(data['record_date'], '%Y-%m-%d').date(),
                'teacher_id': user_id
            }

            record = academic_records_repository.create_record(record_data)
            return jsonify({'record_id': record.id, 'message': 'Grade record posted successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error posting grade record: {e}")
            return jsonify({'error': 'An error occurred while posting the grade record'}), 500

    @staticmethod
    @dashboard_bp.route('/api/dashboard/attendance', methods=['GET'])
    @jwt_required()
    def get_attendance():
        """Retrieve attendance data formatted for heatmaps."""
        user_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role not in ['parent', 'teacher']:
                return jsonify({'error': 'Unauthorized access'}), 403

            if user.role == 'parent':
                student_id = user.student_id
                if not student_id:
                    return jsonify({'error': 'Student ID not found'}), 404
                student_ids = [student_id]
            else:
                class_value = request.args.get('class_value')
                section = request.args.get('section')
                if not class_value or not section:
                    return jsonify({'error': 'class_value and section are required for teachers'}), 400
                student_ids = [student.student_id for student in students_repository.get_students_by_class_and_section(class_value, section)]

            month = request.args.get('month')
            year = request.args.get('year')

            response = {'students': []}
            for student_id in student_ids:
                student = students_repository.get_student_by_id(student_id)
                attendance_records = attendance_repository.get_attendance_by_student_id(student_id)
                student_data = {
                    'student_id': student_id,
                    'student_name': student.student_name,
                    'gender': student.gender,
                    'attendance': []
                }

                for record in attendance_records:
                    if month and record.attendance_date.month != int(month):
                        continue
                    if year and record.attendance_date.year != int(year):
                        continue
                    student_data['attendance'].append({'date': record.attendance_date, 'status': record.status})

                response['students'].append(student_data)

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving attendance: {e}")
            return jsonify({'error': 'An error occurred while retrieving attendance'}), 500

    @staticmethod
    @dashboard_bp.route('/api/dashboard/attendance', methods=['POST'])
    @jwt_required()
    def post_attendance():
        """Post attendance details."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'teacher':
                return jsonify({'error': 'Unauthorized access'}), 403

            record_data = {
                'student_id': data['student_id'],
                'attendance_date': datetime.strptime(data['attendance_date'], '%Y-%m-%d').date(),
                'status': data['status'],
                'notes': data.get('notes')
            }

            record = attendance_repository.create_attendance(record_data)
            return jsonify({'record_id': record.id, 'message': 'Attendance record posted successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error posting attendance record: {e}")
            return jsonify({'error': 'An error occurred while posting the attendance record'}), 500

    @staticmethod
    @dashboard_bp.route('/api/dashboard/activities', methods=['GET'])
    @jwt_required()
    def get_activities():
        """Get extracurricular participation and badges."""
        user_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role not in ['parent', 'teacher']:
                return jsonify({'error': 'Unauthorized access'}), 403

            if user.role == 'parent':
                student_id = user.student_id
                if not student_id:
                    return jsonify({'error': 'Student ID not found'}), 404
                student_ids = [student_id]
            else:
                class_value = request.args.get('class_value')
                section = request.args.get('section')
                if not class_value or not section:
                    return jsonify({'error': 'class_value and section are required for teachers'}), 400
                student_ids = [student.student_id for student in students_repository.get_students_by_class_and_section(class_value, section)]

            response = {'students': []}
            for student_id in student_ids:
                student = students_repository.get_student_by_id(student_id)
                activities = activities_repository.get_activities_by_student_id(student_id)
                student_data = {
                    'student_id': student_id,
                    'student_name': student.student_name,
                    'gender': student.gender,
                    'activities': [{'activity_name': activity.activity_name, 'badge': activity.badge, 'description': activity.description} for activity in activities]
                }

                response['students'].append(student_data)

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving activities: {e}")
            return jsonify({'error': 'An error occurred while retrieving activities'}), 500

    @staticmethod
    @dashboard_bp.route('/api/dashboard/activities', methods=['POST'])
    @jwt_required()
    def post_activities():
        """Post extracurricular activity details."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'teacher':
                return jsonify({'error': 'Unauthorized access'}), 403

            record_data = {
                'student_id': data['student_id'],
                'activity_name': data['activity_name'],
                'badge': data.get('badge'),
                'description': data.get('description')
            }

            record = activities_repository.create_activity(record_data)
            return jsonify({'record_id': record.id, 'message': 'Activity record posted successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error posting activity record: {e}")
            return jsonify({'error': 'An error occurred while posting the activity record'}), 500

    @staticmethod
    @dashboard_bp.route('/api/dashboard/behavior', methods=['GET'])
    @jwt_required()
    def get_behavior():
        """Return behavioral sentiment analysis data."""
        user_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role not in ['parent', 'teacher']:
                return jsonify({'error': 'Unauthorized access'}), 403

            if user.role == 'parent':
                student_id = user.student_id
                if not student_id:
                    return jsonify({'error': 'Student ID not found'}), 404
                student_ids = [student_id]
            else:
                class_value = request.args.get('class_value')
                section = request.args.get('section')
                if not class_value or not section:
                    return jsonify({'error': 'class_value and section are required for teachers'}), 400
                student_ids = [student.student_id for student in students_repository.get_students_by_class_and_section(class_value, section)]

            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            response = {'students': []}
            for student_id in student_ids:
                student = students_repository.get_student_by_id(student_id)
                behavior_records = behavior_records_repository.get_records_by_student_id(student_id)
                student_data = {
                    'student_id': student_id,
                    'student_name': student.student_name,
                    'gender': student.gender,
                    'behavior_records': []
                }

                for record in behavior_records:
                    if start_date and record.record_date < datetime.strptime(start_date, '%Y-%m-%d').date():
                        continue
                    if end_date and record.record_date > datetime.strptime(end_date, '%Y-%m-%d').date():
                        continue
                    student_data['behavior_records'].append({
                        'behavior_type': record.behaviour_type,
                        'sentiment_score': record.sentiment_score,
                        'comment': record.comment,
                        'date': record.record_date
                    })

                response['students'].append(student_data)

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving behavior records: {e}")
            return jsonify({'error': 'An error occurred while retrieving behavior records'}), 500

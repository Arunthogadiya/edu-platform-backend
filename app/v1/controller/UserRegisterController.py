from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.v1.repository.UsersRepository import UsersRepository
from app.v1.repository.StudentsRepository import StudentsRepository
from app.config.postgres_orm_config import scoped_session_factory
from app.config.logger_config import LogConfig
from app.config.auth import Auth
from datetime import timedelta
import bcrypt
import re

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

user_register_bp = Blueprint('user_register', __name__)
users_repository = UsersRepository(scoped_session_factory)
students_repository = StudentsRepository(scoped_session_factory)

class UserRegisterController:
    @staticmethod
    @user_register_bp.route('/register', methods=['POST'])
    def register():
        """Register a new user."""
        data = request.json
        try:
            # Validate email format
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, data['email']):
                return jsonify({'error': 'Invalid email format'}), 400

            # Check if email already exists
            existing_user = users_repository.get_user_by_email(data['email'])
            if (existing_user):
                return jsonify({'error': 'User with this email already exists'}), 400

            # Hash the password
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            data['password_hash'] = hashed_password.decode('utf-8')
            del data['password']

            user = users_repository.create_user(data)
            logger.info(f"User registered with email: {user.email}")
            return jsonify({'message': 'User registered successfully'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return jsonify({'error': 'An error occurred while registering the user'}), 500

    @staticmethod
    @user_register_bp.route('/login', methods=['POST'])
    def login():
        """Login a user and generate tokens."""
        data = request.json
        try:
            user = users_repository.get_user_by_email(data['email'])
            if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
                access_token = Auth.create_access_token(identity=str(user.id), expires_delta=timedelta(minutes=30))
                refresh_token = Auth.create_refresh_token(identity=str(user.id))
                logger.info(f"User logged in with email: {user.email}")
                return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
            logger.warning(f"Invalid login attempt for email: {data['email']}")
            return jsonify({'error': 'Invalid credentials'}), 401
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            return jsonify({'error': 'An error occurred while logging in the user'}), 500

    @staticmethod
    @user_register_bp.route('/user', methods=['GET'])
    @jwt_required()
    def get_user():
        """Get user details."""
        user_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(user_id)
            if user:
                logger.info(f"Fetched user details for user ID: {user_id}")
                return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role}), 200
            logger.warning(f"User not found for user ID: {user_id}")
            return jsonify({'error': 'User not found'}), 404
        except Exception as e:
            logger.error(f"Error fetching user details: {e}")
            return jsonify({'error': 'An error occurred while fetching user details'}), 500

    @staticmethod
    @user_register_bp.route('/token/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh_token():
        """Generate a new access token using the refresh token."""
        user_id = get_jwt_identity()
        try:
            access_token = Auth.create_access_token(identity=str(user_id), expires_delta=timedelta(minutes=30))
            logger.info(f"Access token refreshed for user ID: {user_id}")
            return jsonify({'access_token': access_token}), 200
        except Exception as e:
            logger.error(f"Error refreshing access token: {e}")
            return jsonify({'error': 'An error occurred while refreshing the access token'}), 500

    @staticmethod
    @user_register_bp.route('/teachers', methods=['GET'])
    @jwt_required()
    def get_teachers():
        """Get all teachers' details."""
        try:
            teachers = users_repository.get_users_by_role('teacher')
            response = [{'id': teacher.id, 'name': teacher.name, 'email': teacher.email, 'role': teacher.role, 'subject': teacher.subject} for teacher in teachers]
            logger.info("Fetched all teachers' details")
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error fetching teachers' details: {e}")
            return jsonify({'error': 'An error occurred while fetching teachers\' details'}), 500

    @staticmethod
    @user_register_bp.route('/parents', methods=['GET'])
    @jwt_required()
    def get_parents():
        """Get all parents and their child details."""
        try:
            parents = users_repository.get_users_by_role('parent')
            response = []
            for parent in parents:
                student = students_repository.get_student_by_id(parent.student_id)
                if student:
                    response.append({
                        'parent_id': parent.id,
                        'parent_name': parent.name,
                        'parent_email': parent.email,
                        'student_id': student.student_id,
                        'student_name': student.student_name,
                        'student_gender': student.gender
                    })
            logger.info("Fetched all parents' details")
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error fetching parents' details: {e}")
            return jsonify({'error': 'An error occurred while fetching parents\' details'}), 500

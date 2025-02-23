from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.v1.repository.UsersRepository import UsersRepository
from app.v1.repository.TalentProfilesRepository import TalentProfilesRepository
from app.config.postgres_orm_config import scoped_session_factory
from app.config.logger_config import LogConfig

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

talent_future_potential_bp = Blueprint('talent_future_potential', __name__)
users_repository = UsersRepository(scoped_session_factory)
talent_profiles_repository = TalentProfilesRepository(scoped_session_factory)

class TalentFuturePotentialIdentifierController:
    @staticmethod
    @talent_future_potential_bp.route('/api/talent/profile', methods=['GET'])
    @jwt_required()
    def get_talent_profile():
        """Retrieve the activity DNA profile for a child."""
        user_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'parent':
                return jsonify({'error': 'Unauthorized access'}), 403

            student_id = user.student_id
            if not student_id:
                return jsonify({'error': 'Student ID not found for parent'}), 404

            talent_profiles = talent_profiles_repository.get_profiles_by_student_id(student_id)
            response = {
                'student_id': student_id,
                'talent_profile': {
                    'domains': [{'domain': profile.domain, 'hours_invested': profile.performance_data.get('hours_invested', 0), 'score': profile.score} for profile in talent_profiles]
                }
            }

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving talent profile: {e}")
            return jsonify({'error': 'An error occurred while retrieving the talent profile'}), 500

    @staticmethod
    @talent_future_potential_bp.route('/api/talent/profile', methods=['POST'])
    @jwt_required()
    def update_talent_profile():
        """Update or add performance data."""
        data = request.json
        try:
            user_id = get_jwt_identity()
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'parent':
                return jsonify({'error': 'Unauthorized access'}), 403

            student_id = user.student_id
            if not student_id:
                return jsonify({'error': 'Student ID not found for parent'}), 404

            profile_data = {
                'student_id': student_id,
                'domain': data['domain'],
                'performance_data': data['performance_data'],
                'score': data['performance_data'].get('score', 0)
            }

            talent_profiles_repository.create_profile(profile_data)
            return jsonify({'message': 'Talent profile updated successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error updating talent profile: {e}")
            return jsonify({'error': 'An error occurred while updating the talent profile'}), 500

    @staticmethod
    @talent_future_potential_bp.route('/api/talent/scores', methods=['GET'])
    @jwt_required()
    def get_talent_scores():
        """Retrieve the calculated future potential scores."""
        user_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'parent':
                return jsonify({'error': 'Unauthorized access'}), 403

            student_id = user.student_id
            if not student_id:
                return jsonify({'error': 'Student ID not found for parent'}), 404

            # Placeholder for future potential scores calculation logic
            scores = {
                'Robotics': 92,
                'Cricket': 88,
                'Arts': 75,
                'Leadership': 80
            }

            response = {
                'student_id': student_id,
                'scores': scores,
                'radar_chart_url': 'https://cdn.example.com/charts/radar_456.png'
            }

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving talent scores: {e}")
            return jsonify({'error': 'An error occurred while retrieving the talent scores'}), 500

    @staticmethod
    @talent_future_potential_bp.route('/api/talent/recommendations', methods=['GET'])
    @jwt_required()
    def get_talent_recommendations():
        """Provide proactive recommendations based on the brilliance engine."""
        user_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'parent':
                return jsonify({'error': 'Unauthorized access'}), 403

            student_id = user.student_id
            if not student_id:
                return jsonify({'error': 'Student ID not found for parent'}), 404

            # Placeholder for recommendations logic
            recommendations = [
                'Join a robotics mentorship program.',
                'Participate in district-level cricket tournaments.'
            ]

            response = {
                'student_id': student_id,
                'recommendations': recommendations
            }

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving talent recommendations: {e}")
            return jsonify({'error': 'An error occurred while retrieving the talent recommendations'}), 500

    @staticmethod
    @talent_future_potential_bp.route('/api/talent/peer-comparison', methods=['GET'])
    @jwt_required()
    def get_peer_comparison():
        """Fetch anonymized peer benchmarks for comparison."""
        user_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(user_id)
            if not user or user.role != 'parent':
                return jsonify({'error': 'Unauthorized access'}), 403

            student_id = user.student_id
            if not student_id:
                return jsonify({'error': 'Student ID not found for parent'}), 404

            # Placeholder for peer comparison logic
            peer_comparison = {
                'Robotics': 'Top 10%',
                'Cricket': 'Top 25%'
            }

            response = {
                'student_id': student_id,
                'peer_comparison': peer_comparison
            }

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving peer comparison: {e}")
            return jsonify({'error': 'An error occurred while retrieving the peer comparison'}), 500

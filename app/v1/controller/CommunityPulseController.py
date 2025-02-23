from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.v1.repository.CommunityForumRepository import CommunityForumRepository
from app.v1.repository.CommunityPollRepository import CommunityPollRepository
from app.v1.repository.UsersRepository import UsersRepository
from app.config.postgres_orm_config import scoped_session_factory
from app.config.logger_config import LogConfig
import json

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

community_pulse_bp = Blueprint('community_pulse', __name__)
community_forum_repository = CommunityForumRepository(scoped_session_factory)
community_poll_repository = CommunityPollRepository(scoped_session_factory)
users_repository = UsersRepository(scoped_session_factory)

class CommunityPulseController:
    @staticmethod
    @community_pulse_bp.route('/api/community/forums', methods=['GET'])
    @jwt_required()
    def get_forums():
        """Retrieve regional forum discussions with auto-translation support."""
        try:
            forums = community_forum_repository.get_all_forums()
            response = [{
                'id': forum.id,
                'parent_id': forum.parent_id,
                'student_id': forum.student_id,
                'title': forum.title,
                'content': forum.content,
                'language': forum.language,
                'is_anonymous': forum.is_anonymous,
                'is_reply': forum.is_reply,
                'forum_id': forum.forum_id,
                'created_at': forum.created_at,
                'updated_at': forum.updated_at
            } for forum in forums]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving forums: {e}")
            return jsonify({'error': 'An error occurred while retrieving forums'}), 500

    @staticmethod
    @community_pulse_bp.route('/api/community/forums', methods=['POST'])
    @jwt_required()
    def create_forum():
        """Post a new discussion or reply (with options for anonymity)."""
        data = request.json
        try:
            parent_id = get_jwt_identity()
            user = users_repository.get_user_by_id(parent_id)
            if not user:
                return jsonify({'error': 'Unauthorized access'}), 403

            forum_data = {
                'parent_id': parent_id,
                'student_id': user.student_id,
                'title': data.get('title'),
                'content': data['content'],
                'language': data['language'],
                'is_anonymous': data.get('is_anonymous', False),
                'is_reply': data.get('is_reply', False),
                'forum_id': data.get('forum_id')
            }

            forum = community_forum_repository.create_forum(forum_data)
            return jsonify({'forum_id': forum.id, 'message': 'Forum post created successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error creating forum post: {e}")
            return jsonify({'error': 'An error occurred while creating the forum post'}), 500

    @staticmethod
    @community_pulse_bp.route('/api/community/forums/<int:forum_id>/replies', methods=['GET'])
    @jwt_required()
    def get_replies(forum_id):
        """Retrieve replies for a specific forum discussion."""
        try:
            replies = community_forum_repository.get_replies_by_forum_id(forum_id)
            response = [{
                'id': reply.id,
                'parent_id': reply.parent_id,
                'student_id': reply.student_id,
                'title': reply.title,
                'content': reply.content,
                'language': reply.language,
                'is_anonymous': reply.is_anonymous,
                'is_reply': reply.is_reply,
                'forum_id': reply.forum_id,
                'created_at': reply.created_at,
                'updated_at': reply.updated_at
            } for reply in replies]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving replies: {e}")
            return jsonify({'error': 'An error occurred while retrieving replies'}), 500

    @staticmethod
    @community_pulse_bp.route('/api/community/forums/<int:forum_id>/replies', methods=['POST'])
    @jwt_required()
    def post_reply(forum_id):
        """Post a reply to a specific forum discussion."""
        data = request.json
        try:
            parent_id = get_jwt_identity()
            user = users_repository.get_user_by_id(parent_id)
            if not user:
                return jsonify({'error': 'Unauthorized access'}), 403

            reply_data = {
                'parent_id': parent_id,
                'student_id': user.student_id,
                'content': data['content'],
                'language': data['language'],
                'is_anonymous': data.get('is_anonymous', False),
                'is_reply': True,
                'forum_id': forum_id
            }

            reply = community_forum_repository.create_reply(reply_data)
            return jsonify({'reply_id': reply.id, 'message': 'Reply posted successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error posting reply: {e}")
            return jsonify({'error': 'An error occurred while posting the reply'}), 500

    @staticmethod
    @community_pulse_bp.route('/api/community/polls', methods=['GET'])
    @jwt_required()
    def get_polls():
        """Get active anonymous polls."""
        try:
            polls = community_poll_repository.get_all_polls()
            response = [{
                'id': poll.id,
                'parent_id': poll.parent_id,
                'student_id': poll.student_id,
                'question': poll.question,
                'options': poll.options,
                'votes': poll.votes,
                'created_at': poll.created_at,
                'updated_at': poll.updated_at
            } for poll in polls]
            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving polls: {e}")
            return jsonify({'error': 'An error occurred while retrieving polls'}), 500

    @staticmethod
    @community_pulse_bp.route('/api/community/polls', methods=['POST'])
    @jwt_required()
    def create_poll():
        """Submit a poll vote or new poll creation."""
        data = request.json
        try:
            parent_id = get_jwt_identity()
            user = users_repository.get_user_by_id(parent_id)
            if not user:
                return jsonify({'error': 'Unauthorized access'}), 403

            if 'poll_id' in data:
                # Update existing poll votes
                poll_id = data['poll_id']
                selected_option = data['selected_option']
                poll = community_poll_repository.get_poll_by_id(poll_id)
                if not poll:
                    return jsonify({'error': 'Poll not found'}), 404

                votes = json.loads(poll.votes)
                votes[selected_option] = votes.get(selected_option, 0) + 1
                updated_poll = community_poll_repository.update_poll_votes(poll_id, json.dumps(votes))
                return jsonify({'message': 'Poll vote submitted successfully.'}), 200
            else:
                # Create new poll
                if 'question' not in data:
                    return jsonify({'error': 'Missing required field: question'}), 400

                poll_data = {
                    'parent_id': parent_id,
                    'student_id': user.student_id,
                    'question': data['question'],
                    'options': json.dumps(data['options']),
                    'votes': json.dumps({option: 0 for option in data['options']})
                }

                poll = community_poll_repository.create_poll(poll_data)
                return jsonify({'poll_id': poll.id, 'message': 'Poll created successfully.'}), 201
        except KeyError as e:
            logger.error(f"Missing required field: {e}")
            return jsonify({'error': f"Missing required field: {e}"}), 400
        except Exception as e:
            logger.error(f"Error creating poll: {e}")
            return jsonify({'error': 'An error occurred while creating the poll'}), 500

    @staticmethod
    @community_pulse_bp.route('/api/community/engagement', methods=['GET'])
    @jwt_required()
    def get_engagement():
        """Retrieve the 'Engagement Score' and rewards status."""
        parent_id = get_jwt_identity()
        try:
            user = users_repository.get_user_by_id(parent_id)
            if not user:
                return jsonify({'error': 'Unauthorized access'}), 403

            # Placeholder for engagement score and rewards status logic
            engagement_score = 85
            rewards = [
                {'reward': 'Free eBook', 'points_required': 50},
                {'reward': 'Discount on next course', 'points_required': 100}
            ]

            response = {
                'parent_id': parent_id,
                'engagement_score': engagement_score,
                'rewards': rewards
            }

            return jsonify(response), 200
        except Exception as e:
            logger.error(f"Error retrieving engagement score: {e}")
            return jsonify({'error': 'An error occurred while retrieving the engagement score'}), 500

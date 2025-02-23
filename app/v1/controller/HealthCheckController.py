# HealthCheckController.py

from flask import Blueprint, jsonify
from app.config.logger_config import LogConfig

# Create a blueprint for health checks
health_check_bp = Blueprint('health_check', __name__)

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

@health_check_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint that returns a JSON response indicating service status.
    """
    logger.info("Health check endpoint called.")
    return jsonify({
        'status': 'healthy',
        'message': 'Service is up and running.'
    }), 200

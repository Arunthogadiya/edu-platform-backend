import os

from flask import Flask
import logging
from flask_jwt_extended import JWTManager
from app.v1.controller.HealthCheckController import (
    health_check_bp,
)
from app.v1.controller.UserRegisterController import user_register_bp
from app.config.auth import Auth
from datetime import timedelta


app = Flask(__name__)

# Configure your JWT settings
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)

# Initialize the JWTManager
jwt = JWTManager(app)

# Initialize the Auth class with the app
auth = Auth(app)

# Get the 'werkzeug' logger
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)

# Create a stream handler for console output
handler = logging.StreamHandler()

# Create a formatter with your desired format and date format
formatter = logging.Formatter(
    fmt='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Set the formatter on the handler
handler.setFormatter(formatter)

# Add the handler to the werkzeug logger
werkzeug_logger.addHandler(handler)

# Register the health check blueprint
app.register_blueprint(health_check_bp, url_prefix="/")
# Register the user register blueprint
app.register_blueprint(user_register_bp, url_prefix="/edu-platform/v1")

if __name__ == '__main__':
    debug = os.getenv("FLask_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)

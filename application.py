import os

from flask import Flask
import logging
from app.v1.controller.HealthCheckController import (
    health_check_bp,
)


app = Flask(__name__)

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

if __name__ == '__main__':
    debug = os.getenv("FLask_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)

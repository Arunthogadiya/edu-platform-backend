import logging
import os
from logging.handlers import RotatingFileHandler

class LogConfig:
    @staticmethod
    def setup_logger(logger_name, log_file='logs/app.log', level=logging.INFO):
        """
        Configures and returns a logger.

        Args:
            logger_name (str): The name of the logger.
            log_file (str): Path to the log file.
            level (int): Logging level.

        Returns:
            logging.Logger: The configured logger.
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Avoid adding multiple handlers if already configured
        if not logger.handlers:
            # Rotating file handler
            file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
            file_handler.setLevel(level)
            
            # Stream (console) handler
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            
            # Formatter
            formatter = logging.Formatter(
                fmt='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)
            
            # Add handlers to logger
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
        
        return logger

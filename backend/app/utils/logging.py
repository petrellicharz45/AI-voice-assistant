import logging
import os
from logging.handlers import RotatingFileHandler
from config.base import Config

def setup_logging(app=None):
    """
    Configure logging for the application
    
    :param app: Flask application instance (optional)
    """
    # Ensure logs directory exists
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    log_level = getattr(logging, Config.LOG_LEVEL.upper())
    
    # Create a formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File Handler - Rotating File
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'mrvoiceassistant.log'),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=[file_handler, console_handler]
    )
    
    # Create a logger for the application
    logger = logging.getLogger(__name__)
    
    # If Flask app is provided, add handlers
    if app:
        app.logger.addHandler(file_handler)
        app.logger.addHandler(console_handler)
        app.logger.setLevel(log_level)
    
    return logger

# Create a default logger
logger = setup_logging()
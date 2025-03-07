"""
Logging configuration for the application
"""
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime

# Configure log directory
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Create log file with date
log_filename = f"app_{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
log_filepath = os.path.join(LOG_DIR, log_filename)

# Configure logger
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create file handler
file_handler = RotatingFileHandler(
    log_filepath, 
    maxBytes=10485760,  # 10MB
    backupCount=10
)
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add formatter to handlers
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def get_logger(name):
    """
    Get a logger instance with the specified name
    
    :param name: Name for the logger (typically module name)
    :return: Logger instance
    """
    child_logger = logger.getChild(name)
    return child_logger

def log_request(request, include_headers=False, include_body=False):
    """
    Log HTTP request details
    
    :param request: Flask request object
    :param include_headers: Whether to include request headers in the log
    :param include_body: Whether to include request body in the log
    """
    logger.info(f"Request: {request.method} {request.path} {request.remote_addr}")
    
    if include_headers:
        logger.debug(f"Headers: {dict(request.headers)}")
    
    if include_body and request.is_json:
        try:
            logger.debug(f"Body: {request.get_json()}")
        except Exception as e:
            logger.warning(f"Could not log request body: {e}")

def log_response(response, include_headers=False, include_body=False):
    """
    Log HTTP response details
    
    :param response: Flask response object
    :param include_headers: Whether to include response headers in the log
    :param include_body: Whether to include response body in the log
    """
    logger.info(f"Response: {response.status_code}")
    
    if include_headers:
        logger.debug(f"Headers: {dict(response.headers)}")
    
    if include_body:
        try:
            logger.debug(f"Body: {response.get_data(as_text=True)}")
        except Exception as e:
            logger.warning(f"Could not log response body: {e}")

def log_exception(e, include_traceback=True):
    """
    Log exception details
    
    :param e: Exception object
    :param include_traceback: Whether to include traceback in the log
    """
    if include_traceback:
        logger.exception(f"Exception: {type(e).__name__}: {str(e)}")
    else:
        logger.error(f"Exception: {type(e).__name__}: {str(e)}")
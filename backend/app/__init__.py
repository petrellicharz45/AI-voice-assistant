from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config.base import Config
from .routes import voice_assistant, text_chat
from .utils.logging import logger  # Import the logger
from .utils.error_handlers import register_error_handlers  # Import error handler function

# Global SocketIO instance
socketio = SocketIO()

def create_app(config_class=Config):
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Import and register blueprints
    app.register_blueprint(voice_assistant.bp, url_prefix='/api/voice')
    app.register_blueprint(text_chat.bp, url_prefix='/api/chat')
    
    # Initialize error handlers - IMPORTANT: Add this line
    register_error_handlers(app)
    
    # Add CORS headers to all responses
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    # Log application startup
    logger.info(f"Application started in {app.config.get('ENV', 'development')} mode")
    
    return app
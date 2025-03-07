import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    # Secret key for sessions and security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-very-secret-key-change-in-production')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # LiveKit Credentials
    LIVEKIT_API_KEY = os.getenv('LIVEKIT_API_KEY')
    LIVEKIT_API_SECRET = os.getenv('LIVEKIT_API_SECRET')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Application Settings
    APP_NAME = "MrAssistant Voice Agent"
    
    # Database Configuration (if needed)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
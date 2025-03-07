from .base import Config

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = True
    
    # Additional development-specific settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    
    # More verbose logging
    LOG_LEVEL = 'DEBUG'
    
    # Development API endpoints or mock services
    MOCK_SERVICES_ENABLED = True
from .base import Config

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Production database (replace with your actual production database)
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/mrvoiceassistant'
    
    # More conservative logging
    LOG_LEVEL = 'WARNING'
    
    # Security enhancements
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
    # Rate limiting and other production safeguards
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
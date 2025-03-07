import os
from app import create_app, socketio
from config.development import DevelopmentConfig
from config.production import ProductionConfig

# Determine the environment
env = os.getenv('FLASK_ENV', 'development')

# Select configuration based on environment
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
config_class = config_map.get(env, DevelopmentConfig)

# Create Flask application
app = create_app(config_class)

if __name__ == '__main__':
    # Run the application
    print(f"Starting MrAssistant Voice Agent in {env.upper()} mode")
    socketio.run(
        app, 
        host='0.0.0.0', 
        port=5000, 
        debug=(env == 'development')
    )
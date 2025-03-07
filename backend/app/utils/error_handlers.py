from flask import jsonify
from .logging import logger

def register_error_handlers(app):
    """
    Register error handlers for the Flask application
    
    :param app: Flask application instance
    """
    @app.errorhandler(400)
    def bad_request(error):
        """
        Handle 400 Bad Request errors
        """
        logger.error(f"Bad Request: {error}")
        return jsonify({
            "status": "error",
            "message": "Bad request. Please check your input.",
            "error": str(error)
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        """
        Handle 401 Unauthorized errors
        """
        logger.error(f"Unauthorized Access: {error}")
        return jsonify({
            "status": "error",
            "message": "Unauthorized. Authentication required.",
            "error": str(error)
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        """
        Handle 403 Forbidden errors
        """
        logger.error(f"Forbidden Access: {error}")
        return jsonify({
            "status": "error",
            "message": "Forbidden. You don't have permission to access this resource.",
            "error": str(error)
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        """
        Handle 404 Not Found errors
        """
        logger.error(f"Resource Not Found: {error}")
        return jsonify({
            "status": "error",
            "message": "Resource not found. The requested endpoint does not exist.",
            "error": str(error)
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """
        Handle 500 Internal Server errors
        """
        logger.error(f"Internal Server Error: {error}")
        return jsonify({
            "status": "error",
            "message": "Internal server error. Our team has been notified.",
            "error": str(error)
        }), 500

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        """
        Handle any unhandled exceptions
        """
        logger.error(f"Unhandled Exception: {error}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred.",
            "error": str(error)
        }), 500
"""
Error handling utilities for Flask application
"""
from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
import traceback
import sys

def register_error_handlers(app):
    """
    Register error handlers for the Flask application
    
    :param app: Flask application instance
    """
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors"""
        return jsonify({
            'status': 'error',
            'message': 'Bad request: ' + str(error),
            'error_code': 400
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors"""
        return jsonify({
            'status': 'error',
            'message': 'Unauthorized: ' + str(error),
            'error_code': 401
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors"""
        return jsonify({
            'status': 'error',
            'message': 'Forbidden: ' + str(error),
            'error_code': 403
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors"""
        return jsonify({
            'status': 'error',
            'message': 'Resource not found',
            'error_code': 404
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors"""
        return jsonify({
            'status': 'error',
            'message': 'Method not allowed',
            'error_code': 405
        }), 405

    @app.errorhandler(429)
    def too_many_requests(error):
        """Handle 429 Too Many Requests errors"""
        return jsonify({
            'status': 'error',
            'message': 'Too many requests. Please try again later.',
            'error_code': 429
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error"""
        # Log the error details
        current_app.logger.error(f"Internal Server Error: {error}")
        current_app.logger.error(traceback.format_exc())
        
        return jsonify({
            'status': 'error',
            'message': 'An internal server error occurred',
            'error_code': 500
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle unhandled exceptions"""
        # Log the error
        exc_type, exc_value, exc_traceback = sys.exc_info()
        current_app.logger.error(f"Unhandled Exception: {exc_type.__name__}: {exc_value}")
        current_app.logger.error(traceback.format_exc())
        
        # Print to console in development
        if app.debug:
            print(f"Exception: {exc_type.__name__}: {exc_value}")
            traceback.print_exc()
        
        # Handle HTTP exceptions
        if isinstance(e, HTTPException):
            return jsonify({
                'status': 'error',
                'message': str(e),
                'error_code': e.code
            }), e.code
        
        # Handle generic exceptions
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'error_code': 500
        }), 500
from flask import Blueprint, request, jsonify
from ..services.llm_service import ChatService

# Create a blueprint for text chat routes
bp = Blueprint('text_chat', __name__)

# Initialize chat service
chat_service = ChatService()

@bp.route('/', methods=['GET', 'OPTIONS'])
def chat_root():
    """
    Root endpoint for /api/chat
    """
    return jsonify({
        "status": "success",
        "message": "Welcome to the chat API"
    }), 200

@bp.route('/send', methods=['POST'])
def send_message():
    """
    Endpoint to send a text message and get a response
    """
    try:
        # Get message from request
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({
                "status": "error",
                "message": "No message provided"
            }), 400
        
        user_message = data['message']
        
        # Optional: chat history or context
        chat_history = data.get('chat_history', [])
        
        # Generate response
        response = chat_service.generate_response(
            user_message, 
            chat_history
        )
        
        return jsonify({
            "status": "success",
            "response": response,
            "message_type": "text"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@bp.route('/context', methods=['POST'])
def update_context():
    """
    Endpoint to update conversation context
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                "status": "error",
                "message": "No context data provided"
            }), 400
        
        # Update conversation context
        chat_service.update_context(data)
        
        return jsonify({
            "status": "success",
            "message": "Context updated successfully"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
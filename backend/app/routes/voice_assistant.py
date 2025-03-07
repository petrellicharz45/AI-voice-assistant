from flask import Blueprint, request, jsonify
from ..services.voice_service import VoiceAssistantService

# Create a blueprint for voice-related routes
bp = Blueprint('voice_assistant', __name__)

# Initialize voice assistant service
voice_service = VoiceAssistantService()

@bp.route('/start', methods=['POST'])
def start_voice_assistant():
    """
    Endpoint to start the voice assistant
    """
    try:
        # Get any configuration from request
        config = request.json or {}
        
        # Start voice assistant
        session_id = voice_service.start_session(config)
        
        return jsonify({
            "status": "success",
            "message": "Voice assistant started",
            "session_id": session_id
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@bp.route('/stop', methods=['POST'])
def stop_voice_assistant():
    """
    Endpoint to stop the voice assistant
    """
    try:
        session_id = request.json.get('session_id')
        
        if not session_id:
            return jsonify({
                "status": "error",
                "message": "Session ID is required"
            }), 400
        
        voice_service.stop_session(session_id)
        
        return jsonify({
            "status": "success",
            "message": "Voice assistant stopped"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@bp.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Endpoint to transcribe audio
    """
    try:
        # Check if audio file is present
        if 'audio' not in request.files:
            return jsonify({
                "status": "error",
                "message": "No audio file provided"
            }), 400
        
        audio_file = request.files['audio']
        
        # Transcribe audio
        transcription = voice_service.transcribe_audio(audio_file)
        
        return jsonify({
            "status": "success",
            "transcription": transcription
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
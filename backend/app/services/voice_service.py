import uuid
import os
import datetime
import logging
from werkzeug.utils import secure_filename

# Import speech recognition with error handling
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    logging.warning("speech_recognition module not found. Speech transcription will be limited.")

class VoiceAssistantService:
    def __init__(self):
        """
        Initialize voice assistant service with necessary configurations
        """
        # Active sessions tracking
        self.active_sessions = {}
        
        # Temporary storage for audio files
        self.UPLOAD_FOLDER = 'uploads'
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
        
        # Check for API key if needed for transcription services
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
    def start_session(self, config=None):
        """
        Start a new voice assistant session
        
        :param config: Optional configuration for the session
        :return: Unique session ID
        """
        session_id = str(uuid.uuid4())
        
        # Store session details
        self.active_sessions[session_id] = {
            'created_at': datetime.datetime.now(),
            'config': config or {},
            'status': 'active'
        }
        
        return session_id
    
    def stop_session(self, session_id):
        """
        Stop an active voice assistant session
        
        :param session_id: Unique identifier for the session
        """
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['status'] = 'closed'
            return True
        return False
    
    def transcribe_audio(self, audio_file):
        """
        Transcribe audio file to text using speech recognition
        
        :param audio_file: Audio file to transcribe (from request.files)
        :return: Transcribed text
        """
        if not audio_file:
            return "No audio file provided"
        
        try:
            # Secure filename and save
            filename = secure_filename(audio_file.filename or f"audio_{uuid.uuid4()}.wav")
            filepath = os.path.join(self.UPLOAD_FOLDER, filename)
            audio_file.save(filepath)
            
            # Check file exists and has content
            if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
                return "Audio file is empty or couldn't be saved"
            
            # Use SpeechRecognition for transcription if available
            if SPEECH_RECOGNITION_AVAILABLE:
                try:
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(filepath) as source:
                        audio = recognizer.record(source)
                    
                    # Try to transcribe
                    transcription = recognizer.recognize_google(audio)
                    return transcription
                except sr.UnknownValueError:
                    return "Could not understand audio"
                except sr.RequestError as e:
                    return f"Speech recognition service unavailable: {e}"
                except Exception as e:
                    logging.error(f"Error in speech recognition: {e}")
                    return "Error processing audio with speech recognition"
            else:
                # Fallback for testing without speech_recognition
                # Return a placeholder message based on file size
                file_size = os.path.getsize(filepath)
                if file_size < 1000:
                    return "Audio received (small file). Speech recognition not available."
                else:
                    return "Audio received (large file). Speech recognition not available."
                
        except Exception as e:
            logging.error(f"Transcription error: {e}")
            return f"Error processing audio: {str(e)}"
        finally:
            # Always clean up the file
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                logging.error(f"Error removing temporary file: {e}")
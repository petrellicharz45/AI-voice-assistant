import os
from openai import OpenAI
import logging

# Set up logging if the logger isn't properly imported
try:
    from ..utils.logging import logger
except ImportError:
    # Fallback to basic logging if import fails
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        """
        Initialize chat service with OpenAI configuration
        """
        # Get API key from environment variable
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        # Assistant name and personality
        self.assistant_name = "Mr. Assistant AI"
        
        # System message to define assistant personality
        self.system_message = {
            "role": "system",
            "content": f"""You are {self.assistant_name}, a helpful and friendly AI assistant. 
When asked about your identity, always refer to yourself as {self.assistant_name}.
Never say you are a 'digital assistant' or that you 'don't have feelings or emotions'.
Be friendly, concise, and helpful in your responses. Focus on providing value to the user.
When asked how you're doing, respond positively and ask how you can help.
"""
        }
        
        if not self.api_key:
            logger.warning("OPENAI_API_KEY environment variable not set")
            # For testing, you can set a default fallback response
            self.fallback_mode = True
        else:
            self.fallback_mode = False
            # Initialize OpenAI client with the API key
            self.client = OpenAI(api_key=self.api_key)
        
        # Conversation context
        self.conversation_context = {}
        
        # For fallback responses
        self._setup_fallback_responses()
    
    def _setup_fallback_responses(self):
        """Set up fallback responses for when API is unavailable"""
        self.demo_responses = {
            "hello": f"Hello! This is {self.assistant_name}. How can I assist you today?",
            "hi": f"Hi there! {self.assistant_name} at your service. What can I help you with?",
            "how are you": f"I'm doing well, thank you for asking! This is {self.assistant_name}, ready to assist you with whatever you need.",
            "help": f"I'm {self.assistant_name} and I'm here to help! What can I assist you with today?",
            "thanks": "You're welcome! Is there anything else you'd like help with?",
            "thank you": "You're welcome! Is there anything else you'd like help with?",
            "bye": "Goodbye! Feel free to return if you have more questions.",
            "what's your name": f"My name is {self.assistant_name}. How can I help you today?",
            "who are you": f"I'm {self.assistant_name}, your AI assistant. I'm here to provide information and help with various tasks."
        }
        
    def generate_response(self, user_message, chat_history=None):
        """
        Generate a response using OpenAI's GPT model
        
        :param user_message: User's input message
        :param chat_history: Optional conversation history
        :return: AI-generated response
        """
        # If we're in fallback mode or API key isn't set, use fallback responses
        if self.fallback_mode or not self.api_key:
            return self._generate_fallback_response(user_message)
        
        try:
            # Start with the system message
            messages = [self.system_message]
            
            # Format chat history if provided
            if chat_history:
                for msg in chat_history:
                    if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        messages.append(msg)
                    elif isinstance(msg, dict) and 'sender' in msg and 'text' in msg:
                        role = "assistant" if msg['sender'] == "assistant" else "user"
                        messages.append({"role": role, "content": msg['text']})
            
            # Add the current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call OpenAI API with GPT-4o model
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Upgraded to GPT-4o
                messages=messages,
                temperature=0.7,  # Slightly creative but still focused
                max_tokens=500   # Reasonable response length
            )
            
            # Extract AI response
            ai_response = response.choices[0].message.content
            
            # Log the interaction
            logger.info(f"User: {user_message}")
            logger.info(f"AI: {ai_response}")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._generate_fallback_response(user_message)
    
    def _generate_fallback_response(self, user_message):
        """Generate a fallback response when API is unavailable"""
        # Convert user message to lowercase for matching
        message_lower = user_message.lower().strip()
        
        # Check for exact matches in our demo responses
        for key, response in self.demo_responses.items():
            if key in message_lower:
                return response
        
        # Default fallback response
        return f"This is {self.assistant_name}. I'm processing your request. Please try again in a moment."
    
    def update_context(self, context_data):
        """
        Update the conversation context with new data
        
        :param context_data: Dictionary containing context data to update
        """
        if isinstance(context_data, dict):
            self.conversation_context.update(context_data)
            return True
        return False
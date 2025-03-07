# MrAssistant Voice Agent

## Overview
MrAssistant is an advanced voice-enabled AI assistant built with Flask, integrating cutting-edge speech recognition, natural language processing, and text-to-speech technologies.

## Features
- Voice-to-Text Transcription
- Text-based Chat Interactions
- OpenAI GPT Integration
- Flexible Configuration Management
- Comprehensive Logging
- Error Handling

## Prerequisites
- Python 3.8+
- pip
- Virtual Environment

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/mrvoiceassistant.git
cd mrvoiceassistant
```

2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Configure Environment Variables
Create a `.env` file with the following:
```
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_api_key
FLASK_ENV=development
```

## Running the Application

### Development Mode
```bash
python run.py
```

### Production Mode
```bash
FLASK_ENV=production python run.py
```

## Testing
```bash
pytest tests/
```

## Project Structure
- `app/`: Main application package
- `config/`: Configuration management
- `routes/`: API endpoint definitions
- `services/`: Business logic
- `models/`: Data models
- `utils/`: Utility functions

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License


## Contact
Your Name - kiwalabye45charles@gmail.com
Project Link: https://github.com/petrellicharz45/AI-voice-assistant/
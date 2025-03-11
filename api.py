import enum
from typing import Annotated
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import silero, openai
import logging
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# System prompt for the assistant
SYSTEM_PROMPT = (
    "You're a smart MrAssistant AI created by MrAssistant Company. "
    "Your interface with users is going to be Audio. "
    "You should use short and concise responses to user queries and avoid using unpronounceable punctuations."
)

async def handle_conversation(assistant: VoiceAssistant):
    """
    Handles the conversation flow with the user.
    """
    while True:
        user_input = await assistant.listen()
        if not user_input:
            continue

        logger.info(f"User said: {user_input}")

        if "goodbye" in user_input.lower():
            await assistant.say("Goodbye! Have a great day.")
            break

        # Generate a response using the LLM
        response = await assistant.llm.generate(user_input)
        await assistant.say(response)

async def entrypoint(ctx: JobContext):
    """
    Entrypoint for the LiveKit job.
    """
    try:
        # Initial system message for the assistant
        initial_ctx = llm.ChatContext().append(
            role="system",
            text=SYSTEM_PROMPT,
        )

        # Connect to LiveKit
        logger.info("Connecting to LiveKit...")
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

        # Initialize the voice assistant
        assistant = VoiceAssistant(
            vad=silero.VAD.load(),  # Voice Activity Detection
            stt=openai.STT(),      # Speech-to-Text
            tts=openai.TTS(),      # Text-to-Speech
            llm=openai.LLM(),      # Large Language Model
            chat_ctx=initial_ctx,  # Initial chat context
        )

        # Start the assistant
        logger.info("Starting voice assistant...")
        assistant.start(ctx.room)

        # Greet the user
        await asyncio.sleep(1)
        await assistant.say("Hello, I'm MrAssistant, your voice assistant. How can I help you today?", allow_interruptions=True)

        # Handle the conversation
        await handle_conversation(assistant)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Shutting down...")
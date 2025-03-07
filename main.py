from livekit.agents import cli, WorkerOptions
from api import entrypoint

if __name__ == "__main__":
    try:
        cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
    except KeyboardInterrupt:
        print("Application terminated by user.")
    except Exception as e:
        print(f"Application failed: {e}")
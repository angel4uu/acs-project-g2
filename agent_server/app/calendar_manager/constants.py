import os
import dotenv

dotenv.load_dotenv()

AGENT_NAME = "calendar_manager_agent"
AGENT_DESCRIPTION = "Agente para gestionar y optimizar el calendario del usuario."
AGENT_MODEL = "gemini-2.5-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

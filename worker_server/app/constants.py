import os
import dotenv

dotenv.load_dotenv()

RABBITMQ_USER = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "rabbitmq")
AGENT_SERVER_URL = os.environ.get("AGENT_SERVER_URL", "http://agent-server:8000")

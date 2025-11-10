from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
import os

# Configuration of agent server
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AGENT_DIR = BASE_DIR

print(f"Iniciando ADK server desde el directorio: {AGENT_DIR}")
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    allow_origins=["*"],
    web=True,
)

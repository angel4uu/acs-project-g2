from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .tools import sync_events, save_events
from . import prompt


saving_agent = Agent(
    model="gemini-2.5-flash",
    name="saving_agent",
    description="Agente encargado de guardar y sincronizar el plan diario con la base de datos y el calendario del usuario cuando ha sido aceptado.",
    instruction=prompt.SAVING_PROMPT,
    tools=[sync_events, save_events],
)

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .tools import get_today_calendar_events, get_metrics
from . import prompt
from libraries import schemas
from google.genai import types

plan_generation_agent = Agent(
    model="gemini-2.5-flash",
    name="plan_generation_agent",
    description="Genera un plan diario optimizado basado en el calendario y métricas del usuario.",
    instruction=prompt.PLAN_GENERATION_PROMPT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=schemas.PlanGenerationOutput,
    output_key="today_plan_generation_output",
    generate_content_config=types.GenerateContentConfig(
        response_mime_type="application/json"
    ),
)

planning_agent = Agent(
    model="gemini-2.5-flash",
    name="planning_agent",
    description="Agente encargado de planificar el día del usuario basándose en sus eventos de calendario y métricas diarias.",
    instruction=prompt.PLANNING_PROMPT,
    tools=[get_today_calendar_events, get_metrics, AgentTool(plan_generation_agent)],
)

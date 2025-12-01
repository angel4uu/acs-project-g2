from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .tools import save_metrics
from daily_plan_generator.subagents.plannning.tools import get_today_calendar_events
from . import prompt
from libraries import schemas
from google.genai import types

event_mapping_agent = Agent(
    model="gemini-2.5-flash",
    name="event_mapping_agent",
    description="Determina qué evento del calendario debe ser rastreado basándose en el nombre solicitado por el usuario.",
    instruction=prompt.EVENT_MAPPING_PROMPT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=schemas.CalendarEvent,
    output_key="tracking_event",
    generate_content_config=types.GenerateContentConfig(
        response_mime_type="application/json"
    ),
)

question_generation_agent = Agent(
    model="gemini-2.5-flash",
    name="question_generation_agent",
    description="Genera micro-interacciones naturales para iniciar el bucle de retroalimentación post-evento.",
    instruction=prompt.QUESTION_GENERATION_PROMPT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

metrics_generation_agent = Agent(
    model="gemini-2.5-flash",
    name="metrics_generation_agent",
    description="Traduce las respuestas del usuario en métricas cuantificables para evaluar el éxito del evento.",
    instruction=prompt.METRICS_GENERATION_PROMPT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=schemas.MetricsGenerationOutput,
    output_key="tracking_metrics_generation_output",
    generate_content_config=types.GenerateContentConfig(
        response_mime_type="application/json"
    ),
)

tracking_agent = Agent(
    model="gemini-2.5-flash",
    name="tracking_agent",
    description="Agente encargado de realizar el seguimiento y evaluación de eventos diarios del usuario.",
    instruction=prompt.TRACKING_PROMPT,
    tools=[
        get_today_calendar_events,
        AgentTool(event_mapping_agent),
        AgentTool(question_generation_agent),
        AgentTool(metrics_generation_agent),
        save_metrics,
    ],
)

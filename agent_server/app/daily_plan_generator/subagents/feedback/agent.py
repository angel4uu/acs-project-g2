from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .tools import update_plan
from . import prompt
from libraries import schemas
from google.genai import types

feedback_interpretation_agent = Agent(
    model="gemini-2.5-flash",
    name="feedback_interpretation_agent",
    description="Interpreta el feedback del usuario sobre el plan diario propuesto y actualiza el borrador en consecuencia.",
    instruction=prompt.FEEDBACK_INTERPRETATION_PROMPT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=schemas.FeedbackInterpretationOutput,
    output_key="plan_feedback_interpretation_output",
    generate_content_config=types.GenerateContentConfig(
        response_mime_type="application/json"
    ),
)

feedback_agent = Agent(
    model="gemini-2.5-flash",
    name="feedback_agent",
    description="Agente encargado de manejar el feedback del usuario sobre el plan diario generado.",
    instruction=prompt.FEEDBACK_PROMPT,
    tools=[AgentTool(feedback_interpretation_agent), update_plan],
)

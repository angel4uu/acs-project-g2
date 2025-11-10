from google.adk.agents import LlmAgent
from . import constants
from . import prompt
from .tools import analysis_tools

# Define the root agent
root_agent = LlmAgent(
    name=constants.AGENT_NAME,
    model=constants.AGENT_MODEL,
    description=constants.AGENT_DESCRIPTION,
    instruction=prompt.ROOT_PROMPT,
    tools=[analysis_tools.get_today_plan],
)

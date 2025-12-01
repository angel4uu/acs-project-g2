import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Ensure these imports are correct based on your file structure:
from .prompt import ROOT_SYSTEM_PROMPT
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from .subagents.plannning.agent import planning_agent
from .subagents.feedback.agent import feedback_agent
from .subagents.saving.agent import saving_agent
from .subagents.tracking.agent import tracking_agent


def set_init_state(callback_context: CallbackContext):
    # Load initial state from JSON file
    data = {}
    with open("libraries/states.json", "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")
    callback_context.state.update(data)

    # Get user's timezone from state or default to UTC
    user_tz_id = callback_context.state.get("user_profile:user_tz_id", "UTC")

    # Parse and validate timezone
    try:
        user_tz = ZoneInfo(user_tz_id)
    except Exception:
        # Final safety net if the ID is malformed
        user_tz = ZoneInfo("UTC")
        user_tz_id = "UTC"

    # Get current time in user's timezone
    current_utc_time = datetime.now(timezone.utc)
    current_local_time = current_utc_time.astimezone(user_tz)
    current_time_local_str = current_local_time.strftime("%Y-%m-%d %H:%M %Z")

    # Update state with current time info
    callback_context.state["current_local_time"] = current_time_local_str


print("Initializing Root Agent instance in agent.py...")
root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="The main orchestration agent for daily planning and tracking.",
    instruction=ROOT_SYSTEM_PROMPT,
    sub_agents=[planning_agent, feedback_agent, saving_agent, tracking_agent],
    before_agent_callback=set_init_state,
    tools=[],
)

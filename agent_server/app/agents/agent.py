from agents.definitions import RootAgent
from tools.planning import (
    orchestrate_daily_plan,
    handle_plan_feedback,
    finalize_plan,
)
from tools.tracking import ask_tracking_question, save_tracking_metrics

# Tools list
tools = [
    orchestrate_daily_plan,
    handle_plan_feedback,
    finalize_plan,
    ask_tracking_question,
    save_tracking_metrics,
]

# Root Agent instance
print("Initializing Root Agent instance in agent.py...")
root_agent = RootAgent(tools=tools)

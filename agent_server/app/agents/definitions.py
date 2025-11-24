from datetime import datetime, timezone
from google.adk.agents import Agent
from google.adk.agents.invocation_context import InvocationContext
from schemas import (
    DailyPlanOutput,
    FeedbackInterpretationOutput,
    TrackingMetricOutput,
)
from agents import prompts


# --- Agente Principal (Chat) ---
class RootAgent(Agent):
    def __init__(self, tools):
        super().__init__(
            name="root_agent",
            model="gemini-2.5-flash",
            tools=tools,
            instruction=prompts.ROOT_PROMPT,
        )

    async def run_async(self, invocation_context: InvocationContext):
        # Gather user-specific data from session state
        user_name = invocation_context.agent_states.get("user_name", "Usuario")
        invocation_context.agent_states["user_name"] = user_name

        # Maintain session mode
        current_mode = invocation_context.agent_states.get("session_mode", "NORMAL")
        invocation_context.agent_states["session_mode"] = current_mode
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        # Update instruction with dynamic context
        self.instruction = prompts.ROOT_PROMPT.format(
            user_name=user_name,
            current_time_utc=current_time,
            session_mode=current_mode,
        )

        # Delegate execution back to the ADK framework
        async for event in super().run_async(invocation_context):
            yield event


# --- Sub-Agentes (Lógica JSON) ---
class PlanningAgent(Agent):
    def __init__(self):
        super().__init__(
            name="planner",
            model="gemini-2.5-flash",
            output_type=DailyPlanOutput,
            instruction=prompts.PLANNER_PROMPT,
        )

    def generate(self, events: list, metrics: dict) -> DailyPlanOutput:
        formatted_input = (
            f"INPUTS:\n1. `original_schedule`: {events}\n2. `user_metrics`: {metrics}"
        )
        return self.predict(formatted_input)


class InterpreterAgent(Agent):
    def __init__(self):
        super().__init__(
            name="interpreter",
            model="gemini-2.5-flash",
            output_type=FeedbackInterpretationOutput,
            instruction=prompts.INTERPRETER_PROMPT,
        )

    def interpret(
        self, draft_plan: dict, user_input: str
    ) -> FeedbackInterpretationOutput:
        formatted_input = (
            f'INPUTS:\n1. `draft_plan`: {draft_plan}\n2. `user_input`: "{user_input}"'
        )
        return self.predict(formatted_input)


class TrackingAgent(Agent):
    def __init__(self):
        super().__init__(
            name="tracker",
            model="gemini-2.5-flash",
            output_type=TrackingMetricOutput,
            instruction=prompts.TRACKER_PROMPT,
        )

    def analyze(
        self, event_name: str, scheduled_minutes: int, user_response: str
    ) -> TrackingMetricOutput:
        formatted_input = (
            f"INPUTS:\n"
            f"1. `event_context`: {event_name}\n"
            f"2. `scheduled_duration`: {scheduled_minutes} minutos\n"
            f'3. `user_response`: "{user_response}"'
        )
        return self.predict(formatted_input)


class QuestionerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="questioner",
            model="gemini-2.5-flash",
            instruction=prompts.QUESTIONER_SYSTEM_PROMPT,
        )

    def generate_question(self, name: str, category: str, start: str, end: str) -> str:
        self.instruction = prompts.QUESTIONER_SYSTEM_PROMPT.format(
            event_name=name, event_category=category, event_duration=f"{start} to {end}"
        )
        return self.predict("Generate question.")

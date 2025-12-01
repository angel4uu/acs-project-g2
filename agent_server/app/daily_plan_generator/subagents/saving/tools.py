from google.adk.tools import ToolContext
from services.mocks import MockCalendarService, MockDatabaseService


def sync_events(tool_context: ToolContext):
    """
    Sincroniza el plan diario con el calendario del usuario
    """
    # Retrieve state.
    user_id = tool_context.state.get("user_profile:user_id")
    plan = tool_context.state.get("today_plan_generation_output")
    today_events = tool_context.state.get("today_calendar_events")

    """ if not user_id:#TODO: habilitar despues de autenticacion
        return "Error: User ID missing from session state."
    """
    if not plan:
        return "Error: No active plan found to sync."

    try:
        # Get suggested modifications from the plan
        modifications = plan.get("suggested_modifications", [])

        # External Service Call
        calendar_service = MockCalendarService()
        updated_events = calendar_service.sync_changes(
            user_id=user_id, modifications=modifications, existing_events=today_events
        )

        # Save updated events back to state
        tool_context.state["today_calendar_events"] = updated_events

        return f"Success: Synced {len(modifications)} modifications to Google Calendar."
    except Exception as e:
        return f"Error during Calendar Sync: {str(e)}"


def save_events(tool_context: ToolContext):
    """
    Guarda el plan diario en la base de datos
    """
    # Retrieve Data
    events = tool_context.state.get("today_calendar_events")
    user_id = tool_context.state.get("user_profile:user_id")

    if not events:
        return "Error: No calendar events found in state. Did sync_events run?"

    try:
        # External Service Call
        database_service = MockDatabaseService()

        # Save events to the database
        database_service.save_events(user_id, events)

        return "Success: Final schedule saved to Database history."

    except Exception as e:
        return f"Error during Database Save: {str(e)}"

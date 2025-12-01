from google.adk.tools import ToolContext
from services.mocks import MockDatabaseService


def save_metrics(tool_context: ToolContext):
    """
    Saves the generated metrics and links them to the specific event ID.
    """
    user_id = tool_context.state.get("user_profile:user_id")

    # Get the metrics from state
    metrics = tool_context.state.get("tracking_metrics_generation_output")

    """ if not user_id:
        return "Error: User ID missing." """
    if not metrics:
        return "Error: No metrics generated to save."

    try:
        # Save metrics to the database
        MockDatabaseService.save_metrics(metrics, user_id)

        # Cleanup state (Optional but good practice to prevent stale data on next loop)
        tool_context.state["tracking_metrics_generation_output"] = None
        tool_context.state["tracking_event"] = None

        return "EXITO: Métricas guardadas correctamente."
    except Exception as e:
        return f"ERROR: Error al guardar métricas. Razón: {str(e)}"

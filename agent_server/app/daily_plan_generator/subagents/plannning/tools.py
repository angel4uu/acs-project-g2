from google.adk.tools import ToolContext
from services.mocks import MockCalendarService, MockAnalysisService


def get_today_calendar_events(tool_context: ToolContext):
    """
    Utiliza esta herramienta para obtener los eventos del calendario del usuario
    para el día actual.

    Returns:
        A status message indicating success or failure.
    """
    # Access user ID stored in context state
    user_id = tool_context.state.get("user_profile:user_id")
    """ if not user_id:#TODO Delete when auth setupped
        return "Error de sistema: No se encontró el ID de usuario en la sesión." """

    try:
        # Data Retrieval
        events = MockCalendarService.get_today_events(user_id)
        # Set states
        tool_context.state["today_calendar_events"] = events
        return f"EXITO: Se obtuvieron {len(events)} eventos del calendario. Datos: {str(events)}"
    except Exception as e:
        return f"ERROR: Error al obtener eventos. Razón: {str(e)}"


def get_metrics(tool_context: ToolContext):
    """
    Utiliza esta herramienta para obtener las métricas del usuario
    para el día actual.

    Returns:
        A status message indicating success or failure.
    """
    # Access user ID stored in context state
    user_id = tool_context.state.get("user_profile:user_id")
    """ if not user_id:#TODO Delete when auth setupped
        return "Error de sistema: No se encontró el ID de usuario en la sesión." """

    try:
        # Data Retrieval
        metrics = MockAnalysisService.get_metrics(user_id)  # TODO: Param correct?
        # Set states
        tool_context.state["today_metrics_summary"] = metrics
        return f"EXITO: Se obtuvieron las métricas del usuario. Datos: {str(metrics)}"
    except Exception as e:
        return f"ERROR: Error al obtener métricas. Razón: {str(e)}"

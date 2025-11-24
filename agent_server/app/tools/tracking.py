import datetime
from venv import logger
from services.mocks import MockDatabaseService
from agents.definitions import QuestionerAgent, TrackingAgent
from google.adk.tools import ToolContext


def ask_tracking_question(event_id: str, tool_context: ToolContext):
    """
    Utiliza esta herramienta cuando recibas una señal automática del sistema o un trigger
    indicando que un evento ha finalizado.

    Esta herramienta obtiene el contexto del evento y genera una pregunta de seguimiento
    para el usuario, cambiando el modo de sesión a 'TRACKING'.

    Args:
        event_id (str): ID del evento que acaba de terminar.
    """
    try:
        # Data Retrieval
        event = MockDatabaseService.get_event(event_id)
        if not event:
            return "Error: No pude encontrar el evento para hacer seguimiento."

        # Update state
        tool_context.state["tracking_event_id"] = event_id
        tool_context.state["session_mode"] = "TRACKING"

        # Agent Question Generation
        questioner = QuestionerAgent()
        question = questioner.generate_question(
            name=event.name, category=event.category, start=event.start, end=event.end
        )

        return question
    except Exception as e:
        logger.error(f"Error en ask_tracking_question: {e}", exc_info=True)
        return f"Veo que terminó '{event_id}'. ¿Podrías decirme si lo completaste y cómo te sentiste?"


def save_tracking_metrics(user_response: str, tool_context: ToolContext):
    """
    Utiliza esta herramienta EXCLUSIVAMENTE cuando el sistema esté en modo 'TRACKING'
    y el usuario responda a la pregunta de seguimiento sobre su actividad reciente.

    Esta herramienta analiza la respuesta, extrae métricas de productividad/ánimo,
    las guarda en la base de datos y devuelve la sesión al modo 'NORMAL'.

    Args:
        user_response (str): La respuesta textual del usuario.
    """
    try:
        event_id = tool_context.state.get("tracking_event_id")
        if not event_id:
            return "Error: Contexto de evento perdido."

        event = MockDatabaseService.get_event(event_id)
        if not event:
            return "Error: No pude encontrar el evento para hacer seguimiento."

        # Calculate Scheduled Duration
        start = datetime.fromisoformat(event.start.replace("Z", "+00:00"))
        end = datetime.fromisoformat(event.end.replace("Z", "+00:00"))
        scheduled_minutes = int((end - start).total_seconds() / 60)

        # Use TrackingAgent with injection
        tracker = TrackingAgent()
        metrics = tracker.analyze(
            event_name=event.name,
            scheduled_minutes=scheduled_minutes,
            user_response=user_response,
        )

        # Save to DB
        metrics_dict = metrics.model_dump()
        metrics_dict["event_id"] = int(event_id) if event_id.isdigit() else 1

        MockDatabaseService.save_metrics(metrics_dict)

        tool_context.state["session_mode"] = "NORMAL"
        tool_context.state["tracking_event_id"] = None

        return "Gracias, datos guardados. ¡Sigue así!"

    except Exception as e:
        logger.error(f"Error en save_tracking_metrics: {e}", exc_info=True)
        return (
            "Lo siento, ocurrió un error al intentar guardar tus datos de seguimiento."
        )

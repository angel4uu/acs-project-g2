from asyncio.log import logger
from services.mocks import (
    MockCalendarService,
    MockAnalysisService,
    MockQueueService,
)
from google.adk.tools import ToolContext
from agents.definitions import PlanningAgent, InterpreterAgent


def orchestrate_daily_plan(tool_context: ToolContext):
    """
    Utiliza esta herramienta cuando el usuario exprese intención de planificar su día,
    pregunte qué tiene en la agenda hoy, o quiera reorganizar sus eventos desde cero.

    Esta herramienta:
    1. Obtiene los eventos actuales y métricas del usuario.
    2. Genera un borrador de plan inteligente con sugerencias.
    3. Establece el modo de sesión a 'PLAN_REVIEW'.
    """
    # Access user ID stored in context state
    user_id = tool_context.state.get("user_id")
    if not user_id:
        return "Error de sistema: No se encontró el ID de usuario en la sesión."

    try:
        # Data Retrieval
        events = MockCalendarService.get_today_events(user_id)  # TODO: Param correct?
        metrics = MockAnalysisService.get_metrics(user_id)

        # Planning Agent Invocation
        planner = PlanningAgent()
        plan_json = planner.generate(events, metrics)

        # Save plan draft and review mode
        tool_context.state["draft_plan"] = plan_json.model_dump()
        tool_context.state["session_mode"] = "PLAN_REVIEW"

        return (
            f"He diseñado un plan con el tema: **{plan_json.daily_theme}**.\n"
            f"Sugerencias: {len(plan_json.suggested_modifications)}.\n"
            f"Resumen: {plan_json.summary_text}\n"
            "¿Revisamos los cambios?"
        )
    except Exception as e:
        logger.error(f"Error en orchestrate_daily_plan: {e}", exc_info=True)
        return "Lo siento, ocurrió un error al intentar generar tu plan. Por favor, inténtalo de nuevo en unos momentos."


def handle_plan_feedback(user_input: str, tool_context: ToolContext):
    """
    Utiliza esta herramienta EXCZ   LUSIVAMENTE cuando el sistema esté en modo 'PLAN_REVIEW'
    y el usuario proporcione feedback sobre el borrador presentado (ej: aprobar sugerencias,
    rechazar cambios, o solicitar modificaciones de hora específicas).

    Esta herramienta interpreta la intención del usuario y actualiza el borrador en memoria.

    Args:
        user_input (str): El texto completo del mensaje del usuario con sus instrucciones.
    """
    try:
        # Retrieve plan draft
        draft = tool_context.state.get("draft_plan")
        if not draft:
            return "Error: No hay un plan borrador para revisar."

        # Interpreter Agent Invocation
        interpreter = InterpreterAgent()
        interpretation = interpreter.interpret(draft, user_input)

        # Update Draft Based on Interpretation
        changes_summary = []

        for update in interpretation.modifications_updates:
            for mod in draft["suggested_modifications"]:
                if mod["temp_id"] == update.temp_id:
                    # Mapeamos la respuesta del interpreter al estado del borrador
                    if update.status == "APPROVED":
                        mod["review_status"] = "APPROVED"
                        changes_summary.append(f"Aceptado: {mod['name']}")
                    elif update.status == "REJECTED":
                        mod["review_status"] = "REJECTED"
                        changes_summary.append(f"Rechazado: {mod['name']}")
                    elif update.status == "MODIFIED":
                        mod["review_status"] = "APPROVED"
                        mod["start"] = update.new_start
                        mod["end"] = update.new_end
                        changes_summary.append(f"Modificado: {mod['name']}")

        # Identify Pending Modifications
        pending_mods = [
            m
            for m in draft["suggested_modifications"]
            if m["review_status"] == "PENDING"
        ]

        # Save updated draft
        tool_context.state["draft_plan"] = draft

        # Build response
        response_text = f"Cambios aplicados: {', '.join(changes_summary)}."

        if pending_mods:
            # If there are pending suggestions, guide the user
            names = [m["name"] for m in pending_mods]
            return f"{response_text}\n\nAún tienes {len(pending_mods)} sugerencias pendientes: {', '.join(names)}. ¿Qué hacemos con ellas?"
        else:
            # If none are pending, invite to finalize
            return f"{response_text}\n\nYa has revisado todas las sugerencias. ¿Escribo 'Confirmar' para aplicar los cambios?"

    except Exception as e:
        logger.error(f"Error en handle_plan_feedback: {e}", exc_info=True)
        return "Tuve un problema procesando tu respuesta. ¿Podrías repetirla?"


def finalize_plan(tool_context: ToolContext):
    """
    Utiliza esta herramienta cuando el usuario confirme explícitamente que está satisfecho
    con el plan actual (ej: "Confirmar", "Se ve bien", "Adelante") mientras está en modo 'PLAN_REVIEW'.

    Esta herramienta aplica permanentemente los cambios en el calendario y base de datos,
    y devuelve la sesión al modo 'NORMAL'.
    """
    # Access user ID stored in context state
    user_id = tool_context.state.get("user_id")
    if not user_id:
        return "Error de sistema: No se encontró el ID de usuario en la sesión."

    try:
        # Retrieve draft plan
        draft = tool_context.state.get("draft_plan")
        if not draft:
            return "Error: No hay un plan borrador para finalizar."

        # Impedimos finalizar si hay decisiones pendientes
        pending_items = [
            mod["name"]
            for mod in draft["suggested_modifications"]
            if mod.get("review_status") == "PENDING"
        ]

        if pending_items:
            items_str = ", ".join(pending_items)
            return (
                f"No puedo finalizar el plan todavía.\n\n"
                f"Tienes {len(pending_items)} sugerencias sin revisar: **{items_str}**.\n"
                "Por favor, dime si las apruebas, rechazas o modificas antes de confirmar."
            )

        # Filter approved modifications
        mods_to_sync = [
            mod
            for mod in draft["suggested_modifications"]
            if mod.get("review_status") == "APPROVED"
        ]

        # Handle case where user rejected all suggestions
        if not mods_to_sync:
            tool_context.state.set("session_mode", "NORMAL")
            tool_context.state.delete("draft_plan")
            return "Has rechazado todas las sugerencias. El calendario se mantiene sin cambios."

        # Execute approved modifications
        MockCalendarService.sync_changes(user_id, mods_to_sync)

        # Simulate publishing schedule to queue for reminder/tracking workers
        MockQueueService.publish_schedule(user_id, draft)

        # State
        tool_context.state["session_mode"] = "NORMAL"
        tool_context.state["draft_plan"] = None

        return f"¡Plan activado! He sincronizado {len(mods_to_sync)} cambios en tu calendario. ¡A por el día!"

    except Exception as e:
        logger.error(f"Error en finalize_plan: {e}", exc_info=True)
        return "Error crítico al intentar guardar los cambios en el calendario. Por favor verifica tu conexión."

import os
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

# Root paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AGENT_DIR = BASE_DIR

print(f"Starting ADK Server scanning directory: {AGENT_DIR}")

# Create FastAPI app with ADK
app: FastAPI = get_fast_api_app(agents_dir=AGENT_DIR, allow_origins=["*"], web=True)


# # Endpoint especial para triggers externos (ej: Worker)
# @app.post("/internal/trigger_tracking")
# async def trigger_tracking(payload: dict):
#     """
#     Este endpoint es llamado por el Worker cuando termina un evento.

#     Payload esperado:
#     {
#         "session_id": "uuid-session-123",
#         "event_id": "evt-google-555"
#     }
#     """
#     # Validación básica del payload
#     session_id = payload.get("session_id")
#     event_id = payload.get("event_id")

#     if not session_id or not event_id:
#         raise HTTPException(status_code=400, detail="Missing session_id or event_id")

#     print(f"⚡ [TRIGGER] Activando modo TRACKING para sesión: {session_id}")

#     # Accesamos el estado de la sesión y modificamos el modo
#     state = State(session_id)

#     # Cambiamos el modo de sesión a TRACKING
#     state["session_mode"] = "TRACKING"
#     state["tracking_event_id"] = event_id

#     # Inyectamos la pregunta de seguimiento para la próxima interacción
#     return {
#         "status": "armed",
#         "message": "Tracking mode set. Agent will ask on next interaction.",
#     }

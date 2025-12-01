from typing import List
import uuid
from libraries.schemas import (
    DBMetrics,
    MetricsGenerationOutput,
    Modification,
    CalendarEvent,
    DBEvent,
)


class MockCalendarService:
    @staticmethod
    def get_today_events(user_id: str):
        """Retorna eventos fijos simulados."""
        return [
            CalendarEvent(
                id="g_123",
                name="Reunión de Sincronización Semanal",
                start="2025-11-21T09:00:00Z",
                end="2025-11-21T09:30:00Z",
                category="MEETING",
            )
        ]

    @staticmethod
    def sync_changes(
        user_id: str,
        modifications: List[Modification],
        existing_events: List[CalendarEvent],
    ) -> List[CalendarEvent]:
        """
        Mock implementation that merges approved modifications into the existing calendar.
        """
        print(f"[MOCK CALENDAR] Starting synchronization for user {user_id}...")

        calendar_state = {}

        for event in existing_events:
            # Si es un modelo Pydantic v2
            if hasattr(event, "model_dump"):
                event_dict = event.model_dump()
            # Si es un modelo Pydantic v1
            elif hasattr(event, "dict"):
                event_dict = event.dict()
            # Si ya es un diccionario
            elif isinstance(event, dict):
                event_dict = event.copy()
            # Fallback para objetos genéricos
            else:
                event_dict = event.__dict__.copy()

            calendar_state[event_dict["id"]] = event_dict
        # --------------------------

        count_added = 0
        count_updated = 0
        count_removed = 0

        for mod in modifications:
            # Aseguramos que 'mod' sea dict (por si acaso llega como objeto)
            mod_data = mod.model_dump() if hasattr(mod, "model_dump") else mod

            # CRITICAL: Only process APPROVED modifications
            if mod_data.get("review_status") != "APPROVED":
                continue

            action = mod_data.get("action")

            # --- HANDLE ADD ---
            if action == "ADD":
                new_event_id = f"g_{uuid.uuid4().hex[:8]}"
                new_event = {
                    "id": new_event_id,
                    "name": mod_data["name"],
                    "start": mod_data["start"],
                    "end": mod_data["end"],
                    "category": mod_data["category"],
                }
                calendar_state[new_event_id] = new_event
                count_added += 1
                print(f"   + Added: {mod_data['name']}")

            # --- HANDLE RESCHEDULE ---
            elif action == "RESCHEDULE":
                target_id = mod_data.get("target_event_id")

                if target_id and target_id in calendar_state:
                    # Update times
                    calendar_state[target_id]["start"] = mod_data["start"]
                    calendar_state[target_id]["end"] = mod_data["end"]

                    if mod_data.get("name"):
                        calendar_state[target_id]["name"] = mod_data["name"]

                    count_updated += 1
                    print(f"   ~ Rescheduled: {mod_data['name']}")
                else:
                    print(
                        f"   ! Warning: Could not find event {target_id} to reschedule"
                    )

            # --- HANDLE REMOVE ---
            elif action == "REMOVE":
                target_id = mod_data.get("target_event_id")
                if target_id and target_id in calendar_state:
                    del calendar_state[target_id]
                    count_removed += 1
                    print(f"   - Removed: {mod_data.get('name', 'Unknown')}")

        print(
            f"[MOCK CALENDAR] Sync Complete. Added: {count_added}, Updated: {count_updated}, Removed: {count_removed}"
        )

        # 2. Return the values as a list of dicts
        final_event_list = list(calendar_state.values())

        # Optional: Sort by start time for cleanliness
        # Aseguramos que 'start' exista para evitar errores de sort
        final_event_list.sort(key=lambda x: x.get("start", ""))

        return final_event_list


class MockAnalysisService:
    @staticmethod
    def get_metrics(user_id: str):
        """
        Retorna la estructura exacta de análisis basada en tus datos históricos.
        Esto permite al agente saber que la productividad es alta en la mañana (4.5)
        y que las reuniones bajan el ánimo (3.6).
        """
        return {
            "analysis_date": "2025-11-09",
            "event_completion_stats": {
                "completed_percentage": 78.5,
                "missed_percentage": 15.7,
                "rescheduled_percentage": 5.8,
                "total_events_week": 32,
                "completed_events_week": 25,
            },
            "productivity_analysis": {
                "average_productivity_score": 4.1,
                "by_time_period": {"morning": 4.5, "afternoon": 3.8, "night": 3.2},
            },
            "mood_analysis": {
                "average_mood_score": 3.9,
                "by_event_type": {
                    "work": 4.2,
                    "meeting": 3.6,
                    "personal": 4.5,
                    "learning": 3.8,
                    "wellness": 4.0,
                },
            },
            "time_analysis": {
                "average_planned_time_by_day": {"Thursday": 6.2, "Friday": 3.8},
                "average_event_duration_minutes": 45.2,
            },
        }


class MockDatabaseService:
    @staticmethod
    def save_metrics(metrics: MetricsGenerationOutput, user_id: str):
        print(f"[MOCK DB] Métricas guardadas.")
        # [DBMetrics]
        return []

    @staticmethod
    def save_events(events: List[CalendarEvent], use):
        print(f"[MOCK DB] Eventos guardados.")
        # [DBEvent]
        return []


# class MockQueueService:
# @staticmethod
# def publish_schedule

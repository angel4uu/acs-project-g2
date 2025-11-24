from schemas import ExistingEvent


class MockCalendarService:
    @staticmethod
    def get_today_events(user_id: str):
        """Retorna eventos fijos simulados."""
        return [
            ExistingEvent(
                id="g_123",
                name="Reunión de Sincronización Semanal",
                start="2025-11-21T09:00:00Z",
                end="2025-11-21T09:30:00Z",
                category="MEETING",
            )
        ]

    @staticmethod
    def sync_changes(user_id, modifications):
        print(f"[MOCK CALENDAR] Sincronizando cambios en Google Calendar...")
        return True


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
    def get_event(event_id: str):
        return ExistingEvent(
            id=event_id,
            name="Deep Work Session",
            start="2025-11-21T10:00:00Z",
            end="2025-11-21T12:00:00Z",
            category="WORK",
        )

    @staticmethod
    def save_metrics(metrics):
        print(f"[MOCK DB] Métricas guardadas.")


class MockQueueService:
    @staticmethod
    def publish_schedule(user_id: str, daily_plan: dict):
        """
        Simula el envío de mensajes a RabbitMQ.
        Esto es lo que configuará los 'Workers' para despertar al agente
        cuando terminen los eventos.
        """
        print(f"[MOCK QUEUE] 📨 Publicando cronograma para el usuario {user_id}...")

        # Simulamos la lógica de extracción de eventos aprobados
        events_to_schedule = 0
        if "suggested_modifications" in daily_plan:
            # Contamos solo los que fueron aprobados/aceptados
            events_to_schedule = len(
                [
                    m
                    for m in daily_plan["suggested_modifications"]
                    if m.get("review_status") == "APPROVED" or m.get("approved") is True
                ]
            )

        print(
            f"[MOCK QUEUE] Se han encolado {events_to_schedule} triggers de seguimiento y recordatorios."
        )
        return True

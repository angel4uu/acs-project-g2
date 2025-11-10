def get_today_plan() -> dict:
    """
    Genera un plan diario personalizado para el usuario.
    Debe ser invocado cuando el usuario pida su plan para el día.
    Devuelve un objeto JSON que representa el plan.
    """
    print("\n[ADK Tool Executed]: get_today_plan()")

    return {
        "plan_date": "2025-11-09",
        "user_id": "abc123_adk",
        "today_summary": {
            "existing_events_count": 5,
            "suggested_new_events": 2,
            "expected_productivity_score": 4.4,
        },
        "recommendations": [
            "Move Deep Work earlier in the day for higher focus.",
            "Add short reflection breaks after intense sessions.",
        ],
        "summary_text": "Este plan fue generado por el Agente ADK. Tus tendencias de foco muestran un pico de productividad en la mañana.",
    }

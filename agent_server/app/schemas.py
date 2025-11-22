# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# --- 1. PLANNING AGENT SCHEMA ---


class ExistingEvent(BaseModel):
    """
    Schema for events currently fetched from Google Calendar.
    At this stage, they exist only in Google, so we use the Google ID.
    """

    id: str = Field(
        ..., description="The alphanumeric Google Calendar Event ID (e.g., '7n2...a')"
    )
    name: str = Field(..., description="Event summary/title")
    start: str = Field(
        ..., description="ISO 8601 Datetime (e.g., '2025-11-21T09:00:00Z')"
    )
    end: str = Field(..., description="ISO 8601 Datetime")
    category: Literal["WORK", "MEETING", "PERSONAL", "LEARNING", "WELLNESS"] = Field(
        ..., description="Inferred category based on title/calendar"
    )


class Modification(BaseModel):
    """Schema for each suggested modification in the Planning Agent's output."""

    temp_id: str = Field(..., description="Unique temporary ID (e.g., 'mod_1')")
    action: Literal["ADD", "RESCHEDULE", "REMOVE"]
    target_event_id: Optional[str] = Field(
        None, description="Google Event ID if rescheduling"
    )
    name: str
    start: str = Field(..., description="ISO 8601 Datetime string")
    end: str = Field(..., description="ISO 8601 Datetime string")
    category: Literal["WORK", "MEETING", "PERSONAL", "LEARNING", "WELLNESS"]
    reason_for_suggestion: str
    approved: bool = Field(False, description="Always False initially")


class DailyPlanOutput(BaseModel):
    """Schema for the Planning Agent's output."""

    plan_date: str
    daily_theme: str = Field(..., description="A short creative title for the day")
    motivational_quote: str
    original_schedule: List[ExistingEvent] = Field(
        ..., description="The exact list of Google Calendar events found, unaltered."
    )
    suggested_modifications: List[Modification]
    summary_text: str = Field(..., description="Natural language summary for the user")


# --- 2. INTERPRETER AGENT SCHEMA ---


class ModificationUpdate(BaseModel):
    """Schema for each modification update in the Feedback Interpreter Agent's output."""

    temp_id: str = Field(..., description="Must match a temp_id from the draft")
    status: Literal["APPROVED", "REJECTED", "MODIFIED"]
    new_start: Optional[str] = None
    new_end: Optional[str] = None


class FeedbackInterpretationOutput(BaseModel):
    """Schema for the Feedback Interpreter Agent's output."""

    modifications_updates: List[ModificationUpdate]


# --- 3. TRACKING AGENT SCHEMA ---


class TrackingMetricOutput(BaseModel):
    """Schema for the Tracking Agent's output."""

    event_id: str
    event_name: str
    completion_status: Literal["COMPLETED", "MISSED", "RESCHEDULED"]
    productivity_score: Optional[int] = Field(None, description="1-5 Scale")
    mood_score: Optional[int] = Field(None, description="1-5 Scale")
    actual_duration_minutes: Optional[int]
    user_comment: str

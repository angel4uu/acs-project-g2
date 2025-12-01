from google.adk.tools import ToolContext
from services.mocks import MockCalendarService, MockAnalysisService


def update_plan(tool_context: ToolContext):
    """
    Updates the daily plan based on the interpreted feedback.
    """
    # Retrieve state.
    plan = tool_context.state.get("today_plan_generation_output")
    feedback = tool_context.state.get("plan_feedback_interpretation_output")

    if not plan:
        return "Error: No active plan found in state. Please generate a plan first."
    if not feedback:
        return "Error: No feedback interpretation found. The interpreter agent may have failed."

    # Logic to Apply Updates
    changes_summary = []

    # Get the list of suggested modifications (Safely)
    suggestions = plan.get("suggested_modifications", [])

    # Get updates list safely from the feedback DICTIONARY
    updates_list = feedback.get("modifications_updates", [])

    # Iterate through the updates provided by the Interpreter
    for update in updates_list:
        update_temp_id = update.get("temp_id")
        update_status = update.get("status")
        new_start = update.get("new_start")
        new_end = update.get("new_end")

        found = False
        for mod in suggestions:
            # Match by temp_id
            if mod.get("temp_id") == update_temp_id:
                found = True

                if update_status == "APPROVED":
                    mod["review_status"] = "APPROVED"
                    changes_summary.append(
                        f"✅ Approved: {mod.get('category')} - {mod.get('name', 'Event')}"
                    )

                elif update_status == "REJECTED":
                    mod["review_status"] = "REJECTED"
                    changes_summary.append(f"❌ Rejected: {mod.get('name', 'Event')}")

                elif update_status == "MODIFIED":
                    mod["review_status"] = "APPROVED"  # Modified implies approval

                    if new_start:
                        mod["start"] = new_start
                    if new_end:
                        mod["end"] = new_end

                    changes_summary.append(
                        f"🔄 Rescheduled: {mod.get('name', 'Event')} to {new_start}"
                    )
                break

        if not found:
            # Handle case where AI hallucinated an ID
            changes_summary.append(
                f"⚠️ Warning: Could not find event ID {update.temp_id}"
            )

    # Save updated plan back to state
    tool_context.state["today_plan_generation_output"] = plan

    # Generate Result Summary
    pending_count = sum(1 for m in suggestions if m.get("review_status") == "PENDING")

    result_text = "\n".join(changes_summary)

    if pending_count > 0:
        return f"{result_text}\n\nThere are still {pending_count} pending suggestions. Ask the user about them."
    else:
        return f"{result_text}\n\nAll suggestions reviewed. The plan is ready to be finalized."

from datetime import datetime, date
from Models.TravelSearchState import TravelSearchState

def analyze_conversation_node(state: TravelSearchState) -> TravelSearchState:
    """Validate the information extracted by the LLM conversation node and craft targeted follow-up."""

    # Determine which fields are still missing or invalid
    missing_fields = []

    # Validate departure date
    departure_date = state.get("departure_date")
    if departure_date:
        try:
            parsed_date = datetime.strptime(departure_date, "%Y-%m-%d").date()
            if parsed_date < datetime.now().date():
                missing_fields.append("departure_date")
                state["departure_date"] = None
        except ValueError:
            missing_fields.append("departure_date")
            state["departure_date"] = None
    else:
        missing_fields.append("departure_date")

    # Validate origin and destination
    if not state.get("origin"):
        missing_fields.append("origin")
    if not state.get("destination"):
        missing_fields.append("destination")

    # Cabin class is optional for search; normalize step will default to ECONOMY if missing
    # Duration is optional; if missing we will search one-way or set return via duration if present
    
    # Decide completion
    core_complete = all(field not in missing_fields for field in ["departure_date", "origin", "destination"])

    if not core_complete:
        state["info_complete"] = False
        state["needs_followup"] = True

        # Generate a specific follow-up question if the LLM didn't provide one
        if not state.get("followup_question"):
            questions = []
            if "origin" in missing_fields and "destination" in missing_fields and "departure_date" in missing_fields:
                questions.append("What city are you flying from, where are you going, and on what date?")
            else:
                if "origin" in missing_fields:
                    questions.append("Which city are you flying from?")
                if "destination" in missing_fields:
                    questions.append("Which city would you like to fly to?")
                if "departure_date" in missing_fields:
                    questions.append("What is your departure date? (YYYY-MM-DD)")
            state["followup_question"] = " ".join(questions) or "Could you share your origin, destination, and departure date?"
    else:
        state["info_complete"] = True
        state["needs_followup"] = False
        state["followup_question"] = None
        # Default request type to flights so the graph can proceed
        state.setdefault("request_type", "flights")

    state["current_node"] = "analyze_conversation"
    return state

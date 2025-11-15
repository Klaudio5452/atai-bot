"""
Simple rule-based intent detection as an MVP.
You can later replace this with an LLM-based classifier.
"""
def detect_intent(text: str) -> str:
    t = (text or "").lower()
    if any(w in t for w in ["flight", "fly", "ticket", "airline", "departure", "pnr"]):
        return "search_flights"
    if any(w in t for w in ["hotel", "room", "stay", "accommodation"]):
        return "search_hotels"
    if any(w in t for w in ["expense", "receipt", "report", "claim"]):
        return "expense"
    if any(w in t for w in ["itinerary", "plan trip", "create trip"]):
        return "plan_itinerary"
    return "chat"

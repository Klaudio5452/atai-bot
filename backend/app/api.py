"""
ATAI API endpoints — fully wired.
"""
from fastapi import APIRouter, HTTPException
from .models import QueryRequest, BookingIn, ExpenseRequest
from .services.llm_client import LLMClient
from .services.rag import RAG
from .services.intent import detect_intent
from .services.amadeus_connector import AmadeusConnector
from .services.hotels_connector import HotelsConnector
from .services.bookings import BookingManager
from .services.expenses import ExpenseManager
from .data.sample_docs import SAMPLE_DOCS
from app.services.llm_client import LLMClient

import asyncio

router = APIRouter()

# ----------------------------------------------------------
# Initialize core services (load once at startup)
# ----------------------------------------------------------
llm = None
rag = None
amadeus = None
hotels = None
booking_mgr = None
expense_mgr = None

@router.on_event("startup")
async def startup_event():
    global llm, rag, amadeus, hotels, booking_mgr, expense_mgr

    try:
        llm = LLMClient()
    except Exception as e:
        print(f"[WARN] Could not init LLM client: {e}")
        llm = None

    rag = RAG(llm)
    rag.index_documents(SAMPLE_DOCS)

    amadeus = AmadeusConnector()
    hotels = HotelsConnector()
    booking_mgr = BookingManager(amadeus, hotels)
    expense_mgr = ExpenseManager()
    print("[ATAI] Services initialized")

# ----------------------------------------------------------
# Routes
# ----------------------------------------------------------

@router.get("/health")
async def health():
    return {"status": "ok", "service": "atai-bot-backend"}


# ------------------------------------------------------------------
#  QUERY ENDPOINT — main chat/AI endpoint
# ------------------------------------------------------------------
@router.post("/query")
async def query(req: QueryRequest):
    text = req.query.strip()
    role = req.role or "user"

    if not text:
        raise HTTPException(status_code=400, detail="Empty query")

    intent = detect_intent(text)
    print(f"[ATAI] Detected intent: {intent}")

    # fetch relevant docs via RAG
    retrieved_docs = rag.retrieve(text, top_k=3)
    rag_context = "\n".join(retrieved_docs)

    # placeholder result
    result = {
        "intent": intent,
        "response": None,
        "extra": {}
    }

    # handle by intent
    if intent == "search_flights":
        flights = await amadeus.search_flights(text)
        prompt = f"User role: {role}\nIntent: search_flights\nQuery: {text}\nContext:\n{rag_context}\nFlight options:\n{flights}\n\nGive a short summary."
        llm_text = llm.complete(prompt) if llm else "LLM not available."
        result["response"] = llm_text
        result["extra"]["flights"] = flights

    elif intent == "search_hotels":
        hotels_res = await hotels.search_hotels(text)
        prompt = f"User role: {role}\nIntent: search_hotels\nQuery: {text}\nContext:\n{rag_context}\nHotel options:\n{hotels_res}\n\nSummarize nicely."
        llm_text = llm.complete(prompt) if llm else "LLM not available."
        result["response"] = llm_text
        result["extra"]["hotels"] = hotels_res

    elif intent == "expense":
        prompt = f"User role: {role}\nIntent: expense\nQuery: {text}\nContext:\n{rag_context}\nGenerate guidance for expense management or report submission."
        llm_text = llm.complete(prompt) if llm else "LLM not available."
        result["response"] = llm_text
        result["extra"]["note"] = "Use /api/expense endpoint for full expense report upload."

    elif intent == "plan_itinerary":
        prompt = f"User role: {role}\nIntent: itinerary planning\nQuery: {text}\nContext:\n{rag_context}\nPlan a trip outline with flights, hotels, and possible activities."
        llm_text = llm.complete(prompt) if llm else "LLM not available."
        result["response"] = llm_text

    else:
        # general chat fallback
        prompt = f"User role: {role}\nIntent: general\nContext:\n{rag_context}\nUser query: {text}\nAnswer helpfully."
        llm_text = llm.complete(prompt) if llm else "LLM not available."
        result["response"] = llm_text

    return result


# ------------------------------------------------------------------
# BOOKING ENDPOINT
# ------------------------------------------------------------------
@router.post("/booking")
async def booking(req: BookingIn):
    try:
        res = await booking_mgr.create_booking(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------------
# EXPENSE ENDPOINT
# ------------------------------------------------------------------
@router.post("/expense")
async def expense(req: ExpenseRequest):
    try:
        res = expense_mgr.generate_report(req)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

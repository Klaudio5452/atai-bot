# app/models.py
from pydantic import BaseModel
from typing import List, Optional
from typing import Optional

class QueryRequest(BaseModel):
    query: str
    role: Optional[str] = "user"  # 👈 add this line


class BookingIn(BaseModel):
    origin: str
    destination: str
    date: str
    passengers: int = 1


class ExpenseItem(BaseModel):
    description: str
    amount: float


class ExpenseRequest(BaseModel):
    employee_id: str
    items: List[ExpenseItem]
    currency: Optional[str] = "EUR"

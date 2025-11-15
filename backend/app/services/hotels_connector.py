"""
Simple hotels connector (stub).
Later you can integrate Hotel APIs or channel managers.
"""
import asyncio

class HotelsConnector:
    def __init__(self):
        pass

    async def search_hotels(self, text_query: str):
        await asyncio.sleep(0.02)
        return [
            {"provider":"HotelX", "price": 120.0, "currency":"EUR", "details":{"name":"Hotel X Plaza","stars":4,"address":"Center"}},
            {"provider":"Booking-Stub", "price": 95.0, "currency":"EUR", "details":{"name":"City Budget","stars":3,"address":"Near station"}},
        ]

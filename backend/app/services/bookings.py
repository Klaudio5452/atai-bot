"""
Booking manager - MVP simulated booking flow.
Replace create_booking internals with real GDS/NDC PNR creation routines.
"""
import asyncio
from ..models import BookingIn
from typing import Dict

class BookingManager:
    def __init__(self, amadeus_connector=None, hotels_connector=None):
        self.amadeus = amadeus_connector
        self.hotels = hotels_connector

    async def create_booking(self, booking: BookingIn) -> Dict:
        # Validate minimal fields
        if not booking.passengers or not booking.segments:
            return {"status":"ERROR","message":"Missing passengers or segments"}

        # Simulate small async operation
        await asyncio.sleep(0.05)

        # Create a fake PNR based on first passenger
        first = booking.passengers[0]
        pnr = "PNR" + (first.last_name[:3].upper() if first.last_name else "XXX")
        return {
            "status": "CONFIRMED",
            "pnr": pnr,
            "booking_ref": "SIM" + pnr,
            "message": "Simulated booking created. Replace logic with real GDS/NDC calls."
        }

"""
Amadeus connector with safe stub fallback.

To enable real Amadeus:
 - install 'amadeus' package (already in requirements)
 - set use_real_amadeus = True
 - set AMA_CLIENT_ID and AMA_CLIENT_SECRET in env
 - implement call logic as shown in the comments
"""
import asyncio
import os

use_real_amadeus = False  # flip to True when you're ready + have credentials

if use_real_amadeus:
    from amadeus import Client, ResponseError

class AmadeusConnector:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("AMADEUS_API_KEY")
        if use_real_amadeus:
            client_id = os.getenv("AMADEUS_CLIENT_ID")
            client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
            if not (client_id and client_secret):
                raise RuntimeError("Set AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET in env to use real Amadeus.")
            self.client = Client(client_id=client_id, client_secret=client_secret)

    async def search_flights(self, text_query: str):
        """
        Returns list of dicts: {provider, price, currency, details}
        For now returns stub data. Replace with Amadeus SDK calls when ready.
        """
        await asyncio.sleep(0.02)
        if use_real_amadeus:
            # Example pseudocode—replace with actual SDK usage:
            # try:
            #     resp = self.client.shopping.flight_offers_search.get(params)
            #     parse response into our output format
            # except ResponseError as e:
            #     return []
            return []
        # stubbed example results
        return [
            {"provider":"Amadeus-EXAMPLE", "price": 420.0, "currency":"EUR", "details":{"route":"TIA-FCO","class":"Y","fare":"Q"}},
            {"provider":"NDC-Partner", "price": 510.0, "currency":"EUR", "details":{"route":"TIA-FRA","class":"B","fare":"M"}},
        ]

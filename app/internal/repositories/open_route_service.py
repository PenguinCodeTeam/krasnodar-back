from math import ceil

import httpx


OPEN_ROUTE_SERVICE_URL = 'https://api.openrouteservice.org/v2/directions/driving-car'


class OpenRouteServiceRepository:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def __params(self, start_point: str, end_point: str) -> dict:
        return {
            'api_key': self.api_key,
            'start': start_point,
            'end': end_point,
        }

    def convert_point_to_str(self, point: tuple):
        return ','.join(map(str, point))

    async def get_duration(self, start_point: tuple, end_point: tuple) -> float:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                OPEN_ROUTE_SERVICE_URL,
                params=self.__params(
                    start_point=self.convert_point_to_str(start_point),
                    end_point=self.convert_point_to_str(end_point),
                ),
            )
            data: dict = resp.json()
        features: dict = data.get('features', [{}])[0]
        properties: dict = features.get('properties', {})
        summary: dict = properties.get('summary', {})
        return int(ceil(summary.get('duration', -60) / 60))

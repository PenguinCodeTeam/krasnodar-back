from math import ceil

import httpx


GEOAPIFY_URL = 'https://api.geoapify.com/v1/routing'


class GeoapifyRepository:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def __params(self, start_point: str, end_point: str) -> dict:
        return {'apiKey': self.api_key, 'mode': 'drive', 'waypoints': f'{start_point}%7C{end_point}'}

    def convert_point_to_str(self, point: tuple):
        return '%2C'.join(map(str, point))

    async def get_duration(self, start_point: tuple, end_point: tuple) -> float:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                GEOAPIFY_URL,
                params=self.__params(self.convert_point_to_str(start_point), self.convert_point_to_str(end_point)),
            )
            data: dict = resp.json()
        features: dict = data.get('features', [{}])[0]
        properties: dict = features.get('properties', {})
        return int(ceil(properties.get('time', -60) / 60))

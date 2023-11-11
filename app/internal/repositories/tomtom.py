from math import ceil

import httpx


TOMTOM_URL = 'https://api.tomtom.com/routing/1/calculateRoute'


class TomTomRepository:
    def __init__(self, api_key: str):
        self.key = api_key

    def __params(self) -> dict:
        return {
            'key': self.key,
        }

    def convert_point_to_str(self, point: tuple):
        return ','.join(map(str, point))

    async def get_duration(self, start_point: tuple, end_point: tuple) -> float:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                TOMTOM_URL + f'/{self.convert_point_to_str(start_point)}:{self.convert_point_to_str(end_point)}/json',
                params=self.__params(),
            )
            data: dict = resp.json()
        routes: dict = data.get('routes', [{}])[0]
        summary: dict = routes.get('summary', {})
        return int(ceil(summary.get('travelTimeInSeconds', -60) / 60))

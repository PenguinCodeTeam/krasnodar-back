import httpx


OPEN_ROUTE_SERVICE_REPOSITORY = "https://api.openrouteservice.org/v2/directions/driving-car"


class OpenRouteServiceRepository:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def __params(self, start_point: str, end_point: str) -> dict:
        return {
            "api_key": self.api_key,
            "start": start_point,
            "end": end_point,
        }

    def convert_point_to_str(self, point: tuple):
        return ','.join((lambda point: (str(point[0]), str(point[1])))(point))

    async def get_duration(self, start_point: str, end_point: str) -> float:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                OPEN_ROUTE_SERVICE_REPOSITORY,
                params=self.__params(
                    start_point=self.convert_point_to_str(start_point),
                    end_point=self.convert_point_to_str(end_point),
                ),
            )
            data: dict = resp.json()
        features: dict = data.get("features", [{}])[0]
        properties: dict = features.get("properties", {})
        summary: dict = properties.get("summary", {})
        return summary.get("duration", -1)

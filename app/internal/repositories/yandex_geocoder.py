import httpx


class YandexGeocoderRepository:
    def __init__(self, api_key: str):
        self.api_url = "https://geocode-maps.yandex.ru/1.x"
        self.api_key = api_key

    def __params(self, city: str, address: str) -> dict:
        return {
            "apikey": self.api_key,
            "geocode": f"{city}, {address}",
            "format": "json",
            "results": 1,
        }

    async def get_coordinates(self, city: str, address: str) -> tuple[float] | None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                self.api_url,
                params=self.__params(city=city, address=address),
            )
            data: dict = resp.json()
        response: dict = data.get("response", {})
        geo_object_collection: dict = response.get("GeoObjectCollection", {})
        feature_member: dict = geo_object_collection.get("featureMember", [{}])[0]
        geo_object: dict = feature_member.get("GeoObject", {})
        point: dict = geo_object.get("Point", {})
        pos: str | None = point.get("pos", None)
        return tuple(map(float, pos.split())) if pos else None

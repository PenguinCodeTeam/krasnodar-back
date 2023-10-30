from fastapi.exceptions import HTTPException

from internal.services.authentication.jwt import encode_jwt


class AuthenticationService:
    async def login_service(self, login: str, password: str) -> dict:
        """Logins the user and returns generated token"""
        if login == 'test' and password == 'test':
            return {'access_token': f'{encode_jwt(login)}', 'role': 'manager'}
        raise HTTPException(status_code=401, detail='Invalid credentials')

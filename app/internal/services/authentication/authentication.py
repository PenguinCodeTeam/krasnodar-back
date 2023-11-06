from fastapi.exceptions import HTTPException

from internal.core.utils import check_password
from internal.repositories.db.users import UserRepository
from internal.services.authentication.jwt import encode_jwt


class AuthenticationService:
    def __init__(self):
        self.repository = UserRepository()

    async def login_service(self, login: str, password: str) -> dict:
        """Авторизация пользователя, возвращение сгенерированного токена, фио, роли и uuid"""
        if user := await self.repository.get_user(login=login):
            if check_password(password, user.password_hash):
                user_id = user.id
                return {
                    'access_token': encode_jwt(user_id),
                    'name': user.name,
                    'surname': user.surname,
                    'patronymic': user.patronymic,
                    'role': user.role,
                    'id': user_id,
                }
        raise HTTPException(status_code=401, detail='Invalid credentials')

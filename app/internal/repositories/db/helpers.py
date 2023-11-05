import config
from passlib.context import CryptContext
from sqlalchemy import URL


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


connection_string = URL.create(
    drivername='postgresql+asyncpg',
    username=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    database=config.POSTGRES_DB,
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
)

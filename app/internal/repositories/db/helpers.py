from sqlalchemy import URL

import config


connection_string = URL.create(
    drivername='postgresql+asyncpg',
    username=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    database=config.POSTGRES_DB,
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
)

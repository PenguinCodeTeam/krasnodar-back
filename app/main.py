from os import cpu_count

import uvicorn

import config
from config.logging import LOGGING


def main():
    uvicorn.run(
        'initializer:create_app',
        factory=True,
        access_log=True,
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        log_config=LOGGING,
        reload=config.DEV,
        workers=cpu_count(),
    )


if __name__ == '__main__':
    main()

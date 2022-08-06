
import os
from typing import List

from pydantic import BaseSettings

from app import logging_


logger = logging_.get_logger(__file__)


class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_password: str
    db_host: str
    db_user: str
    db_password: str
    db_name: str

    class Config:
        env_file = '.env'


FASTAPI_APP_ENV = os.getenv('FASTAPI_APP_ENV', default='dev')
settings = Settings(_env_file=f'{FASTAPI_APP_ENV}.env')
logger.info(f'{FASTAPI_APP_ENV=}')


class EngineeringCenterProfile(BaseSettings):
    name: str = 'Hanyang University Engineering Center'
    x_actual: float = 73.85
    y_actual: float = 28.21
    lat0: float = 37.555155
    lon0: float = 127.046074
    bearing: float = 103.79971366339193
    cell_size: float = 1.5
    n_col: int = 49
    n_row: int = 18
    floors: List = [2, 3, 4, 5, 6, 7]
    aisle: List = [(7, col) for col in range(n_col)] + \
                  [(8, col) for col in range(n_col)]


# if __name__ == '__main__':
#     x = EngineeringCenterProfile().x_actual
#     y = EngineeringCenterProfile().y_actual
#     cell_size = EngineeringCenterProfile().cell_size
#     print(x // cell_size)
#     print(y // cell_size)

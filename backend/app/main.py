from fastapi import FastAPI
from core import config

from functools import lru_cache


@lru_cache
def get_settings():
    return config.Settings()  # type: ignore


app = FastAPI()

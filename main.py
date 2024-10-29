from fastapi import FastAPI

from data import setup_database, setup_environment

setup_environment()
setup_database()

app = FastAPI()

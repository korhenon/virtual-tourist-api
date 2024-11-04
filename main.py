from fastapi import FastAPI

from data import setup_environment
from data.database import setup_database
from router.auth.router import router as auth
from router.author.router import router as author
from router.files.router import router as files
from router.user.router import router as user

setup_environment()
setup_database()

app = FastAPI()

app.include_router(auth)
app.include_router(author)
app.include_router(user)
app.include_router(files)

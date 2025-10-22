from fastapi import FastAPI
from .routes import strings

app = FastAPI()

app.include_router(strings.router)
#app.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import routes

app = FastAPI()
app.include_router(routes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


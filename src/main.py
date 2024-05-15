from fastapi import FastAPI

from src.controllers import user_controller
from src.database.connection import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_controller.router)

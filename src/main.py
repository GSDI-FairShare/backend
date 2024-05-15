from fastapi import FastAPI

from src.controllers import user_controllers
from src.controllers import auth_controllers
from src.database.connection import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_controllers.router)
app.include_router(auth_controllers.router)

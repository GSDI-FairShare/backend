from fastapi import FastAPI

# from src.controllers import user_controllers
from src.controllers import auth_controllers
from src.controllers import individual_expenses_controllers
from src.database.connection import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shared Expenses Manager API",
    description="API for managing individual and shared expenses between friends or family members.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Auth", "description": "Operations with authentication"},
        {
            "name": "Individual Expenses",
            "description": "Operations with individual expenses",
        },
    ],
)

# app.include_router(user_controllers.router)
app.include_router(auth_controllers.router)
app.include_router(individual_expenses_controllers.router)

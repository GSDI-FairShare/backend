from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from src.controllers import user_controllers
from src.controllers import (
    auth_controllers,
    group_controllers,
    individual_expenses_controllers,
)
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

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.include_router(user_controllers.router)
app.include_router(auth_controllers.router)
app.include_router(individual_expenses_controllers.router)
app.include_router(group_controllers.router)

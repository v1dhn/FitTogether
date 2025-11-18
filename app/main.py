from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import Base, engine
from app.routers import users, workouts


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    Base.metadata.create_all(bind=engine)
    print("Database initialized")

    yield

    # Shutdown code (optional)
    print("App shutting down")


def create_app() -> FastAPI:
    app = FastAPI(title="FitTogether", lifespan=lifespan)

    app.include_router(users.router)
    app.include_router(workouts.router)

    return app


app = create_app()
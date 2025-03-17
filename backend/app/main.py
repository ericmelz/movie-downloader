import uvicorn as uvicorn
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    @property
    def database_url(self):
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()

Base = declarative_base()

engine = create_async_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Report(Base):
    __tablename__ = "movie_reports"

    id = Column(String(50), primary_key=True, index=True)
    ready = Column(Boolean, default=False)
    file_path = Column(String(100))


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(on_startup=[init_models])


@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI!!"}


def main():
    """Entry point for running the FastAPI application."""
    uvicorn.run("fastapi_app.main:app", host="0.0.0.0", port=8005, reload=True)

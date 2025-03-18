from uuid import uuid4

import uvicorn as uvicorn
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic_settings import BaseSettings
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio
import os


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    movies_dir: str
    report_output_dir: str

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


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def generate_report_task(report_id: str):
    # TODO add logging, test with errors (e.g., missing dir)
    await asyncio.sleep(5)  # Simulate a long-running task
    report_path = f'{settings.report_output_dir}/{report_id}.pdf'
    print(f'writing to {report_path}')
    with open(report_path, 'w') as f:
        f.write('This is your generated report')
    async with SessionLocal() as db:
        report = await db.get(Report, report_id)
        report.ready = True
        report.file_path = report_path
        # TODO add generated_at timestamp
        await db.commit()


@app.post("/generate")
async def generate_report(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    report_id = "report_" + str(uuid4())
    new_report = Report(id=report_id, ready=False)
    # TODO add requested_at timestamp
    db.add(new_report)
    await db.commit()
    background_tasks.add_task(generate_report_task, report_id)
    return {"report_id": report_id}


@app.get("/{report_id}/status")
async def report_status(report_id: str, db: AsyncSession = Depends(get_db)):
    report = await db.get(Report, report_id)
    if report:
        return {"ready": report.ready, "url": f"/{report_id}" if report.ready else None}
    raise HTTPException(status_code=404, detail="Report not found")


@app.get("/{report_id}")
async def get_report(report_id:str, db: AsyncSession = Depends(get_db)):
    report = await db.get(Report, report_id)
    if report and report.ready and os.path.exists(report.file_path):
        # TODO hack for development
        report.file_path = '/Users/ericmelz/Desktop/Eric Melz.pdf'
        # TODO maybe: use timestamp instead of hardcoded name
        return FileResponse(report.file_path, media_type="application/pdf", filename="{timestamp} movie report.pdf")
    raise HTTPException(status_code=404, detail="Report not found or not ready")


@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI!!"}


def main():
    """Entry point for running the FastAPI application."""
    uvicorn.run("fastapi_app.main:app", host="0.0.0.0", port=8005, reload=True)

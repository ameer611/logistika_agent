from fastapi import FastAPI
from app.routers import zapros_router
from app.database import engine
from app.models import Base
from app.seed import run_database_seeder

Base.metadata.create_all(bind=engine)

run_database_seeder()

app = FastAPI(
    title="AI Cargo Matching System",
    version="1.0.0"
)

app.include_router(zapros_router.router)

@app.get("/")
def health_check():
    return {"status": "healthy"}
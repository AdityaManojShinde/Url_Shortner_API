from fastapi import FastAPI
from datetime import datetime
from app.api.v1 import url_shortner
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.session import create_db_and_tables



@asynccontextmanager
async def lifecyle(app: FastAPI):
    create_db_and_tables()
    print("Database initialized.")
    yield

app = FastAPI(
    title="Url Shortner",
    lifespan=lifecyle,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_shortner.router)


@app.get("/")
def root():
    return {
        "message": "Api running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/{short_code}")
def get_shorten_url(short_code: str):
    return {"msg": short_code}
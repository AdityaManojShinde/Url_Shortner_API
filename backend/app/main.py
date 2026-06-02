from fastapi import FastAPI
from datetime import datetime

from app.api.v1 import url_shortner
from app.api.v1 import auth

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.session import create_db_and_tables, DBSession
from app.db.schema import ShortUrl
from sqlmodel import select
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError




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
        "http://127.0.0.1:3000",
        "https://project-97nl0.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(url_shortner.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {
        "message": "Api running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/r/{short_code}")
def get_shorten_url(
    short_code: str,
    db_session: DBSession,
):
    
    try: 
        record = db_session.exec(
            select(ShortUrl).where(
                ShortUrl.short_code == short_code
            )
        ).first()

        
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )
    
    if record is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
            )

    return RedirectResponse(
        url=record.url,
        status_code=307,
    )
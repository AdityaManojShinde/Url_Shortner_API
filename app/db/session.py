from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated
from fastapi import Depends
from app.db.schema import User, ShortUrl

DATABASE_URL: str = "sqlite:///database.db"
engine_kwargs = {}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {
        "check_same_thread": False
    }
engine = create_engine(
    DATABASE_URL,
    **engine_kwargs
    )

def get_db_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# db session dependency injection
DBSession = Annotated[Session, Depends(get_db_session())]

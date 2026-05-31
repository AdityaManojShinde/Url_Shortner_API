from fastapi import APIRouter, Request
from app.models.shortner_models import ShortnerReq, ShortnerRes
from app.services.url_shortner import shorten_url
from app.db.session import DBSession
from app.db.schema import ShortUrl



router = APIRouter(
    prefix="/shortner",
    tags=["Url Shortner"]
)


@router.get("/")
def shortner_root():
    return {
        "message": "url shortner api"
    }


"""
TODO: 
- check if unique short code already exits in db []
- store short code in db []
- return short code url []

create schema 
create db session
apply it
"""
@router.post("/")
def create_shorten_url(
    payload: ShortnerReq, 
    request: Request,
    db_session: DBSession
    ) -> ShortnerRes:
    response = shorten_url(url=payload.url, req=request, db=db_session)
    return response
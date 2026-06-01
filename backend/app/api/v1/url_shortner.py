from fastapi import APIRouter, Request
from app.models.shortner_models import ShortnerReq, ShortnerRes
from app.services.url_shortner import shorten_url
from app.db.session import DBSession



router = APIRouter(
    prefix="/shortner",
    tags=["Url Shortner"]
)


@router.get("/")
def shortner_root():
    return {
        "message": "url shortner api"
    }

@router.post("/")
def create_shorten_url(
    payload: ShortnerReq, 
    request: Request,
    db_session: DBSession
    ) -> ShortnerRes:
    response = shorten_url(url=payload.url, req=request, db=db_session)
    return response
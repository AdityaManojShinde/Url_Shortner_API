from fastapi import APIRouter, Request

from app.db.session import DBSession
from app.models.shortner_models import ShortnerReq, ShortnerRes
from app.services.auth_service import CurrentUserOptional
from app.services.url_shortner import shorten_url


router = APIRouter(
    prefix="/shortner",
    tags=["Url Shortner"]
)


@router.get("/")
def shortner_root():
    return {
        "message": "url shortner api"
    }


@router.post("/", response_model=ShortnerRes)
def create_shorten_url(
    payload: ShortnerReq,
    request: Request,
    db_session: DBSession,
    user: CurrentUserOptional
) -> ShortnerRes:

    response = shorten_url(
        url=payload.url,
        req=request,
        db=db_session,
        user=user
    )

    return response
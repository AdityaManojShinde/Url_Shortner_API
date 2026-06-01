from fastapi import APIRouter, Request
from sqlmodel import select

from app.db.schema import ShortUrl
from app.db.session import DBSession
from app.models.shortner_models import (
    ShortnerReq,
    ShortnerRes,
)
from app.models.urls import UserUrlsResponse
from app.services.auth_service import (
    CurrentUser,
    CurrentUserOptional,
)
from app.services.url_shortner import (
    shorten_url,
    get_user_urls
)


router = APIRouter(
    prefix="/shortner",
    tags=["Url Shortner"]
)


@router.get("/", response_model=UserUrlsResponse)
def get_urls(
    db_session: DBSession,
    user: CurrentUser,
):
    return get_user_urls(
        user=user,
        db=db_session
    )


@router.post("/", response_model=ShortnerRes)
def create_shorten_url(
    payload: ShortnerReq,
    request: Request,
    db_session: DBSession,
    user: CurrentUserOptional,
) -> ShortnerRes:

    return shorten_url(
        url=payload.url,
        req=request,
        db=db_session,
        user=user,
    )
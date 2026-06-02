from fastapi import APIRouter
from app.db.session import DBSession
from app.models.auth import (
    SignUpUserReq,
    SignUpUserRes,
    LoginUserReq,
    LoginUserRes
)
from app.services.auth_service import (
    auth_service,
    CurrentUser
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/me")
def get_user(
    user: CurrentUser
):
    return {
        "id": str(user.id),
        "email": user.email,
        "created_at": user.created_at
    }


@router.post(
    "/signup",
    response_model=SignUpUserRes,
    status_code=201
)
def signup_user(
    user: SignUpUserReq,
    db: DBSession
) -> SignUpUserRes:

    created_user = auth_service.signup(
        email=user.email,
        password=user.password,
        db=db
    )

    return SignUpUserRes(
        email=created_user.email
    )


@router.post(
    "/login",
    response_model=LoginUserRes
)
def login_user(
    db: DBSession,
    form_data: LoginUserReq
) -> LoginUserRes:

    return auth_service.login(
        email=form_data.email,
        password=form_data.password,
        db=db
    )
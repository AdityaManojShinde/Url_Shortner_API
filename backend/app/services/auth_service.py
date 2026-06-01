import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlmodel import select
from uuid import UUID

from app.db.schema import User
from app.db.session import DBSession
from app.models.auth import LoginUserRes

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not configured")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False
)


class AuthService:
    def __init__(self):
        self._pwd_hash = PasswordHash.recommended()

    def signup(
        self,
        email: str,
        password: str,
        db: DBSession
    ) -> User:

        existing_user = db.exec(
            select(User).where(User.email == email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user = User(
            email=email,
            password_hash=self.get_password_hash(password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def login(
        self,
        email: str,
        password: str,
        db: DBSession
    ) -> LoginUserRes:

        user = db.exec(
            select(User).where(User.email == email)
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not self.verify_password(
            plain_password=password,
            hashed_password=user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        payload = {
            "sub": str(user.id),
            "exp": datetime.now(timezone.utc)
            + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        }

        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return LoginUserRes(
                access_token=token,
                token_type="bearer"
             )

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str
    ) -> bool:
        return self._pwd_hash.verify(
            plain_password,
            hashed_password
        )

    def get_password_hash(
        self,
        password: str
    ) -> str:
        return self._pwd_hash.hash(password)

    def decode_token(
        self,
        token: str
    ) -> dict:
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            return payload

        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


auth_service = AuthService()


def get_current_user(
    db: DBSession,
    token: str = Depends(oauth2_scheme)
) -> User:

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    payload = auth_service.decode_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.get(User, user_uuid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


def get_current_user_optional(
    db: DBSession,
    token: str | None = Depends(oauth2_scheme)
) -> User | None:

    if not token:
        return None

    try:
        payload = auth_service.decode_token(token)

        user_id = payload.get("sub")

        if not user_id:
            return None

        return db.get(
            User,
            UUID(user_id)
        )

    except (HTTPException, ValueError):
        return None 

CurrentUser = Annotated[User,Depends(get_current_user)]
CurrentUserOptional = Annotated[User | None, Depends(get_current_user_optional)]
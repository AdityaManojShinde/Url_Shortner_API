import secrets

from fastapi import Request
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.db.schema import ShortUrl
from app.db.session import DBSession
from app.models.shortner_models import ShortnerRes


def generate_short_code() -> str:
    """Generate a random short code."""
    return secrets.token_urlsafe(6)


def short_code_exists(
    short_code: str,
    db: DBSession,
) -> bool:
    """Check whether a short code already exists."""
    existing = db.exec(
        select(ShortUrl).where(
            ShortUrl.short_code == short_code
        )
    ).first()

    return existing is not None


def get_unique_short_code(
    db: DBSession,
) -> str:
    """Generate a unique short code."""
    while True:
        short_code = generate_short_code()

        if not short_code_exists(
            short_code=short_code,
            db=db,
        ):
            return short_code


def build_short_url(
    short_code: str,
    req: Request,
) -> str:
    """Build the public short URL."""
    return (
        str(req.base_url).rstrip("/")
        + "/"
        + short_code
    )


def save_short_url(
    url: str,
    short_code: str,
    db: DBSession,
) -> ShortUrl:
    """Persist URL mapping to database."""

    try:
        record = ShortUrl(
            user_id=None,
            url=url,
            short_code=short_code,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    except IntegrityError:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise


def shorten_url(
    url: str,
    req: Request,
    db: DBSession,
) -> ShortnerRes:
    """Create and store a shortened URL."""

    short_code = get_unique_short_code(db)

    data = save_short_url(
        url=url,
        short_code=short_code,
        db=db,
    )

    short_url = build_short_url(
        short_code=short_code,
        req=req,
    )

    return ShortnerRes(
        id=data.id,
        url=url,
        short_code=short_code,
        short_url=short_url,
    )
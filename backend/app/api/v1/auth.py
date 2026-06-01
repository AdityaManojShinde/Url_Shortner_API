from fastapi import APIRouter


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/me")
def get_user():
    pass

@router.post("/signup")
def signup_user():
    pass

@router.post("/login")
def login_user():
    pass
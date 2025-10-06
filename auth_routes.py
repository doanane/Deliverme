from fastapi import APIRouter, HTTPException, status, Depends
from database import SessionLocal  # engine
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from schemas import SignUpModel
from models import User

auth_router = APIRouter(prefix="/auth", tags=["auths"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_router.post("/", status_code=status.HTTP_201_CREATED)
async def signup(sign: SignUpModel, db: Session = Depends(get_db)):
    user_email = db.query(User).filter(User.email == sign.email).first()
    if user_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_username = db.query(User).filter(User.username == sign.username).first()
    if user_username:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Create a new user
    new_user = User(
        username=sign.username,
        email=sign.email,
        password=generate_password_hash(sign.password),
        is_staff=sign.is_staff,
        is_active=sign.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


@auth_router.get("/")
async def create_auth():
    return {"message: usermessage"}

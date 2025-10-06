from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from jwt_utils import create_access_token, create_refresh_token, verify_token

auth_router = APIRouter(prefix="/auth", tags=["auth"])


# Signup Route (unchanged)
@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(signup_data: SignUpModel, db: Session = Depends(get_db)):
    # Check if email exists
    user_email = db.query(User).filter(User.email == signup_data.email).first()
    if user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check if username exists
    user_username = db.query(User).filter(User.username == signup_data.username).first()
    if user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Create new user
    new_user = User(
        username=signup_data.username,
        email=signup_data.email,
        password=generate_password_hash(signup_data.password),
        is_staff=signup_data.is_staff,
        is_active=signup_data.is_active,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Login Route - UPDATED to accept username OR email
@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(login_data: LoginModel, db: Session = Depends(get_db)):
    # Find user by either username OR email
    db_user = (
        db.query(User)
        .filter(
            (User.username == login_data.username_or_email)
            | (User.email == login_data.username_or_email)
        )
        .first()
    )

    # Check if user exists and password is correct
    if not db_user or not check_password_hash(db_user.password, login_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username/email or password",
        )

    # Check if user account is active
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User account is inactive"
        )

    # Create tokens
    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_refresh_token(data={"sub": db_user.username})

    response = {
        "access": access_token,
        "refresh": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
        },
    }

    return jsonable_encoder(response)


# Refresh Token Route (unchanged)
@auth_router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    new_access_token = create_access_token(data={"sub": username})

    return {"access": new_access_token, "token_type": "bearer"}


# Protected Route Example (unchanged)
@auth_router.get("/profile")
async def get_profile(token: str):
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    username = payload.get("sub")
    return {"message": f"Hello {username}", "user": username}

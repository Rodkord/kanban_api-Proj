from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt

from database.database import SessionLocal
from database.models import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"


class RegisterRequest(BaseModel):

    username: str
    email: str
    password: str


@router.post("/register")
def register(data: RegisterRequest):

    db: Session = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:

        db.close()

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(
        data.password
    )

    user = User(
        username=data.username,
        email=data.email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {
        "message": "User registered successfully",
        "user_id": user.id
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    db: Session = SessionLocal()

    # Swagger sends the email through the username field
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:

        db.close()

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_correct = pwd_context.verify(
        form_data.password,
        user.password
    )

    if not password_correct:

        db.close()

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = jwt.encode(
        {
            "user_id": user.id,
            "email": user.email
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    db.close()

    return {
        "access_token": token,
        "token_type": "bearer"
    }
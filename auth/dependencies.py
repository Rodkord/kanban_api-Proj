from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database.database import SessionLocal
from database.models import User


SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    db: Session = SessionLocal()

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    db.close()


    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    return user
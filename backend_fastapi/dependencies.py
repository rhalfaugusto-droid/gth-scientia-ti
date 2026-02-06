from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os

from backend_fastapi import database, crud


SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_change")
ALGORITHM = "HS256"


class CurrentUser(BaseModel):
    id: int
    email: str
    name: str | None = None


def get_current_user(
    request: Request,
    db: Session = Depends(database.get_db),
) -> CurrentUser:
    """
    Extracts JWT from Authorization header and returns authenticated user.
    Raises 401 for any authentication failure.
    """

    auth_header = request.headers.get("authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = auth_header.removeprefix("Bearer ").strip()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")

        if not email:
            raise ValueError("Token missing subject")

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = crud.get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return CurrentUser(
        id=user.id,
        email=user.email,
        name=user.name,
    )

from sqlalchemy.orm import Session

from app.repositories.user_repository import get_user_by_email
from app.core.security import verify_password
from app.models.user import User


class AuthenticationError(Exception):
    pass


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> User:
    user = get_user_by_email(db, email)

    if not user:
        raise AuthenticationError("Invalid credentials")

    if not user.is_active:
        raise AuthenticationError("Inactive user")

    if not verify_password(password, user.password_hash):
        raise AuthenticationError("Invalid credentials")

    return user

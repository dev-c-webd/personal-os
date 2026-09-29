from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.modules.auth.schemas import LoginRequest
from app.modules.users.models import User
from app.modules.auth.schemas import UserRegister

"""
# FLOW

registration data
      ↓
check username/email
      ↓
hash password
      ↓
create User object
      ↓
db.add()
      ↓
db.commit()
      ↓
db.refresh()
      ↓
return User
"""

def register_user(data: UserRegister, db: Session) -> User:

    # getting the user from the db to check if the user(the one registering) already exists
    existing_user = db.scalar(
        select(User).where(
            or_(
                User.username == data.username,
                User.email == data.email,
            )
        )
    )

    if existing_user:
        if existing_user.username == data.username:
            raise ValueError("Username already exists")
        
        raise ValueError("Email already exists")

    user = User(
        username = data.username,
        email = data.email,
        password_hash = hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(data: LoginRequest, db: Session) -> User | None:

    user = db.scalar(
        select(User).where(
            or_(
                User.username == data.identifier,
                User.email == data.identifier,
            )
        )
    )

    if not user:
        return None

    if not verify_password(data.password, user.password_hash):
        return None

    return user

def create_login_token(user: User) -> str:
    return create_access_token(str(user.id))

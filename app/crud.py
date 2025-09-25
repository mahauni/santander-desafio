from typing import Any
from sqlmodel import Session


def authenticate(*, session: Session, email: str, password: str) -> Any | None:
    #    if not db_user:
    #        return None
    #    if not verify_password(password, db_user.hashed_password):
    #        return None
    return Any

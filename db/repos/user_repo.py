import hashlib
import typing

import sqlalchemy as sa
from sqlalchemy.orm import Session

from config.app_config import DevelopmentCfg
from db.models.user import Users
from db.role import check_is_valid_role
from api.validators.users_requests_validation import _validate_password


def hash_user_password(pwd: str) -> str:
    salt = DevelopmentCfg.SALT.encode()

    pwd_hashed = hashlib.sha256(pwd.encode() + salt)
    return pwd_hashed.hexdigest()


def get_user_by_id(session: Session, user_pk: int) -> dict:
    user: Users = session.get(Users, user_pk)

    if user:
        return user.to_json()
    else:
        return {"error": "Authentication error"}


def get_user(session: Session, login: str, password: str) -> typing.Union[Users, dict]:
    req = sa.select(Users).where(Users.login == login)
    user: Users = session.scalar(req)

    if user and user.password == hash_user_password(password):
        return user
    else:
        return {"error": "Authentication error"}


def add_user(session: Session, name: str, login: str, password: str, role: str):
    pwd = hash_user_password(password)

    if all([name, login, password, role]) and isinstance(get_user(session, login, password), dict):
        if check_is_valid_role(role):
            user = Users(name=name, login=login, password=pwd, role=role)
            session.add(user)

            session.commit()

            return user
        else:
            return {"error": "Invalid role, only 'admin' or 'owner'"}
    else:
        return {"error": "Sign up error, check data"}


def change_password(session, user_id: int, previous_pwd: str, new_pwd: str):
    user = session.get(Users, user_id)

    if user.password == hash_user_password(previous_pwd):
        result = _validate_password(new_pwd)

        if result.get("error"):
            return result

        user.password = hash_user_password(new_pwd)

        session.commit()
        return {}
    else:
        return {"error": "Invalid previous password"}

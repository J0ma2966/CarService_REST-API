import typing
import hashlib
from datetime import datetime, timezone, timedelta

import jwt
import sqlalchemy as sa
from sqlalchemy.orm import Session, relationship

from db.models import BaseModel
from db.role import UserRole, check_is_valid_role
from config.app_config import DevelopmentCfg


class Users(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    login = sa.Column(sa.String, unique=True)
    password = sa.Column(sa.String)
    role = sa.Column(sa.Enum(UserRole))

    wash_company_id = sa.Column(sa.BigInteger, sa.ForeignKey('wash_companies.id'))

    reg_date = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())

    def __repr__(self):
        return f"User\n{self.username=}"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "login": self.login,
            "password": self.password,
            "wash_company_id": self.wash_company_id,
            "role": self.role.value
        }

    def encode_access_token(self):
        alive = datetime.now(timezone.utc) + timedelta(DevelopmentCfg.TOKEN_EXPIRE)
        payload = dict(exp=alive, user=self.id)
        key = DevelopmentCfg.SECRET_KEY
        return jwt.encode(payload, key, algorithm="HS256").encode()


def hash_user_password(pwd: str) -> str:
    salt = DevelopmentCfg.SALT.encode()

    pwd_hashed = hashlib.sha256(pwd.encode() + salt)
    return pwd_hashed.hexdigest()


def get_user_by_id(session: Session, user_pk: int) -> typing.Union[Users, dict]:
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

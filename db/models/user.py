from datetime import datetime, timezone, timedelta

import jwt
import sqlalchemy as sa

from config.app_config import DevelopmentCfg
from db.models import BaseModel
from db.role import UserRole


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

import sqlalchemy as sa

from db.models import BaseModel
from db.role import UserRole


class Users(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    login = sa.Column(sa.String, unique=True)
    password = sa.Column(sa.String)
    role = sa.Column(sa.Enum(UserRole))

    reg_date = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())

    def __repr__(self):
        return f"User\n{self.username=}"

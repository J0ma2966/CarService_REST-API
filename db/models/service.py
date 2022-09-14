import sqlalchemy as sa

from db.models import BaseModel


class Service(BaseModel):
    __tablename__ = "services"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    duration = sa.Column(sa.Integer)
    price = sa.Column(sa.Integer)

    def __repr__(self):
        return f"Service\n{self.name=}"

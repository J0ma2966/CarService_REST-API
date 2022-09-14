import sqlalchemy as sa

from db.models import BaseModel


class Washer(BaseModel):
    __tablename__ = "washer"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    phone_number = sa.Column(sa.BigInteger)
    stake = sa.Column(sa.Integer)
    image = sa.Column(sa.LargeBinary, nullable=True)
    is_active = sa.Column(sa.Boolean, default=True)

    def __repr__(self):
        return f"Washer\n{self.name=}"

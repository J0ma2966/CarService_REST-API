import sqlalchemy as sa

from db.models import BaseModel


class WashCompany(BaseModel):
    __tablename__ = "wash_company"

    id = sa.Column(sa.BigInteger, primary_key=True)
    name = sa.Column(sa.String)
    avatar = sa.Column(sa.)
    location = sa.Column(sa.String)

    def __repr__(self):
        return f"WashCompany\n{self.name=}"

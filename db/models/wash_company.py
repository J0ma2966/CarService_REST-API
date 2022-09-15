import typing

import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.orm import relationship

from db.models import BaseModel


class WashCompany(BaseModel):
    __tablename__ = "wash_companies"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    avatar = sa.Column(sa.LargeBinary, nullable=True)
    location = sa.Column(sa.String)

    orders = relationship('Order', backref='wash_company')
    users = relationship('Users', backref='wash_company')
    washers = relationship('Washer', backref='wash_company')
    services = relationship('Service', backref='wash_company')
    journals = relationship('Journal', backref='wash_company')

    def __repr__(self):
        return f"WashCompany\n{self.name=}"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "orders": [order.to_json() for order in self.orders],
            "users": [user.to_json() for user in self.users],
            "washers": [washer.to_json() for washer in self.washers],
            "services": [service.to_json() for service in self.services],
            "journals": [journal.to_json() for journal in self.journals]
        }


def get_company_by_name(session, name: str) -> typing.Optional[WashCompany]:
    smtp = select(WashCompany).where(WashCompany.name == name)
    company = session.scalar(smtp)

    return company


def add_wash_company(session, name: str, avatar: bytes, location: str) -> typing.Union[WashCompany, dict]:
    if get_company_by_name(session, name):
        return {"error": "Company already exists"}

    company = WashCompany(name=name, avatar=avatar, location=location)

    session.add(company)
    session.commit()

    return company

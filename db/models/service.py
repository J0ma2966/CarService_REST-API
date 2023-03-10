import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db.models import BaseModel


class Service(BaseModel):
    __tablename__ = "services"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    duration = sa.Column(sa.Integer)
    price = sa.Column(sa.Integer)

    orders = relationship("Order", secondary='order_services', back_populates='services')
    wash_company_id = sa.Column(sa.BigInteger, sa.ForeignKey('wash_companies.id'))

    def __repr__(self):
        return f"Service\n{self.name=}"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "wash_company_id": self.wash_company_id,
            "price": self.price
        }

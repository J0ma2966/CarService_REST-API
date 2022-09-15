import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db.models import BaseModel


class Washer(BaseModel):
    __tablename__ = "washers"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    phone_number = sa.Column(sa.BigInteger)
    stake = sa.Column(sa.Integer)
    image = sa.Column(sa.LargeBinary, nullable=True)
    is_active = sa.Column(sa.Boolean, default=True)

    orders = relationship("Order", secondary='order_washers', back_populates='washers')
    wash_company_id = sa.Column(sa.BigInteger, sa.ForeignKey('wash_companies.id'))

    def __repr__(self):
        return f"Washer\n{self.name=}"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "stake": self.stake,
            "is_active": self.is_active,
            "wash_company_id": self.wash_company_id,
        }


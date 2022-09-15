import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db.models import BaseModel


class Order(BaseModel):
    __tablename__ = "orders"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    price = sa.Column(sa.Integer)
    car_model = sa.Column(sa.String)
    car_number = sa.Column(sa.String)
    client_name = sa.Column(sa.String)
    client_number = sa.Column(sa.Integer)
    is_active = sa.Column(sa.Boolean, default=True)
    is_canceled = sa.Column(sa.Boolean, default=False)

    date = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())

    wash_company_id = sa.Column(sa.BigInteger, sa.ForeignKey('wash_companies.id'))
    services = relationship('Service', secondary="order_services", back_populates="orders")
    washers = relationship('Washer', secondary="order_washers", back_populates="orders")

    def __repr__(self):
        return f"Order\n{self.id=}"

    def to_json(self):
        return {
            "id": self.id,
            "price": self.price,
            "car_model": self.car_model,
            "car_number": self.car_number,
            "client_name": self.client_name,
            "client_number": self.client_number,
            "is_active": self.is_active,
            "is_canceled": self.is_canceled,
            "wash_company_id": self.wash_company_id,
            "services": [service.to_json() for service in self.services.all()],
            "washers": [washer.to_json() for washer in self.washers.all()]
        }


class OrderServices(BaseModel):
    __tablename__ = "order_services"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    order_id = sa.Column(sa.BigInteger, sa.ForeignKey('orders.id'))
    service_id = sa.Column(sa.BigInteger, sa.ForeignKey('services.id'))


class OrderWashers(BaseModel):
    __tablename__ = "order_washers"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    order_id = sa.Column(sa.BigInteger, sa.ForeignKey('orders.id'))
    washer_id = sa.Column(sa.BigInteger, sa.ForeignKey('washers.id'))

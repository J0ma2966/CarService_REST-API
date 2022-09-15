import datetime

import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.orm import relationship

from db.models import BaseModel
from db.models.service import Service
from db.models.wash_company import get_company_by_id
from db.models.washer import Washer


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
            "services": [service.to_json() for service in self.services],
            "washers": [washer.to_json() for washer in self.washers]
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


def _order_obj(session, id_: int) -> Order:
    order = session.get(Order, id_)

    return order


def get_order_by_id(session, order_id: int) -> dict:
    """
    Get order json object
    :param session: sqlalchemy session
    :param order_id: int
    :return: json
    """
    order = session.get(Order, order_id)

    if order:
        return order.to_json()
    return {"error": "Not found"}


def get_company_order(session, company_id: int, is_active: bool = True, date_from: datetime.datetime = None,
                      date_to: datetime.datetime = None, page: int = 1, offset: int = 10):
    """
    Get company orders with any params
    :param session: SQLAlchemy session
    :param company_id: WashCompany orders return
    :param is_active: by default True
    :param date_from: by default None, means all the time
    :param date_to: by default None, means all the time
    :param page: pagination page
    :param offset: elements per one page
    :return: json obj with orders
    """
    smtp = select(Order).where(
        Order.wash_company_id == company_id, Order.is_active == is_active, Order.date.between(date_from, date_to)
    ).order_by(
        sa.asc(Order.id)
    ).offset(page * offset - offset).limit(offset)
    # - offset because we start page from 1

    orders = session.scalars(smtp)

    return {"orders": [order.to_json() for order in orders]}


def add_new_order(session, price: int, car_model: str, car_number: str, client_name: str, client_number: int,
                  services: list, washers: list,
                  company_id: int, is_active: bool = True, is_canceled: bool = False) -> dict:
    if isinstance(data := get_company_by_id(session, company_id), dict):
        return data

    order = Order(price=price, car_model=car_model, car_number=car_number, client_name=client_name,
                  client_number=client_number, is_active=is_active, is_canceled=is_canceled, wash_company_id=company_id)

    session.add(order)
    session.commit()

    for service in services:
        s = session.get(Service, service)

        if s:
            order.services.append(s)

    for washer in washers:
        w = session.get(Washer, washer)

        if w:
            order.washers.append(w)

    session.commit()

    return order.to_json()


def update_order(session, order_id: int, price: int, car_model: str, car_number: str, is_cancelled: bool,
                 is_active: bool, services: list, washers: list):
    order = _order_obj(session, order_id)

    if price:
        order.price = price
    if car_model:
        order.car_model = car_model
    if car_number:
        order.car_number = car_number
    if isinstance(is_cancelled, bool):
        order.is_canceled = is_cancelled
    if isinstance(is_active, bool):
        order.is_active = is_active
    if services:
        for service in services:
            s = session.get(Service, service)

            if s not in order.services:
                order.services.append(s)
    if washers:
        for washer in washers:
            w = session.get(Washer, washer)

            if w not in order.washers:
                order.washers.append(w)

    session.commit()
    return order

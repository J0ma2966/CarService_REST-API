import datetime

import sqlalchemy as sa
from sqlalchemy import select

from db.models.order import Order
from db.models.service import Service
from db.models.washer import Washer
from db.repos.washing_company_repo import get_company_by_id


def order_obj(session, id_: int) -> Order:
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
    order = order_obj(session, order_id)

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

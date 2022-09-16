import datetime
import typing

import sqlalchemy as sa
from sqlalchemy import select

from db.models.order import Order
from db.models.washer import Washer
from db.repos.order_repo import order_obj


def get_washers_by_name(session, company_id: int, name: str, page: int, offset: int = 10):
    smtp = select(Washer).where(
        Washer.wash_company_id == company_id, Washer.name.ilike(name)
    ).order_by(Washer.id).offset(page * offset - offset).limit(offset)

    washers = session.scalars(smtp)

    return {"washers": [washer.to_json() for washer in washers]}


def get_washer_by_id(session, washer_id: int) -> typing.Union[Washer, dict]:
    washer = session.get(Washer, washer_id)

    if washer:
        return washer

    return {"error": "Not found"}


def get_washer_orders(session, washer_id: int, is_active, date_from: datetime.datetime, date_to: datetime.datetime,
                      page: int = 1, offset: int = 10):
    smtp = select(Washer).join(Order.washers).where(
        Washer.id == washer_id, Order.is_active == is_active, Order.date.between(date_from, date_to)
    ).order_by(
        sa.asc(Washer.id)
    ).offset(page * offset - offset).limit(offset)

    washer = session.scalar(smtp)

    if washer:
        orders = [order.to_json() for order in washer.orders]
    else:
        orders = []

    return {"washer_id": washer_id, "orders": orders}


def add_washer(session, name: str, phone: int, stake: int, company_id: int, is_active: bool) -> Washer:
    washer = Washer(name=name, phone_number=phone, stake=stake, is_active=is_active, wash_company_id=company_id)

    session.add(washer)
    session.commit()

    return washer


def update_washer(session, washer_id: int, name: str, phone: int, stake: int, company_id: int, is_active: bool,
                  orders: list) -> typing.Union[Washer, dict]:
    washer = get_washer_by_id(session, washer_id)

    if isinstance(washer, dict):
        return washer

    if name:
        washer.name = name
    if phone:
        washer.phone_number = phone
    if stake:
        washer.stake = stake
    if company_id:
        washer.wash_company_id = company_id
    if is_active:
        washer.is_active = is_active

    for order_id in orders:
        o = order_obj(session, order_id)

        if o:
            washer.orders.append(o)

    session.commit()

    return washer

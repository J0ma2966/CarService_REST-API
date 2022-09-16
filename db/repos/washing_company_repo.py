import datetime
import typing

from sqlalchemy import select

from api.utils.analytics_db import filter_washers, washers_profit
from db.models.wash_company import WashCompany
from db.models.order import Order


def get_company_by_name(session, name: str) -> typing.Optional[WashCompany]:
    smtp = select(WashCompany).where(WashCompany.name == name)
    company = session.scalar(smtp)

    return company


def get_company_by_id(session, company_id: int) -> typing.Union[WashCompany, dict]:
    company = session.get(WashCompany, company_id)

    if company:
        return company

    return {"error": "Invalid argument 'company_id'"}


def add_wash_company(session, name: str, avatar: bytes, location: str) -> typing.Union[WashCompany, dict]:
    if get_company_by_name(session, name):
        return {"error": "Company already exists"}

    company = WashCompany(name=name, avatar=avatar, location=location)

    session.add(company)
    session.commit()

    return company


def analytics(session, company_id: int, from_date: datetime.datetime, to_date: datetime.datetime):
    smtp = select(Order).where(
        Order.date.between(from_date, to_date), Order.wash_company_id == company_id
    ).order_by(Order.id)

    orders = session.scalars(smtp).all()
    washers = filter_washers([order.washers for order in orders])

    return {
        "totalOrders": len(orders),
        "totalWashers": len(washers),
        "ordersSum": sum(order.price for order in orders),
        "washersSum": washers_profit(orders)
    }



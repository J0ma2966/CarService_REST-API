import typing

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models.service import Service


def get_company_services(session: Session, company_id: int, page: int = 1, offset: int = 10) -> dict:
    smtp = select(Service).where(
        Service.wash_company_id == company_id
    ).order_by(Service.id).offset(page * offset - offset).limit(offset)

    services = session.scalars(smtp)

    return {"services": [service.to_json() for service in services]}


def get_service_by_id(session: Session, service_id: int) -> typing.Union[Service, dict]:
    service = session.get(Service, service_id)

    if service:
        return service

    return {"error": "Not found"}


def add_company_service(session: Session, company_id: int, name: str, duration: int, price: int) -> Service:
    service = Service(name=name, duration=duration, price=price, wash_company_id=company_id)

    session.add(service)
    session.commit()

    return service


def update_service(session: Session, service_id: int, name: str, duration: int, price: int, company_id: int):
    service = get_service_by_id(session, service_id)

    if isinstance(service, dict):
        return service

    if name:
        service.name = name
    if duration:
        service.duration = duration
    if price:
        service.price = price
    if company_id:
        service.wash_company_id = company_id

    session.commit()
    return service

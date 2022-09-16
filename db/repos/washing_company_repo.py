import typing

from sqlalchemy import select

from db.models.wash_company import WashCompany


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

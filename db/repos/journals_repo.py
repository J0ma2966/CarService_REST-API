from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models.journal import Journal


def get_journals_paginate(session: Session, company_id: int, page: int = 1, offset: int = 10):
    smtp = select(Journal).where(Journal.wash_company_id == company_id).order_by(Journal.id).offset(
        page * offset - offset
    ).limit(offset)

    return {"journals": [journal.to_json() for journal in session.scalars(smtp).all()]}


def add_journal(session: Session, data: dict, company_id: int):
    journal = Journal(changes=data, wash_company_id=company_id)

    session.add(journal)
    session.commit()

    return journal

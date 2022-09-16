from flask import Blueprint, request, g

from api.utils.authenticate_user import owner_required
from db.repos import journals_repo


journals_api = Blueprint("journals_api", __name__, url_prefix="/api")


@journals_api.route("/<int:company_id>/getJournals", methods=["GET"])
@owner_required
def get_journals(user: dict, company_id: int):
    page = int(request.args.get("page")) or 1

    return journals_repo.get_journals_paginate(g.session, company_id, page)


@journals_api.route("/<int:company_id>/insertJournal", methods=["POST"])
@owner_required
def add_journal(user: dict, company_id: int):
    req_data = request.json

    j = journals_repo.add_journal(g.session, req_data, company_id)

    return j.to_json()

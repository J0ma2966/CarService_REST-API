import datetime

from flask import Blueprint, request, g

from api.utils.authenticate_user import jwt_token_required
from api.validators.validate_arguments import validate_args
from db.repos import washing_company_repo

stats = Blueprint("analytics_api", __name__, url_prefix="/api")


@stats.route("/<int:company_id>/analytics", methods=["GET"])
@jwt_token_required
def get_analytics(user: dict, company_id: int):
    args = request.args

    data = validate_args(
        (args.get("fromDate"), datetime.datetime.__name__, "from_date"),
        (args.get("toDate"), datetime.datetime.__name__, "to_date"),
    )

    analytics = washing_company_repo.analytics(g.session, company_id, data.get("from_date"), data.get("to_date"))

    return analytics

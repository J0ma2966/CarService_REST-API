from flask import request, g, Blueprint

from api.utils.authenticate_user import jwt_token_required
from db.models.user import Users
from db.models import wash_company as company_repo

company_api = Blueprint(name='wash_company_api', import_name=__name__, url_prefix='/api')


@company_api.route("/washCompanyInsert", methods=["POST"])
@jwt_token_required
def add_wash_company(*args, **kwargs):
    data = request.json

    name = data.get('name')
    avatar = data.get('avatar', None)
    location = data.get('location')

    res = company_repo.add_wash_company(g.session, name, avatar, location)

    if isinstance(res, dict):
        return res, 404

    return res.to_json(), 200


@company_api.route("/getWashCompanyId", methods=["POST"])
@jwt_token_required
def get_users_wash_company(user: Users):
    return {"wash_company_id": user.wash_company_id}, 200

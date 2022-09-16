from flask import request, g, Blueprint

from api.utils.authenticate_user import jwt_token_required
from api.validators.users_requests_validation import sign_validation
from db.models.user import Users
from db.repos import washing_company_repo
from db.repos.user_repo import get_user

company_api = Blueprint(name='wash_company_api', import_name=__name__, url_prefix='/api')


@company_api.route("/washCompanyInsert", methods=["POST"])
@jwt_token_required
def add_wash_company(*args, **kwargs):
    data = request.json

    name = data.get('name')
    avatar = data.get('avatar', None)
    location = data.get('location')

    if name and location:
        res = washing_company_repo.add_wash_company(g.session, name, avatar, location)
    else:
        return {"error": "Validation error"}, 400

    if isinstance(res, dict):
        return res, 404

    return res.to_json(), 200


@company_api.route("/getWashCompanyId", methods=["POST"])
@jwt_token_required
def get_users_wash_company(user: dict):
    if body := request.json:
        data = sign_validation(body.get('login'), body.get('password'))

        if (password := data.get("password")) and (login := data.get("login")):
            user: Users = get_user(g.session, login, password)

            if isinstance(user, Users):
                return {"wash_company_id": user.wash_company_id}, 200

            return user, 400
        return {"error": "Authentication error"}, 400
    else:
        return {"wash_company_id": user.get("wash_company_id")}, 200

from flask import Blueprint
from flask import jsonify
from flask import request, g, session

from api.utils.authenticate_user import authentication, jwt_token_required, logout
from api.validators import users_requests_validation as validators
from db.repos import user_repo

user_api = Blueprint(name='user_api', import_name=__name__, url_prefix='/api')


@user_api.route("/signIn", methods=["POST"])
def user_sign_in():
    body = request.json
    data = validators.sign_validation(body.get('login'), body.get('password'))

    if (password := data.get("password")) and (login := data.get("login")):
        user = user_repo.get_user(
            g.session, login, password
        )

        if isinstance(user, dict):
            return jsonify(user), 400
        else:
            return authentication(user, session)
    else:
        return jsonify(data), 400


@user_api.route("/signUp", methods=["POST"])
def user_sign_up():
    body = request.json
    registration_data = validators.sign_validation(body.get("login"), body.get("password"))

    if (password := registration_data.get("password")) and (login := registration_data.get("login")):
        name = body.get("name")
        role = body.get("role")

        user = user_repo.add_user(g.session, name, login, password, role)

        if isinstance(user, dict):
            return user, 400
        else:
            return authentication(user, session)
    else:
        return jsonify(registration_data), 400


@user_api.route("/signOut", methods=["POST"])
@jwt_token_required
def user_sign_out(user):
    logout(session)
    return {"msg": "Logged out"}

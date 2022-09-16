from flask import Blueprint, request, g

from api.utils.authenticate_user import owner_required
from api.validators.validate_arguments import validate_args
from db.repos import user_repo

credentials = Blueprint("credentials_api", __name__, url_prefix="/api")


@credentials.route("/changePassword", methods=["POST"])
@owner_required
def change_owner_pwd(user: dict):
    data = request.json

    data = validate_args(
        (data.get('oldPassword'), str.__name__, 'old_pwd'),
        (data.get('newPassword'), str.__name__, 'new_pwd')
    )

    if data.get("error"):
        return data, 404

    result = user_repo.change_password(g.session, user.get('id'), data.get('old_pwd'), data.get('new_pwd'))

    if result.get("error"):
        return result, 400

    return {"ok": True, "msg": "Password changed"}

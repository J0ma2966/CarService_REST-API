from flask import Blueprint, request

from api.utils.authenticate_user import owner_required
from api.validators.validate_arguments import validate_args
from api.utils.send_message import send_message_to_email

support = Blueprint("support", __name__, url_prefix="/api")


@support.route("/sendMessage", methods=["POST"])
@owner_required
def send_message_to_email_api(user: dict):
    body = request.json

    data = validate_args(
        (body.get('contact'), str.__name__, 'contact'),
        (body.get('message'), str.__name__, 'message'),
        (body.get('toEmail'), str.__name__, 'email')
    )

    if data.get("error"):
        return data, 400

    result = send_message_to_email(data.get("contact"), data.get("message"), data.get("email"))

    if result.get("error"):
        return result, 400

    return result

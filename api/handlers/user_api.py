from flask import Blueprint, request

user_api = Blueprint(name='user_api', import_name=__name__, url_prefix='/api')


@user_api.route('/signIn', methods=["POST"])
def user_sign_in():
    ...


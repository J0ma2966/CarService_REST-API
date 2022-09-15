import datetime

from flask import request, g, Blueprint

from api.utils.authenticate_user import jwt_token_required
from api.validators.validate_arguments import validate_args
from db.models import order as order_repo

orders_api = Blueprint(name='orders_api', import_name=__name__, url_prefix='/api')


@orders_api.route("/<int:wash_company_id>/orders", methods=["GET"])
@jwt_token_required
def get_company_orders(user: dict, wash_company_id: int):
    args = request.args

    is_active = args.get('IsActive', default=True)
    date_from = args.get('dateFrom', default=None)
    date_to = args.get('dateTo', default=None)
    page = args.get('page', default=1)

    data = validate_args((is_active, bool.__name__, 'is_active'),
                         (date_from, datetime.datetime.__name__, 'date_from'),
                         (date_to, datetime.datetime.__name__, 'date_to'),
                         (page, int.__name__, 'page'))

    if data.get("error"):
        return data, 400

    return order_repo.get_company_order(g.session, wash_company_id, is_active=data.get('is_active'),
                                        date_from=data.get('date_from'),
                                        date_to=data.get('date_to'), page=data.get('page'))


@orders_api.route("/order/<int:order_id>", methods=["GET"])
@jwt_token_required
def get_users_wash_company(user: dict, order_id: int):
    """
    Get order from database if it exists
    :param user: user that send request
    :param order_id: integer
    :return: Order json object or error(404)
    """
    order = order_repo.get_order_by_id(g.session, order_id)

    if order.get("error"):
        return order, 404

    return order


@orders_api.route("/<int:company_id>/insertOrder", methods=["POST"])
@jwt_token_required
def insert_new_order(user: dict, company_id: int):
    data: dict = request.json

    data = validate_args(
        (data.get("price"), int.__name__, "price"),
        (data.get("car_model"), str.__name__, "car_model"),
        (data.get("car_number"), str.__name__, "car_number"),
        (data.get("client_name"), str.__name__, "client_name"),
        (data.get("client_number"), int.__name__, "client_number")
    )

    if data.get("error"):
        return data, 400

    order = order_repo.add_new_order(g.session, data.get('price'), data.get('car_model'), data.get('car_number'),
                                     data.get('client_name'), data.get('client_number'), data.get('services') or [],
                                     data.get('washers') or [], company_id,
                                     data.get('is_active') or True)

    return order


@orders_api.route("/<int:company_id>/updateOrder", methods=["POST"])
@jwt_token_required
def update_order(user: dict, *args):
    ...

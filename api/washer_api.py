import datetime

from flask import Blueprint
from flask import request, g

from api.utils.authenticate_user import jwt_token_required
from api.validators.validate_arguments import validate_args
from db.repos import washers_repo
from db.repos import washing_company_repo

washer_api = Blueprint('washer_api', __name__, url_prefix='/api')


@washer_api.route("/<int:wash_company_id>/washers", methods=["GET"])
@jwt_token_required
def get_company_washers_by_name(user: dict, wash_company_id: int):
    args = request.args

    data = validate_args(
        (args.get('searchName'), str.__name__, 'search_name'),
        (args.get('page'), int.__name__, 'page')
    )

    if data.get('error'):
        return data, 400

    washers = washers_repo.get_washers_by_name(g.session, wash_company_id, data.get('search_name'), data.get('page'))

    return washers


@washer_api.route("/washer")
@jwt_token_required
def get_washer_info(user: dict):
    args = request.args

    data = validate_args((args.get('id'), int.__name__, 'id'))

    if data.get("error"):
        return data, 400

    washer = washers_repo.get_washer_by_id(g.session, data.get('id'))

    if isinstance(washer, dict):
        return washer, 400

    return washer.to_json()


@washer_api.route("/<int:washer_id>/getOrders", methods=["GET"])
@jwt_token_required
def get_washers_orders_by_pagination(user: dict, washer_id: int):
    args = request.args

    data = validate_args(
        (args.get('isActive'), bool.__name__, 'is_active'),
        (args.get('dateFrom'), datetime.datetime.__name__, 'date_from'),
        (args.get('dateTo'), datetime.datetime.__name__, 'date_to'),
        (args.get('page'), int.__name__, 'page')
    )

    if data.get('error'):
        return data, 400

    orders = washers_repo.get_washer_orders(g.session, washer_id, data.get('is_active'), data.get('date_from'),
                                            data.get('date_to'), data.get('page'))

    return orders


@washer_api.route("/<int:wash_company_id>/insertWasher", methods=["POST"])
@jwt_token_required
def add_washer_to_company(user: dict, wash_company_id: int):
    company = washing_company_repo.get_company_by_id(g.session, wash_company_id)

    if isinstance(company, dict):
        return company, 400

    req_data = request.json

    data = validate_args(
        (req_data.get("name"), str.__name__, 'name'),
        (req_data.get("phoneNumber"), int.__name__, 'phone_number'),
        (req_data.get("stake"), int.__name__, 'stake'),
        (req_data.get("isActive"), bool.__name__, 'is_active'),
    )

    if data.get("error"):
        return data, 400

    washer = washers_repo.add_washer(g.session, data.get('name'), data.get('phone_number'),
                                     data.get('stake'), wash_company_id, data.get('is_active'))
    company.washers.append(washer)
    g.session.commit()

    return {"washer": washer.to_json(), "washCompany": company.to_json()}


@washer_api.route("/<int:washer_id>/updateWasher", methods=["POST"])
@jwt_token_required
def update_washer_data(user: dict, washer_id: int):
    req_data = request.json

    data = validate_args((req_data.get("name"), str.__name__, 'name'))
    data.update(validate_args((req_data.get("phoneNumber"), int.__name__, 'phone_number')))
    data.update(validate_args((req_data.get("stake"), int.__name__, 'stake')))
    data.update(validate_args((req_data.get("isActive"), bool.__name__, 'is_active')))
    data.update(validate_args((req_data.get("washCompanyId"), int.__name__, "company_id")))

    washer = washers_repo.update_washer(g.session, washer_id, data.get("name"), data.get("phone_number"),
                                        data.get("stake"), data.get("company_id"), data.get("is_active"),
                                        req_data.get("orders") or [])

    if isinstance(washer, dict):
        return washer, 400

    return {"washer": washer.to_json()}

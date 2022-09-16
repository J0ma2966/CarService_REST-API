from flask import Blueprint, request, g

from api.utils.authenticate_user import jwt_token_required
from api.validators.validate_arguments import validate_args
from db.repos import services_repo

service_api = Blueprint("service_api", __name__, url_prefix="/api")


@service_api.route("/<int:company_id>/services", methods=["GET"])
@jwt_token_required
def get_company_services(user: dict, company_id: int):
    args = request.args

    data = validate_args(
        (args.get('page'), int.__name__, 'page')
    )

    service = services_repo.get_company_services(g.session, company_id, data.get('page') or 1)

    return service


@service_api.route("/service", methods=["GET"])
@jwt_token_required
def get_service_info(user: dict):
    args = request.args

    data = validate_args(
        (args.get('id'), int.__name__, 'id')
    )

    service = services_repo.get_service_by_id(g.session, data.get('id'))

    if isinstance(service, dict):
        return service, 400

    return service.to_json()


@service_api.route("/<int:company_id>insertService", methods=["POST"])
@jwt_token_required
def insert_new_service_for_company(user: dict, company_id: int):
    req_data = request.json

    data = validate_args(
        (req_data.get('name'), str.__name__, 'name'),
        (req_data.get('duration'), int.__name__, 'duration'),
        (req_data.get('price'), int.__name__, 'price'),
    )

    if data.get("error"):
        return data, 400

    service = services_repo.add_company_service(g.session, company_id, data.get('name'), data.get('duration'),
                                                data.get('price'))

    return service.to_json()


@service_api.route("/<int:service_id>/updateService", methods=["POST"])
@jwt_token_required
def edit_service(user: dict, service_id: int):
    req_data = request.json

    data = validate_args((req_data.get('name'), str.__name__, 'name'))
    data.update(validate_args((req_data.get('duration'), int.__name__, 'duration')))
    data.update(validate_args((req_data.get('price'), int.__name__, 'price')))
    data.update(validate_args((req_data.get("washCompanyId"), int.__name__, 'company_id')))

    service = services_repo.update_service(g.session, service_id, data.get('name'), data.get('duration'),
                                           data.get('price'), data.get('company_id'))

    if isinstance(service, dict):
        return service, 400

    return service.to_json()

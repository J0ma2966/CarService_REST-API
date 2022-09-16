import sqlalchemy
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy.orm import sessionmaker

from api.analytics_api import stats
from api.change_pwd_api import credentials
from api.orders_api import orders_api
from api.journals_api import journals_api
from api.services_api import service_api
from api.support_api import support
from api.user_api import user_api
from api.wash_company_api import company_api
from api.washer_api import washer_api
from config.app_config import DevelopmentCfg
from config.conf import load_config
from db import get_engine
from middlewares.database import DbMiddleware


def create_tables(engine: sqlalchemy.engine.Engine):
    from db.models import BaseModel

    BaseModel.metadata.create_all(engine)


def main():
    cfg = load_config()

    app = Flask(__name__)
    swagger_blueprint = get_swaggerui_blueprint(
        base_url="/api/swagger",
        api_url="/static/swagger.json",
        config={
            "app_name": "WashCompanyApi"
        }
    )
    # register something like a middleware for using session from Flask.g(thread-local)
    engine = get_engine(cfg.db_cfg)
    session_maker = sessionmaker(engine)
    db_session_middleware = DbMiddleware(app, session_maker)
    db_session_middleware.register()

    # create tables
    create_tables(engine)

    # register api blueprints
    app.register_blueprint(swagger_blueprint, url_prefix="/api/swagger")
    app.register_blueprint(user_api)
    app.register_blueprint(company_api)
    app.register_blueprint(orders_api)
    app.register_blueprint(washer_api)
    app.register_blueprint(service_api)
    app.register_blueprint(stats)
    app.register_blueprint(journals_api)
    app.register_blueprint(credentials)
    app.register_blueprint(support)

    # start app
    app.config.from_object(DevelopmentCfg)
    app.run()


if __name__ == "__main__":
    main()

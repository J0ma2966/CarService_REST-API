import sqlalchemy
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy.orm import sessionmaker

from api.handlers.user_api import user_api
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

    # start app
    app.run(debug=True)


if __name__ == "__main__":
    main()

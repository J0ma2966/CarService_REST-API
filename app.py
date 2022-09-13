from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from api.handlers.user_api import user_api


def main():
    app = Flask(__name__)
    swagger_blueprint = get_swaggerui_blueprint(
        base_url="/api/swagger",
        api_url="/static/swagger.json",
        config={
            "app_name": "WashCompanyApi"
        }
    )

    app.register_blueprint(swagger_blueprint, url_prefix="/api/swagger")
    app.register_blueprint(user_api)
    app.run(debug=True)


if __name__ == "__main__":
    main()

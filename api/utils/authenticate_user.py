import jwt
from flask import jsonify, g

from config.app_config import DevelopmentCfg
from db.models.user import get_user_by_id


def authentication(user, user_session):
    if 'x-access-token' in user_session:
        token = user_session.get('x-access-token')
        try:
            user = jwt.decode(token, DevelopmentCfg.SECRET_KEY, "HS256")
            return get_user_by_id(g.session, user.get('user'))
        except jwt.ExpiredSignatureError:
            return "Invalid token"

    else:
        response = jsonify(user.to_json())
        user_session['x-access-token'] = user.encode_access_token()
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"

        return response

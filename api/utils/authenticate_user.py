from functools import wraps

import jwt
from flask import jsonify, g, session

from config.app_config import DevelopmentCfg
from db.models.user import get_user_by_id


def authentication(user, user_session):
    if 'x-access-token' in user_session:
        token = user_session.get('x-access-token')

        try:
            user_info = jwt.decode(token, DevelopmentCfg.SECRET_KEY, "HS256")
            return get_user_by_id(g.session, user_info.get('user'))
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token is invalid'}), 400
    else:
        return _set_new_jwt_token(user, user_session)


def _set_new_jwt_token(user, users_session):
    response = jsonify(user.to_json())
    users_session['x-access-token'] = user.encode_access_token()
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"

    return response


def jwt_token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'x-access-token' in session:
            token = session.get('x-access-token')
        else:
            return jsonify({'error': 'A valid token is missing, please log-in'}), 400

        try:
            data = jwt.decode(token, DevelopmentCfg.SECRET_KEY, "HS256")
            current_user = get_user_by_id(g.session, data.get('user'))

            if current_user.get("error"):
                return jsonify(current_user)

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token is invalid'}), 400

        return f(current_user, *args, **kwargs)

    return decorator


def logout(user_session):
    user_session.pop('x-access-token')

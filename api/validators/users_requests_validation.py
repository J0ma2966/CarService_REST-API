import re
import typing

regex_email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
# Commonly used regular expression for a password - should be at least 8 characters long, includes a special character
regex_password = re.compile(r"([A-Za-z0-9$%#@]{8,})")


def _validate_login(login: str) -> dict:
    if login:
        return {"login": login}
    else:
        return {"error": "Login validation error"}


def _validate_password(password) -> dict:
    if not password or (len(password) < 8) or (re.search(r"[$%#@]", password) is None) or (
            (regex_password.fullmatch(password)) is None):
        if not password:
            return {"error": "Password validation error, can't find password"}
        if len(password) < 8:
            return {"error": "Password length validation error"}
        if re.search(r"[$%#@]", password) is None:
            return {"error": "Password validation error, minimum one special character"}
        if (regex_password.fullmatch(password)) is None:
            return {"error": "Password validation error"}
    else:
        return {"password": password}


def _extract_errors(email_or_login: dict, password: dict) -> dict:
    if "error" in email_or_login and "error" in password:
        return {"errors": [email_or_login.get("error"), password.get("error")]}

    else:
        if "error" in email_or_login:
            return email_or_login
        elif "error" in password:
            return password
        else:
            email_or_login.update(password)
            return email_or_login


def sign_validation(login: str, password) -> dict:
    login = _validate_login(login)
    password = _validate_password(password)

    return _extract_errors(login, password)

import enum


class UserRole(enum.Enum):
    """ User available roles """
    admin = "admin"
    owner = "owner"


def check_is_valid_role(val):
    try:
        getattr(UserRole, val)
        return True
    except AttributeError:
        return False

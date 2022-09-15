import datetime


def validate_args(*args):
    arguments = {}

    for v, type_of, key in args:
        if type_of == "bool":
            if v in ['true', 'True']:
                arguments[key] = True
            elif v in ['false', 'False']:
                arguments[key] = False
            else:
                return {"error": "Arguments error"}

        elif type_of == "int":
            try:
                arguments[key] = int(v)
            except (TypeError, ValueError):
                return {"error": "Arguments error"}

        elif type_of == "datetime":
            try:
                arguments[key] = datetime.datetime.strptime(v, '%Y-%m-%d')
            except (ValueError, TypeError):
                return {"error": "Arguments error"}

        elif type_of == "str":
            if v:
                arguments[key] = v
            else:
                return {"error": "Arguments error"}

    return arguments

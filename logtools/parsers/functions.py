import datetime


def nullable_int(x):
    if x is None:
        return None
    return int(x)


def maybe_int(x):
    try:
        return int(x)
    except ValueError:
        return None


def parse_dt_string(dt_string):
    return datetime.datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S.%f")

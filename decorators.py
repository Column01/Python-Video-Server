from functools import wraps
from flask import request, abort


accepted_ips = ["127.0.0.1"]


def ip_filtered(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if request.remote_addr in accepted_ips or request.remote_addr.startswith("192.168.0"):
            return f(*args, **kwargs)
        else:
            return abort(403)
    return wrapped
from functools import wraps
from flask import request, abort


accepted_ips = ["127.0.0.1"]


def ip_filtered(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if request.remote_addr in accepted_ips or is_local_ip():
            return f(*args, **kwargs)
        else:
            return abort(403)
    return wrapped


def is_local_ip():
    addr = request.remote_addr
    return addr.startswith("192.168") or addr.startswith("10") or addr.startswith("172.16")
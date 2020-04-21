from functools import wraps
from flask import request, abort

from misc import *


def ip_filtered(f):
    accepted_ips = get_ip_whitelist()
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


def get_ip_whitelist():
    return get_file("ips.txt").replace("\n", "").strip(" ").strip().split(",")

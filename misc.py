import os
from functools import wraps

from flask import abort, request


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_sub_folders(folder):
    return [f for f in sorted(os.listdir(folder)) if os.path.isdir(os.path.join(folder, f))]


def get_folder_files(folder):
    return [f for f in sorted(os.listdir(folder)) if os.path.isfile(os.path.join(folder, f)) and f.endswith(".mp4")]


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError:
        return "File not found"


def ip_filtered(f):
    
    @wraps(f)
    def wrapped(*args, **kwargs):
        accepted_ips = get_ip_whitelist()
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

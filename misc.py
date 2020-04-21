import os


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
    except IOError as exc:
        return str(exc)

import os


def _get_ext(filename):
    filename = os.path.normpath(filename)
    ext = os.path.splitext(filename)[1]
    return ext


def is_qvnote(filename):
    ext = _get_ext(filename)
    return ext == '.qvnote'


def is_qvnotebook(filename):
    ext = _get_ext(filename)
    return ext == '.qvnotebook'


def is_qvlibrary(filename):
    ext = _get_ext(filename)
    return ext == '.qvlibrary'

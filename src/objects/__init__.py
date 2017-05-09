import os

from utils import is_qvlibrary, is_qvnote, is_qvnotebook
from .qvlibrary import QvLibrary
from .qvnote import QvNote
from .qvnotebook import QvNotebook


class QvFactory(object):
    @staticmethod
    def create(filename):
        path = os.path.join(os.getcwd(), filename)
        if is_qvnote(filename):
            return QvNote(path)
        elif is_qvnotebook(filename):
            return QvNotebook(path)
        elif is_qvlibrary(filename):
            return QvLibrary(path)
        else:
            raise Exception('not support path: %s' % filename)

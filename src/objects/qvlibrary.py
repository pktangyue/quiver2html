import os

from mixin import ParserMixin
from utils import is_qvnotebook
from .qvnotebook import QvNotebook


class QvLibrary(ParserMixin):
    def __init__(self, path):
        self._path = path
        self._qvnotebooks = []

        for filename in os.listdir(self._path):
            if not is_qvnotebook(filename) or filename == 'Trash.qvnotebook':
                continue
            self._qvnotebooks.append(QvNotebook(self, os.path.join(self._path, filename)))

    @property
    def qvnotebooks(self):
        return self._qvnotebooks

    def parse(self, template, output):
        for qvnotebook in self.qvnotebooks:
            qvnotebook.parse(template, output)

    def get_qvnote(self, uuid):
        return next(
            iter([qvnote
                  for qvnotebook in self.qvnotebooks
                  for qvnote in qvnotebook.qvnotes
                  if qvnote.uuid == uuid])
            , None
        )

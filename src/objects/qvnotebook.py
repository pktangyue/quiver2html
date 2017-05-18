import json
import os

from mixin import ParserMixin
from utils import is_qvnote
from .qvnote import QvNote


class QvNotebook(ParserMixin):
    def __init__(self, parent, path):
        self._parent = parent
        self._path = path
        self._qvnotes = []

        with open(os.path.join(self._path, 'meta.json'), encoding='UTF-8') as f:
            data = json.load(f)
            self._meta = QvNotebookMeta(**data)

        for filename in os.listdir(self._path):
            if not is_qvnote(filename):
                continue
            self._qvnotes.append(QvNote(self, os.path.join(self._path, filename)))

    @property
    def parent(self):
        return self._parent

    @property
    def name(self):
        return self._meta.name if self._meta else ''

    @property
    def filename(self):
        return self.name.replace(' ', '_') + '/'

    @property
    def qvnotes(self):
        return self._qvnotes

    def parse(self, template, classes, output):
        output = self.get_output_dir(output, self.name)
        for qvnote in self.qvnotes:
            qvnote.parse(template, classes, output)


class QvNotebookMeta(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.uuid = kwargs.get('uuid', None)

    def __repr__(self):
        return json.dumps(self.__dict__)

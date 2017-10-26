import json
import os

from .qvnote import QvNote
from ..mixin import ParserMixin
from ..utils import is_qvnote


class QvNotebook(ParserMixin):
    def __init__(self, path, parent=None):
        self._parent = parent
        self._path = path
        self._qvnotes = []

        with open(os.path.join(self._path, 'meta.json'), encoding='UTF-8') as f:
            data = json.load(f)
            self._meta = QvNotebookMeta(**data)

        for filename in os.listdir(self._path):
            if not is_qvnote(filename):
                continue
            self._qvnotes.append(QvNote(os.path.join(self._path, filename), parent=self))

        self._qvnotes.sort(key=lambda v: v.created_datetime)

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
    def html(self):
        ret = '<ul>'
        for qvnote in self.qvnotes:
            ret += '<li><a href="{}">{}</a></li>'.format(qvnote.get_url(), qvnote.name)

        ret += '</ul>'
        return ret

    @property
    def qvnotes(self):
        return self._qvnotes

    def get_url(self, root='.'):
        return os.path.join(root, self.filename, 'index.html')

    def parse(self, template, output, classes=None, resources_url=None, write_file_func=None):
        output = self.get_output_dir(output, self.name)
        for qvnote in self.qvnotes:
            qvnote.parse(template, output, classes, resources_url, write_file_func)

        context = {
            'title'    : self.name,
            'content'  : self.html,
            'navigator': ''
        }

        write_file_func = write_file_func or self.write_file_func

        write_file_func(template, output, 'index.html', context)

class QvNotebookMeta(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.uuid = kwargs.get('uuid', None)

    def __repr__(self):
        return json.dumps(self.__dict__)

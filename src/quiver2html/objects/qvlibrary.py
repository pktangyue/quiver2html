import os

from .qvnotebook import QvNotebook
from ..mixin import ParserMixin
from ..objects import QV_TYPES
from ..utils import is_qvnotebook


class QvLibrary(ParserMixin):
    type = QV_TYPES.LIBRARY

    def __init__(self, path):
        self._path = path
        self._qvnotebooks = []

        for filename in os.listdir(self._path):
            if not is_qvnotebook(filename) or filename == 'Trash.qvnotebook':
                continue
            self._qvnotebooks.append(QvNotebook(os.path.join(self._path, filename), parent=self))

        self._qvnotebooks.sort(key=lambda v: v.name)

    @property
    def qvnotebooks(self):
        return self._qvnotebooks

    @property
    def html(self):
        ret = '<ul>'
        for qvnotebook in self._qvnotebooks:
            if not qvnotebook.qvnotes:
                continue
            ret += '<li>'
            ret += '<a href="{}">{}</a>'.format(qvnotebook.get_url(), qvnotebook.name)
            ret += '<ul>'
            for qvnote in qvnotebook.qvnotes:
                ret += '<li><a href="{}">{}</a></li>'.format(qvnote.get_url('.'), qvnote.name)

            ret += '</ul>'
            ret += '</li>'

        ret += '</ul>'
        return ret

    def parse(self, template, output, classes=None, resources_url=None, write_file_func=None):
        for qvnotebook in self.qvnotebooks:
            qvnotebook.parse(template, output, classes, resources_url, write_file_func)

        write_file_func = write_file_func or self.write_file_func

        context = {
            'ins'    : self,
            'title'  : 'home',
            'content': self.html,
        }

        write_file_func(template, output, 'index.html', context)

    def get_qvnote(self, uuid):
        return next(
            iter([qvnote
                  for qvnotebook in self.qvnotebooks
                  for qvnote in qvnotebook.qvnotes
                  if qvnote.uuid == uuid])
            , None
        )

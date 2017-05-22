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

    def parse(self, template, classes, output):
        for qvnotebook in self.qvnotebooks:
            qvnotebook.parse(template, classes, output)

        with open(os.path.join(output, 'index.html'), mode='w', encoding='UTF-8') as f:
            output_html = template.replace(
                '{{title}}', 'home'
            ).replace(
                '{{content}}', self.html
            ).replace(
                '{{navigator}}', ''
            )
            f.write(output_html)

    def get_qvnote(self, uuid):
        return next(
            iter([qvnote
                  for qvnotebook in self.qvnotebooks
                  for qvnote in qvnotebook.qvnotes
                  if qvnote.uuid == uuid])
            , None
        )

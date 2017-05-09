import cgi
import json
import os

import markdown


class QvNote(object):
    _meta = None
    _content = None
    _resources = []

    def __init__(self, path):
        self._path = path

        with open(os.path.join(self._path, 'meta.json'), encoding='UTF-8') as f:
            data = json.load(f)
            self._meta = QvNoteMeta(**data)

        with open(os.path.join(self._path, 'content.json'), encoding='UTF-8') as f:
            data = json.load(f)
            self._content = QvNoteContent(**data)

        resource_dir = os.path.join(self._path, 'resources')
        if os.path.exists(resource_dir):
            for resource_path in os.listdir(resource_dir):
                self._resources.append(QvNoteResource(os.path.join(resource_dir, resource_path)))

    def get_title(self):
        return self._meta.title if self._meta else ''

    def get_html(self):
        return self._content.get_html() if self._content else ''

    def get_resources(self):
        return self._resources


class QvNoteMeta(object):

    def __init__(self, **kwargs):
        self.created_at = kwargs.get('created_at', None)
        self.tags = kwargs.get('tags', [])
        self.title = kwargs.get('title', None)
        self.updated_at = kwargs.get('updated_at', None)
        self.uuid = kwargs.get('uuid', None)

    def __repr__(self):
        return json.dumps(self.__dict__)


class QvNoteContent(object):

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', None)
        self.cells = kwargs.get('cells', [])

    def __repr__(self):
        return json.dumps(self.__dict__)

    def get_html(self):
        html = ''
        for cell in self.cells:
            html += getattr(self, 'parse_' + cell['type'])(cell)

        return html

    def parse_text(self, cell):
        data = cell['data'].replace('quiver-image-url', 'resources')
        return "<div class='cell cell-text'>%s</div>" % data

    def parse_code(self, cell):
        data = cgi.escape(cell['data'])
        return "<div class='cell cell-code'><pre><code class='lang-%s'>%s</code></pre></div>" % (cell['language'], data)

    def parse_markdown(self, cell):
        data = cell['data'].replace('quiver-image-url', 'resources')
        data = markdown.markdown(data,
                                 output_format='html5',
                                 extensions=[
                                   'pymdownx.github'
                                 ])
        return "<div class='cell cell-markdown'>%s</div>" % data

    def parse_latex(self, cell):
        data = cell['data']
        return "<div class='cell cell-latex'>%s</div>" % data

    def parse_diagram(self, cell):
        data = cell['data']
        return "<div class='cell cell-diagram'>%s</div>" % data


class QvNoteResource(object):
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return json.dumps(self.__dict__)


class QvNotebook(object):
    def __init__(self, path):
        self._path = path

        with open(os.path.join(self._path, 'meta.json'), encoding='UTF-8') as f:
            data = json.load(f)
            self._meta = QvNotebookMeta(**data)

    def get_name(self):
        return self._meta.name if self._meta else ''


class QvNotebookMeta(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.uuid = kwargs.get('uuid', None)

    def __repr__(self):
        return json.dumps(self.__dict__)

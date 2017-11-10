import json
import os
import re
from datetime import datetime

import markdown

from ..mixin import ParserMixin
from ..objects import QV_TYPES


class QvNote(ParserMixin):
    type = QV_TYPES.NOTE

    def __init__(self, path, parent=None):
        self._parent = parent
        self._path = path

        with open(os.path.join(self._path, 'meta.json'), encoding='UTF-8') as f:
            data = json.load(f)
            self._meta = QvNoteMeta(**data)

        with open(os.path.join(self._path, 'content.json'), encoding='UTF-8') as f:
            data = json.load(f)
            self._content = QvNoteContent(**data)

        self._resources = []
        resource_dir = os.path.join(self._path, 'resources')
        if os.path.exists(resource_dir):
            for resource_path in os.listdir(resource_dir):
                self._resources.append(QvNoteResource(os.path.join(resource_dir, resource_path)))

    @property
    def parent(self):
        return self._parent

    @property
    def name(self):
        return self._meta.title if self._meta else ''

    @property
    def filename(self):
        return self.name.replace(' ', '_') + '.html'

    @property
    def uuid(self):
        return self._meta.uuid if self._meta else ''

    @property
    def html(self):
        return self._content.html if self._content else ''

    @property
    def tags(self):
        return self._meta.tags if self._meta else []

    @property
    def create_datetime(self):
        return datetime.fromtimestamp(self._meta.created_at) if self._meta else datetime.min

    @property
    def update_datetime(self):
        return datetime.fromtimestamp(self._meta.updated_at) if self._meta else datetime.min

    @property
    def resources(self):
        return self._resources

    def get_url(self, root='..'):
        return os.path.join(root, self.parent.filename, self.filename)

    def parse(self, template, output, classes=None, resources_url=None, write_file_func=None):
        # parse html
        html = self.html
        html = self.convert_resource_url(html, resources_url if resources_url else '../resources')
        html = self.convert_note_url(html)
        html = self.add_html_tag_classes(html, classes)

        prev_note = self.get_prev_note()
        next_note = self.get_next_note()
        navigator = {}
        if prev_note:
            navigator['prev'] = {
                'name': prev_note.name,
                'url' : prev_note.get_url(),
            }
        if next_note:
            navigator['next'] = {
                'name': next_note.name,
                'url' : next_note.get_url(),
            }

        context = {
            'ins'      : self,
            'title'    : self.name,
            'content'  : html,
            'navigator': navigator,
        }

        # export html file
        output = self.get_output_dir(output)

        write_file_func = write_file_func or self.write_file_func

        write_file_func(template, output, self.filename, context, resources=self.resources)

    def convert_resource_url(self, data, resource_url):
        return data.replace('quiver-image-url', resource_url)

    def convert_note_url(self, data):
        def repl(match):
            uuid = match.group(1)
            qvnote = self.parent.parent.get_qvnote(uuid)
            return qvnote.get_url()

        p = re.compile(r'quiver-note-url/(\w{8}(?:-\w{4}){3}-\w{12})')
        return p.sub(repl, data)

    def add_html_tag_classes(self, html, classes):
        classes = classes or {}
        for key, value in classes.items():
            html = html.replace('<{}>'.format(key), '<{} class="{}">'.format(key, value))
        return html

    def get_prev_note(self):
        if self.parent.qvnotes.index(self) == 0:
            return None
        try:
            return self.parent.qvnotes[self.parent.qvnotes.index(self) - 1]
        except ValueError:
            return None
        except IndexError:
            return None

    def get_next_note(self):
        try:
            return self.parent.qvnotes[self.parent.qvnotes.index(self) + 1]
        except ValueError:
            return None
        except IndexError:
            return None


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

    @property
    def html(self):
        html = ''
        for cell in self.cells:
            html += getattr(self, 'parse_' + cell['type'])(cell)

        return html

    def parse_text(self, cell):
        data = cell['data']
        return "<div class='cell cell-text'>%s</div>" % data

    def parse_code(self, cell):
        data = '```{}\n{}\n```'.format(cell['language'], cell['data'])
        return "<div class='cell cell-code'>%s</div>" % (self._markdown_to_html(data))

    def parse_markdown(self, cell):
        return "<div class='cell cell-markdown'>%s</div>" % self._markdown_to_html(cell['data'])

    def parse_latex(self, cell):
        return "<div class='cell cell-latex'>%s</div>" % self._markdown_to_html(cell['data'])

    def parse_diagram(self, cell):
        data = '```{}\n{}\n```'.format(cell['diagramType'], cell['data'])
        return "<div class='cell cell-diagram'>%s</div>" % self._markdown_to_html(data)

    def _markdown_to_html(self, data):
        data = markdown.markdown(
            data,
            output_format='html5',
            extensions=[
                'markdown.extensions.nl2br',
                'pymdownx.github',
                'pymdownx.highlight',
                'pymdownx.arithmatex',
            ],
            extension_configs={
                'pymdownx.highlight': {
                    'noclasses'     : True,
                    'pygments_style': 'github',
                }
            }
        )
        return data


class QvNoteResource(object):
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return json.dumps(self.__dict__)

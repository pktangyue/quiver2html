import html
import json
import os
import re
from shutil import copy2

import markdown

from mixin import ParserMixin


class QvNote(ParserMixin):
    def __init__(self, parent, path):
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
    def title(self):
        return self._meta.title if self._meta else ''

    @property
    def filename(self):
        return self.title.replace(' ', '_') + '.html'

    @property
    def uuid(self):
        return self._meta.uuid if self._meta else ''

    @property
    def html(self):
        return self._content.html if self._content else ''

    @property
    def resources(self):
        return self._resources

    def parse(self, template, classes, output):
        # parse html
        html = self.html
        html = self.convert_resource_url(html)
        html = self.convert_note_url(html)
        html = self.add_html_tag_classes(html, classes)
        output_html = template.replace(
            '{{title}}', self.title
        ).replace(
            '{{content}}', html
        )

        # export html file
        output_dir = self.get_output_dir(output)
        output_filename = os.path.join(
            output_dir,
            self.filename,
        )
        with open(output_filename, mode='w', encoding='UTF-8') as f:
            f.write(output_html)

        # export resources
        if self.resources:
            resources_dir = os.path.join(output_dir, 'resources')
            os.makedirs(resources_dir, exist_ok=True)
            for resource in self.resources:
                copy2(resource.path, resources_dir)

    def convert_resource_url(self, data):
        return data.replace('quiver-image-url', 'resources')

    def convert_note_url(self, data):
        def repl(match):
            uuid = match.group(1)
            qvnote = self.parent.parent.get_qvnote(uuid)
            return os.path.join('..', qvnote.parent.filename, qvnote.filename)

        p = re.compile(r'quiver-note-url/(\w{8}(?:-\w{4}){3}-\w{12})')
        return p.sub(repl, data)

    def add_html_tag_classes(self, html, classes):
        if classes:
            for key, value in classes.items():
                html = html.replace('<{}>'.format(key), '<{} class="{}">'.format(key, value))
        return html


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
                'pymdownx.highlight':{
                    'noclasses': True,
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

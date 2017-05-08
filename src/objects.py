import cgi
import json
import markdown2
import markdown


class Qvnote(object):

    def __init__(self, meta, content):
        self.meta = meta
        self.content = content


class QvnoteMeta(object):

    def __init__(self, **kwargs):
        self.created_at = kwargs.get('created_at', None)
        self.tags = kwargs.get('tags', [])
        self.title = kwargs.get('title', None)
        self.updated_at = kwargs.get('updated_at', None)
        self.uuid = kwargs.get('uuid', None)

    def __repr__(self):
        return json.dumps(self.__dict__)


class QvnoteContent(object):

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


class QvnotebookMeta(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.uuid = kwargs.get('uuid', None)

    def __repr__(self):
        return json.dumps(self.__dict__)

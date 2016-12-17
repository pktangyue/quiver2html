import json
import os
from urllib import quote_plus
import codecs

from objects import Qvnote, QvnoteMeta, QvnoteContent, QvnotebookMeta
from utils import is_qvnote, is_qvnotebook, is_qvlibrary


def _get_output_dir(*args):
    output_dir = os.getcwd()
    for arg in args:
        output_dir = os.path.join(output_dir, arg)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

    return output_dir


def parse(filename, template, output):
    path = os.path.join(os.getcwd(), filename)
    if is_qvnote(filename):
        parse_qvnote(path, template, output)
    elif is_qvnotebook(filename):
        parse_qvnotebook(path, template, output)
    elif is_qvlibrary(filename):
        parse_qvlibrary(path, template, output)
    else:
        print 'not support path: %s' % filename


def parse_qvnote(path, template, output):
    with open(os.path.join(path, 'meta.json')) as f:
        data = json.load(f)
        meta = QvnoteMeta(**data)

    with open(os.path.join(path, 'content.json')) as f:
        data = json.load(f)
        content = QvnoteContent(**data)

    qvnote = Qvnote(meta, content)

    output_html = template.replace(
        '{{title}}', qvnote.meta.title
    ).replace(
        '{{content}}', qvnote.content.get_html()
    )
    output_dir = _get_output_dir(output)
    output_filename = os.path.join(
        output_dir,
        codecs.encode(qvnote.meta.title, 'utf-8') + '.html'
    )
    with codecs.open(output_filename, 'w', 'utf-8') as f:
        f.write(output_html)


def parse_qvnotebook(path, template, output):
    with open(os.path.join(path, 'meta.json')) as f:
        data = json.load(f)
        meta = QvnotebookMeta(**data)

    output = _get_output_dir(output, codecs.encode(meta.name, 'utf-8'))
    for filename in os.listdir(path):
        if not is_qvnote(filename):
            continue
        parse_qvnote(os.path.join(path, filename), template, output)


def parse_qvlibrary(path, template, output):
    for filename in os.listdir(path):
        if not is_qvnotebook(filename) or filename == 'Trash.qvnotebook':
            continue
        parse_qvnotebook(os.path.join(path, filename), template, output)

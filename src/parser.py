import os
from abc import ABCMeta, abstractmethod
from shutil import copy2

from objects import QvNote, QvNotebook
from utils import is_qvnote, is_qvnotebook, is_qvlibrary


class ParserFactory(object):
    @staticmethod
    def create(filename, template, output):
        path = os.path.join(os.getcwd(), filename)
        if is_qvnote(filename):
            return QvNoteParser(path, template, output)
        elif is_qvnotebook(filename):
            return QvNoteBookParser(path, template, output)
        elif is_qvlibrary(filename):
            return QvLibraryParser(path, template, output)
        else:
            raise Exception('not support path: %s' % filename)


class BaseParser(object):
    __metaclass__ = ABCMeta

    def __init__(self, path, template, output):
        self.path = path
        self.template = template
        self.output = output

    @abstractmethod
    def parse(self):
        pass

    def get_output_dir(self, *args):
        output_dir = os.getcwd()
        for arg in args:
            output_dir = os.path.join(output_dir, arg.replace(' ', '_'))
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

        return output_dir


class QvNoteParser(BaseParser):
    def parse(self):
        # construct qvnote object
        qvnote = QvNote(self.path)

        # parse html
        output_html = self.template.replace(
            '{{title}}', qvnote.get_title()
        ).replace(
            '{{content}}', qvnote.get_html()
        )

        # export html file
        output_dir = self.get_output_dir(self.output)
        output_filename = os.path.join(
            output_dir,
            qvnote.get_title().replace(' ', '_') + '.html'
        )
        with open(output_filename, mode='w', encoding='UTF-8') as f:
            f.write(output_html)

        # export resources
        if qvnote.get_resources():
            resources_dir = os.path.join(output_dir, 'resources')
            os.makedirs(resources_dir, exist_ok=True)
            for resource in qvnote.get_resources():
                copy2(resource.path, resources_dir)


class QvNoteBookParser(BaseParser):
    def parse(self):
        qvnotebook = QvNotebook(self.path)
        output = self.get_output_dir(self.output, qvnotebook.get_name())
        for filename in os.listdir(self.path):
            if not is_qvnote(filename):
                continue
            QvNoteParser(os.path.join(self.path, filename), self.template, output).parse()


class QvLibraryParser(BaseParser):
    def parse(self):
        for filename in os.listdir(self.path):
            if not is_qvnotebook(filename) or filename == 'Trash.qvnotebook':
                continue
            QvNoteBookParser(os.path.join(self.path, filename), self.template, self.output).parse()

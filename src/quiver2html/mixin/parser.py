import os
from abc import ABCMeta, abstractmethod
from shutil import copy2


class ParserMixin(metaclass=ABCMeta):

    @abstractmethod
    def parse(self, template, output, classes=None, resources_url=None, write_file_func=None):
        pass

    def write_file_func(self, template, output, filename, context, resources=None):
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(os.path.dirname(template)))
        env.get_template(os.path.basename(template)).stream(context).dump(os.path.join(output, filename))
        # export resources
        if resources:
            resources_dir = os.path.join(os.path.dirname(output), 'resources')
            os.makedirs(resources_dir, exist_ok=True)
            for resource in resources:
                copy2(resource.path, resources_dir)

    def get_output_dir(self, *args):
        output_dir = os.getcwd()
        for arg in args:
            output_dir = os.path.join(output_dir, arg.replace(' ', '_'))
            os.makedirs(output_dir, exist_ok=True)

        return output_dir

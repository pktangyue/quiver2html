import os
from abc import ABCMeta, abstractmethod
from shutil import copy2


class ParserMixin(metaclass=ABCMeta):

    @abstractmethod
    def parse(self, template, output, classes=None, resources_url=None, write_file_func=None):
        pass

    def write_file_func(self, template, output, filename, context, resources=None):
        with open(template, mode='r', encoding='UTF-8') as f:
            content = f.read()

        with open(os.path.join(output, filename), mode='w', encoding='UTF-8') as f:
            for key, value in context.items():
                content = content.replace(
                    '{{' + key + '}}', value
                )
            f.write(content)

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

import os
from abc import ABCMeta, abstractmethod


class ParserMixin(metaclass=ABCMeta):

    @abstractmethod
    def parse(self, template, output):
        pass

    def get_output_dir(self, *args):
        output_dir = os.getcwd()
        for arg in args:
            output_dir = os.path.join(output_dir, arg.replace(' ', '_'))
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

        return output_dir

#!/usr/bin/env python
import argparse
import os
import sys

from quiver2html.objects.factory import QvFactory


class StoreDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        ret = {}
        for s in values:
            key, value = s.split('=')
            ret[key] = value
        setattr(namespace, self.dest, ret)


# parse command args
def parse_args():
    src_dir = os.path.dirname(sys.path[0])

    parser = argparse.ArgumentParser(
        prog='quiver2html',
        description='convert quiver note/notebook/library to html.',
    )
    parser.add_argument(
        'notes',
        nargs='+',
        help='.qvlibrary or .qvnotebook or .qvnote dir',
    )
    parser.add_argument(
        '-t',
        '--template',
        default=src_dir + '/template/index.html',
        metavar='TEMPLATE_FILE',
        help='template html file',
    )
    parser.add_argument(
        '--classes',
        action=StoreDict,
        nargs='+',
        metavar='HTML_TAG=CLASSES',
        help='add css classes to html tag'
    )
    parser.add_argument(
        '-o',
        '--output',
        default='output',
        metavar='OUTPUT_DIR',
        help='dest output dir',
    )
    parser.add_argument(
        '--resources_url',
        metavar='RESOURCE_OUTPUT_DIR',
        help='dest resource output dir',
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    template = args.template
    output = args.output
    notes = args.notes
    classes = args.classes
    resources_url = args.resources_url
    for note in notes:
        QvFactory.create(note).parse(template, output, classes=classes, resources_url=resources_url)

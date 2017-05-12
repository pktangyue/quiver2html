import argparse
import os
import sys


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
        '-o',
        '--output',
        default='output',
        metavar='OUTPUT_DIR',
        help='dest output dir',
    )
    parser.add_argument(
        '-t',
        '--template',
        type=argparse.FileType(mode='r', encoding='UTF-8'),
        default= src_dir + '/template/index.html',
        metavar='TEMPLATE_FILE',
        help='template html file',
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    return parser.parse_args()

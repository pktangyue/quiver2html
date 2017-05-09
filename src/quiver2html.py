#!/usr/bin/env python
from command import parse_args
from parser import ParserFactory

if __name__ == '__main__':
    args = parse_args()
    template = args.template
    output = args.output
    notes = args.notes
    for note in notes:
        ParserFactory.create(note, template.read(), output).parse()

    template.close()

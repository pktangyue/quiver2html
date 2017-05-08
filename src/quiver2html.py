#!/usr/bin/env python
from command import parse_args
from parser import parse

if __name__ == '__main__':
    args = parse_args()
    template = args.template
    output = args.output
    notes = args.notes
    print(template, output, notes)
    for note in notes:
        parse(note, template.read(), output)

    template.close()

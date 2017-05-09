#!/usr/bin/env python
from command import parse_args
from objects import QvFactory

if __name__ == '__main__':
    args = parse_args()
    template = args.template
    output = args.output
    notes = args.notes
    for note in notes:
        QvFactory.create(note).parse(template.read(), output)

    template.close()

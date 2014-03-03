#!/usr/bin/python

"""
Entry point of the application
"""

import sys
from gui.application import application


def main(argv):
    editorApp = application()
    sys.exit(editorApp.run())


if __name__ == "__main__":
    main(sys.argv[1:])


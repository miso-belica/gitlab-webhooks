# -*- coding: utf-8 -*-

"""
Simple server for webhooks of http://gitlab.org/.

Usage:
    glhooks [options] <files>...

Options:
    --port=<port>  Number of port on which server is running. [default: 8000]
    --host=<host>  Host name or IP address of HTTP server. [default: ]
    --help  Shows this text :)

"""

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from docopt import docopt
from . import __version__ as VERSION
from .config import Configs
from . import server


def main():
    args = docopt(__doc__, version=VERSION)
    configs = Configs(*args["<files>"])

    server.start(configs, args["--host"], int(args["--port"]))


if __name__ == "__main__":
    main()

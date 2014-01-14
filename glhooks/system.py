# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import subprocess

from os import chdir
from contextlib import contextmanager


try:
    from os import getcwdu as getcwd
except ImportError:
    from os import getcwd


@contextmanager
def working_directory(path):
    try:
        cwd = getcwd()
        chdir(path)
        yield
    finally:
        chdir(cwd)


def run(*args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

    if process.returncode == 0:
        return process.stdout

    # process terminated with error exit code
    command = " ".join(repr(a) for a in args)
    msg = 'Process exited with code %d: %s' % (process.returncode, command)
    raise Exception(msg, process.stderr)

# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from . import system


class Repository(object):
    DEFAULT_REMOTE = "origin"
    DEFAULT_BRANCH = "master"

    def __init__(self, path):
        self._path = path

    def pull(self, remote=None, branch=None):
        if remote is None:
            remote = self.DEFAULT_REMOTE
        if branch is None:
            branch = self.DEFAULT_BRANCH

        with system.working_directory(self._path):
            self.git("checkout", branch)
            self.git("reset --hard HEAD")
            self.git("pull", remote, branch)

    def git(self, *args):
        if len(args) == 1:  # command as a string
            args = args[0].split()

        args = ["git"] + list(args)
        return system.run(*args)

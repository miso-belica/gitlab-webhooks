# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import re
import logging

from logging.handlers import RotatingFileHandler
from .mailer import SmtpMailer
from .utils import cached_property

try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser


class Configs(object):
    DEFAULT_BRANCH = "master"
    LOGGER_MAX_FILE_SIZE = 16*1024*1024  # in bytes
    LOGGER_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"
    LOGGER_DEFAULT_PATH = "/var/log/glhooks.access.log"
    _REPO_SECTION_PATTERN = re.compile(r"^https?://")

    def __init__(self, *file_paths):
        self._file_paths = file_paths
        self._params = self._parse(file_paths)

    def _parse(self, file_paths):
        parser = SafeConfigParser()

        for path in file_paths:
            parser.read(path)

        data = {
            "server": {
                "log_file": self.LOGGER_DEFAULT_PATH,
            }
        }
        for section in parser.sections():
            section_data = dict(parser.items(section))
            if self._REPO_SECTION_PATTERN.match(section):
                if section.endswith("/"):  # remove ending slash
                    section = section[:-1]
                data[section] = section_data
                data[section]["branch"] = section_data.get("branch", self.DEFAULT_BRANCH)
            else:
                data[section] = section_data

        return data

    def __getitem__(self, key):
        return dict(self._params[key])

    @cached_property
    def mailer(self):
        configs = self["mailer"]
        del configs["sender"]

        return SmtpMailer(**configs)

    @cached_property
    def logger(self):
        return self._build_logger(self["server"]["log_file"])

    def _build_logger(self, log_file_path):
        handler = RotatingFileHandler(log_file_path, maxBytes=self.LOGGER_MAX_FILE_SIZE, backupCount=6)
        handler.setFormatter(logging.Formatter(self.LOGGER_FORMAT))

        logger = logging.getLogger("glhooks")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def find_repo(self, url):
        repo = self._params.get(url)
        if repo is not None:
            repo = dict(repo)

        return repo

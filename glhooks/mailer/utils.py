# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import re

from .compat import string_types, to_unicode


_STRIP_TAGS_PATTERN = re.compile(r"<[^>]+>", re.UNICODE)


def strip_tags(value):
    """
    Strips HTML tags from a string (http://php.net/strip_tags).
    Quick and dirty solution to port the PHP function of the same name :)
    """
    return _STRIP_TAGS_PATTERN.sub("", value.decode("utf-8"))


def format_email_address(address):
    """
    Takes e-mail address in common format (sth@domain.tld) or tuple of
    strings (name, e-mail) and returns e-mail address in format "name <e-mail>".
    """
    if isinstance(address, string_types):
        return to_unicode(address)

    try:
        name, email = tuple(address)
    except (TypeError, ValueError):
        raise ValueError("E-mail address may be only string or pair of strings (name, e-mail).", address)
    else:
        return "%s <%s>" % (to_unicode(name), to_unicode(email))

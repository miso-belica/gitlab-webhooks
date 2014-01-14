# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sys import version_info


PY3 = version_info[0] == 3
_DEFAULT_CHARSET = "utf-8"


if PY3:
    bytes = bytes
    unicode = str

    class_types = type

    def unicode_compatible(cls):
        return cls
else:
    bytes = str
    unicode = unicode

    from types import ClassType
    class_types = (ClassType, type)

    def unicode_compatible(cls):
        cls.__unicode__ = cls.__str__
        if hasattr(cls, "__bytes__"):
            cls.__str__ = cls.__bytes__
            delattr(cls, "__bytes__")
        else:
            cls.__str__ = lambda self: self.__unicode__().encode(_DEFAULT_CHARSET)

        return cls

string_types = (bytes, unicode,)

unicode_compatible.__doc__ = """
    A decorator that defines __unicode__ and __str__ methods under Python 2.
    Under Python 3 it does nothing.

    To support Python 2 and 3 with a single code base, define a __str__ method
    returning text and apply this decorator to the class.
"""


def to_bytes(value, encoding=_DEFAULT_CHARSET, strict=True):
    try:
        if isinstance(value, bytes):
            return value
        elif isinstance(value, unicode):
            return value.encode(encoding)
        else:
            # try encode instance to bytes
            return _instance_to_bytes(value, encoding)
    except UnicodeError:
        if strict:
            raise

        # recover from codec error and use 'repr' function
        return to_bytes(repr(value), encoding)


def to_unicode(value, encoding=_DEFAULT_CHARSET, strict=True):
    try:
        if isinstance(value, unicode):
            return value
        elif isinstance(value, bytes):
            return value.decode(encoding)
        else:
            # try decode instance to unicode
            return _instance_to_unicode(value, encoding)
    except UnicodeError:
        if strict:
            raise

        # recover from codec error and use 'repr' function
        return to_unicode(repr(value), encoding)


# converts value to native string
to_string = to_unicode if PY3 else to_bytes


def _instance_to_bytes(instance, encoding):
    if PY3:
        if hasattr(instance, "__bytes__"):
            return bytes(instance)
        elif hasattr(instance, "__str__"):
            return unicode(instance).encode(encoding)
    else:
        if hasattr(instance, "__str__"):
            return bytes(instance)
        elif hasattr(instance, "__unicode__"):
            return unicode(instance).encode(encoding)

    return to_bytes(repr(instance), encoding)


def _instance_to_unicode(instance, encoding):
    if PY3:
        if hasattr(instance, "__str__"):
            return unicode(instance)
        elif hasattr(instance, "__bytes__"):
            return bytes(instance).decode(encoding)
    else:
        if hasattr(instance, "__unicode__"):
            return unicode(instance)
        elif hasattr(instance, "__str__"):
            return bytes(instance).decode(encoding)

    return to_unicode(repr(instance), encoding)

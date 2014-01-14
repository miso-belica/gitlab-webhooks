# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import mimetypes

from email import encoders
from os.path import basename
from collections import defaultdict
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from .compat import to_unicode, to_string, to_bytes


def _default_payload_builder(content, maintype, subtype, charset):
    payload = MIMEBase(maintype, subtype)
    payload.set_payload(content)
    encoders.encode_base64(payload)

    return payload


class Attachment(object):
    _MIMETYPE_DEFAULT = "application/octet-stream"
    _PAYLOAD_BUILDERS = defaultdict(lambda: _default_payload_builder, {
        "text": lambda c, m, s, ch: MIMEText(c, s, ch),
        "image": lambda c, m, s, ch: MIMEImage(c, s),
        "audio": lambda c, m, s, ch: MIMEAudio(c, s),
        "application": lambda c, m, s, ch: MIMEApplication(c, s),
    })

    def __init__(self, file, charset="utf-8", mimetype=None):
        self._charset = to_string(charset)
        self._file_path = to_unicode(file)
        self._mimetype = to_unicode(self._guess_mimetype(self._file_path, mimetype))

    def _guess_mimetype(self, file_path, force_type):
        if force_type is not None:
            return force_type

        mimetype, _ = mimetypes.guess_type(file_path)
        if mimetype is None:
            mimetype = self._MIMETYPE_DEFAULT

        return mimetype

    @property
    def name(self):
        return basename(self._file_path)

    @property
    def payload(self):
        maintype, subtype = self._mimetype.split("/", 1)
        with open(self._file_path, "rb") as file:
            content = file.read()

        if not content:  # some weird UnicodeError with empty files in v3.2
            content = to_bytes(' ')

        build_payload = self._PAYLOAD_BUILDERS[maintype]
        payload = build_payload(content, to_string(maintype), to_string(subtype), self._charset)
        payload.add_header(to_string("Content-Disposition"), to_string("attachment"), filename=to_string(self.name))

        return payload

    def __repr__(self):
        return to_string("<Attachment [%s]: %s>" % (self._mimetype, self._file_path))

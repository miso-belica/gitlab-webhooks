# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from time import strftime, gmtime
from email.header import make_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .utils import strip_tags, format_email_address
from .attachment import Attachment
from .compat import unicode_compatible, to_unicode, to_string, PY3


@unicode_compatible
class PlainMessage(object):
    """Simple wrapper for data of e-mail message with plain text."""
    _PREAMBLE_TEXT = "This is a multi-part message in MIME format."

    def __init__(self, sender, subject, content, charset="utf-8"):
        self._sender = format_email_address(sender)
        self._charset = to_string(charset)
        self._content = to_unicode(content)
        self._subject = to_unicode(subject)

        self._attachments = []
        self._recipients = {"To": [], "Cc": [], "Bcc": []}

    @property
    def sender(self):
        return self._sender

    @property
    def subject(self):
        return self._subject

    @property
    def recipients(self):
        to = self._recipients["To"]
        cc = self._recipients["Cc"]
        bcc = self._recipients["Bcc"]

        return frozenset(to + cc + bcc)

    def add_recipients(self, *recipients):
        recipients = self._unique_recipients(recipients)
        self._recipients["To"].extend(recipients)

    def add_recipients_cc(self, *recipients):
        recipients = self._unique_recipients(recipients)
        self._recipients["Cc"].extend(recipients)

    def add_recipients_bcc(self, *recipients):
        recipients = self._unique_recipients(recipients)
        self._recipients["Bcc"].extend(recipients)

    def _unique_recipients(self, recipients):
        recipients = map(format_email_address, recipients)
        return frozenset(recipients) - self.recipients

    @property
    def content(self):
        return self._content

    @property
    def payload(self):
        payload = self._build_content_payload(self._content)

        if self._attachments:
            content_payload = payload
            payload = MIMEMultipart("mixed")
            payload.attach(content_payload)
            payload.preamble = self._PREAMBLE_TEXT

        payload = self._set_payload_headers(payload)
        for attachment in self._attachments:
            payload.attach(attachment.payload)

        return payload

    def _build_content_payload(self, content):
        return MIMEText(content.encode(self._charset), "plain", self._charset)

    def _set_payload_headers(self, payload):
        for copy_type, recipients in self._recipients.items():
            for recipient in recipients:
                payload[copy_type] = self._make_header(recipient)

        payload["From"] = self._make_header(self._sender)
        payload["Subject"] = self._make_header(self._subject)
        payload["Date"] = strftime("%a, %d %b %Y %H:%M:%S %z", gmtime())

        return payload

    def _make_header(self, value):
        return make_header([(self._to_string(value), self._charset)])

    def _to_string(self, value):
        if PY3:
            return value
        else:
            return value.encode(self._charset)

    def attach(self, file, charset=None, mimetype=None):
        if charset is None:
            charset = self._charset

        attachment = Attachment(file, charset, mimetype)
        self._attachments.append(attachment)

        return attachment

    if PY3:
        def __str__(self):
            return self.payload.as_string()
    else:
        def __bytes__(self):
            return self.payload.as_string()

    def __repr__(self):
        return to_string("<PlainMessage: %s>" % self.subject)


class HtmlMessage(PlainMessage):
    """Simple wrapper for data of e-mail message with HTML content."""
    def _build_content_payload(self, content):
        content = content.encode(self._charset)
        payload = MIMEMultipart("alternative", charset=self._charset)

        text_alternative = MIMEText(strip_tags(content), "plain", self._charset)
        payload.attach(text_alternative)

        html_alternative = MIMEText(content, "html", self._charset)
        payload.attach(html_alternative)

        return payload

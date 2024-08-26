#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sendcloud_email.mailBody import MailBody
from sendcloud_email.mailReceiver import MailReceiver
from sendcloud_email.textContent import TextContent
from sendcloud_email.validationError import ValidationError


class CommonMail:

    def __init__(self, receiver: MailReceiver, body: MailBody, content: TextContent):
        self.receiver = receiver
        self.body = body
        self.content = content

    def validate_common_email(self):
        if not self.receiver.to and (not self.body.xsmtpapi or not self.body.xsmtpapi.to):
            raise ValidationError("to cannot be empty")

        if not self.body.xsmtpapi or not self.body.xsmtpapi.to or self.receiver.use_address_list:
            self.receiver.validate_receiver()

        if not self.receiver.use_address_list and self.body.xsmtpapi:
            self.body.xsmtpapi.validate_xsmtpapi()

        self.body.validate_mail_body()

        if not self.content.html and not self.content.plain:
            raise ValidationError("html or plain cannot be empty")

    def prepare_send_common_email_params(self, params):
        self.receiver.prepare_mail_receiver_params(params)
        self.body.prepare_mail_body_params(params)
        # Add Content Params
        if self.content.plain:
            params['plain'] = self.content.plain
        if self.content.html:
            params['html'] = self.content.html

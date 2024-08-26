#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

from sendcloud_email.validationError import ValidationError


class MailReceiver:
    def __init__(self, to: Optional[str] = None, cc: Optional[str] = None, bcc: Optional[str] = None, use_address_list: bool = False):
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.use_address_list = use_address_list

    def validate_receiver(self):
        if not self.to:
            raise ValidationError("to cannot be empty")

        if self.use_address_list:
            to_list = self.to.split(';')
            if len(to_list) > 5:
                raise ValidationError("address list exceeds limit")
        else:
            all_addresses = [self.to]
            if self.cc:
                all_addresses.extend(self.cc.split(';'))
            if self.bcc:
                all_addresses.extend(self.bcc.split(';'))
            if len(all_addresses) > 100:
                raise ValidationError("the total number of receivers exceeds the maximum allowed")

    def prepare_mail_receiver_params(self, params):
        if self.to:
            params['to'] = self.to
        if self.cc:
            params['cc'] = self.cc
        if self.bcc:
            params['bcc'] = self.bcc
        if self.use_address_list:
            params['useAddressList'] = str(self.use_address_list).lower()
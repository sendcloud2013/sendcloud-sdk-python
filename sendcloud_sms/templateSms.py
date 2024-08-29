#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from typing import Optional, Dict

from sendcloud_sms.validator import is_valid_msg_type, ValidationError


class TemplateSms:
    def __init__(self, template_id: int, phone: str, msg_type: int = 0, label_id: Optional[int] = None,
                 vars_dict: Optional[Dict[str, str]] = None,
                 send_request_id: Optional[str] = None, tag: Optional[Dict[str, str]] = None):
        self.template_id = template_id
        self.label_id = label_id
        self.msg_type = msg_type
        self.phone = phone
        self.vars_dict = vars_dict
        self.send_request_id = send_request_id
        self.tag = tag

    def validate_phone_numbers(self):
        phone_numbers = self.phone.split(',')
        if len(phone_numbers) > 2000:
            raise ValidationError("the number of mobile phone numbers exceeds the maximum limit of 2,000")
        for number in phone_numbers:
            if number.strip() == "":
                raise ValidationError("phone number can not be empty")

    def validate_template_sms(self):
        if self.template_id == 0:
            raise ValidationError("templateId value is illegal")
        if not is_valid_msg_type(self.msg_type):
            raise ValidationError("msgType value is illegal")
        if len(self.phone) == 0:
            raise ValidationError("phone cannot be empty")
        if self.send_request_id and len(self.send_request_id) > 128:
            raise ValidationError("sendRequestId cannot exceed 128 characters")

    def prepare_send_template_sms_params(self, sms_user):
        params = {
            'smsUser': sms_user,
            'msgType': self.msg_type,
            'phone': self.phone,
            'templateId': self.template_id,
            'timestamp': int(time.time() * 1000),  # 毫秒级时间戳
        }
        if self.vars_dict:
            params['vars'] = json.dumps(self.vars_dict)
        if self.label_id:
            params['labelId'] = self.label_id
        if self.send_request_id:
            params['sendRequestId'] = self.send_request_id
        if self.tag:
            params['tag'] = json.dumps(self.tag)
        return params

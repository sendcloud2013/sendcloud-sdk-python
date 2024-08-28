#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from typing import Optional

from sendcloud_sms.validator import is_valid_msg_type, ValidationError


class CodeSms:
    def __init__(self, msg_type: int, phone: str, sign_id: int, sign_name: str, code: str,
                 label_id: int, send_request_id: Optional[str] = None, tag: Optional[str] = None):
        self.msg_type = msg_type
        self.phone = phone
        self.sign_id = sign_id
        self.sign_name = sign_name
        self.code = code
        self.label_id = label_id
        self.send_request_id = send_request_id
        self.tag = tag

    def validate_code_sms(self):
        if not is_valid_msg_type(self.msg_type):
            raise ValidationError("msgType value is illegal")
        if len(self.phone) == 0:
            raise ValidationError("phone cannot be empty")
        if len(self.code) == 0:
            raise ValidationError("code cannot be empty")
        if len(self.send_request_id) > 128:
            raise ValidationError("sendRequestId cannot exceed 128 characters")

    def prepare_send_code_sms_params(self, sms_user):
        params = {
            'smsUser': sms_user,
            'msgType': self.msg_type,
            'phone': self.phone,
            'code': self.code,
            'timestamp': int(time.time() * 1000),  # 毫秒级时间戳
        }
        if self.sign_id:
            params['signId'] = self.sign_id
        if self.sign_name:
            params['signName'] = self.sign_name
        if self.label_id:
            params['labelId'] = self.label_id
        if self.send_request_id:
            params['sendRequestId'] = self.send_request_id
        if self.tag:
            params['tag'] = json.dumps(self.tag)
        return params

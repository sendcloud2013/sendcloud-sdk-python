#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from typing import Optional

from sendcloud_sms.validator import ValidationError


class VoiceSms:
    def __init__(self, phone: str, code: str, label_id: int, send_request_id: Optional[str] = None,
                 tag: Optional[str] = None):
        self.phone = phone
        self.code = code
        self.label_id = label_id
        self.send_request_id = send_request_id
        self.tag = tag

    def validate_voice_sms(self):
        if len(self.code) == 0:
            raise ValidationError("code cannot be empty")
        if len(self.phone) == 0:
            raise ValidationError("phone cannot be empty")
        if len(self.send_request_id) > 128:
            raise ValidationError("sendRequestId cannot exceed 128 characters")

    def prepare_send_voice_sms_params(self, sms_user):
        params = {
            'smsUser': sms_user,
            'phone': self.phone,
            'code': self.code,
            'timestamp': int(time.time() * 1000),  # 毫秒级时间戳
        }
        if self.label_id:
            params['labelId'] = self.label_id
        if self.send_request_id:
            params['sendRequestId'] = self.send_request_id
        if self.tag:
            params['tag'] = json.dumps(self.tag)
        return params

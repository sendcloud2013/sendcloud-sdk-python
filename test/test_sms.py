#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from sendcloud_sms.codeSms import CodeSms
from sendcloud_sms.sms import SendCloudSms
from sendcloud_sms.templateSms import TemplateSms
from sendcloud_sms.voiceSms import VoiceSms


class TestSendCloudSms(unittest.TestCase):

    def setUp(self):
        self.send_cloud_sms = SendCloudSms("YOUR_API_KEY", "YOUR_SECRET_KEY")


    def test_send_template_sms(self):
        template_sms = TemplateSms(
            template_id=1,
            label_id=1,
            msg_type=1,
            phone="13800138000",
            vars_str="{\"name\": \"John\"}",
            send_request_id="request123",
            tag="tag1"
        )
        result = self.send_cloud_sms.send_template_sms(template_sms)
        print(result.message)



    def test_send_voice_sms(self):
        voice_sms = VoiceSms(
            phone="13800138000",
            code="123456",
            label_id=1,
            send_request_id="request123",
            tag="tag1"
        )
        result = self.send_cloud_sms.send_voice_sms(voice_sms)
        print(result.message)


    def test_send_code_sms(self):
        code_sms = CodeSms(
            msg_type=1,
            phone="13800138000",
            sign_id=1,
            sign_name="TestSign",
            code="123456",
            label_id=1,
            send_request_id="request123",
            tag="tag1"
        )
        result = self.send_cloud_sms.send_code_sms(code_sms)
        print(result.message)


if __name__ == '__main__':
    unittest.main()
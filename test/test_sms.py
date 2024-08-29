#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from sendcloud_sms.codeSms import CodeSms
from sendcloud_sms.sms import SendCloudSms
from sendcloud_sms.templateSms import TemplateSms
from sendcloud_sms.voiceSms import VoiceSms


class TestSendCloudSms(unittest.TestCase):

    def setUp(self):
        self.send_cloud_sms = SendCloudSms("*", "*")

    def test_send_template_sms(self):
        template_sms = TemplateSms(
            template_id=40513,
            phone="13800138000",
            vars_dict={"code": "John"},
            tag={"tag1": "tag1"}
        )
        result = self.send_cloud_sms.send_template_sms(template_sms)
        print(result.message)

    def test_send_voice_sms(self):
        voice_sms = VoiceSms(
            phone="13800138000",
            code="123456",
            tag={"tag1": "tag1"}
        )
        result = self.send_cloud_sms.send_voice_sms(voice_sms)
        print(result.message)

    def test_send_code_sms(self):
        code_sms = CodeSms(
            phone="13800138000",
            sign_name="0516test",
            code="123456",
            tag={"tag1": "tag1"}
        )
        result = self.send_cloud_sms.send_code_sms(code_sms)
        print(result.message)


if __name__ == '__main__':
    unittest.main()

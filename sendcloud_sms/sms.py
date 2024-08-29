#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import json

import requests

from sendcloud_sms.codeSms import CodeSms
from sendcloud_sms.templateSms import TemplateSms
from sendcloud_sms.validator import ValidationError
from sendcloud_sms.voiceSms import VoiceSms


class SendSmsResult:
    def __init__(self, result: bool = None, status_code: int = None, message: str = None, info: object = None,
                 json_data=None):
        if json_data is not None:
            self.result = json_data.get('result', result)
            self.status_code = json_data.get('statusCode', status_code)
            self.message = json_data.get('message', message)
            self.info = json_data.get('info', info)
        else:
            self.result = result
            self.status_code = status_code
            self.message = message
            self.info = info


def handle_response(response):
    if response.status_code == 404:
        return SendSmsResult(False, response.status_code, "Not Found")
    if response.status_code != 200:
        return SendSmsResult(False, response.status_code, "API Error")
    try:
        return SendSmsResult(json_data=response.json())
    except json.JSONDecodeError:
        return SendSmsResult(False, 500, "Invalid JSON response")


class SendCloudSms:
    def __init__(self, sms_user: str, sms_key: str, api_base: str = "https://api.sendcloud.net/smsapi"):
        self.sms_user = sms_user
        self.sms_key = sms_key
        self.api_base = api_base

    def validate_config(self):
        if len(self.sms_user) == 0:
            raise ValidationError("smsUser cannot be empty")
        if len(self.sms_key) == 0:
            raise ValidationError("smsKey cannot be empty")

    def calculate_signature(self, params):
        sorted_params = {k: v for k, v in params.items() if k not in ['smsKey', 'signature']}
        sorted_keys = sorted(sorted_params.keys())
        param_str = '&'.join([f"{k}={v}" for k, v in zip(sorted_keys, [params[k] for k in sorted_keys])])
        sign_str = self.sms_key + '&' + param_str + '&' + self.sms_key
        hasher = hashlib.sha256()
        hasher.update(sign_str.encode('utf-8'))
        signature = hasher.hexdigest()
        return signature

    def send_template_sms(self, template_sms: TemplateSms) -> SendSmsResult:
        send_template_url = self.api_base + "/send"
        try:
            self.validate_config()
            template_sms.validate_template_sms()
            params = template_sms.prepare_send_template_sms_params(self.sms_user)
            signature = self.calculate_signature(params)
            params['signature'] = signature
            response = requests.post(send_template_url, data=params,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
            return handle_response(response)
        except ValidationError as e:
            return SendSmsResult(False, 400, str(e))
        except Exception as e:
            return SendSmsResult(False, 400, f"Error: {str(e)}")

    def send_voice_sms(self, voice_sms: VoiceSms) -> SendSmsResult:
        try:
            self.validate_config()
            voice_sms.validate_voice_sms()
            params = voice_sms.prepare_send_voice_sms_params(self.sms_user)
            signature = self.calculate_signature(params)
            params['signature'] = signature
            send_sms_voice_url = self.api_base + "/sendVoice"  # 假设的路径
            response = requests.post(send_sms_voice_url, data=params,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
            return handle_response(response)
        except ValidationError as e:
            return SendSmsResult(False, 400, str(e))
        except Exception as e:
            return SendSmsResult(False, 400, f"Error: {str(e)}")

    def send_code_sms(self, code_sms: CodeSms) -> SendSmsResult:
        try:
            self.validate_config()
            code_sms.validate_code_sms()
            params = code_sms.prepare_send_code_sms_params(self.sms_user)
            signature = self.calculate_signature(params)
            params['signature'] = signature
            send_sms_code_url = self.api_base + "/sendCode"  # 假设的路径
            response = requests.post(send_sms_code_url, data=params,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
            return handle_response(response)
        except ValidationError as e:
            return SendSmsResult(False, 400, str(e))
        except Exception as e:
            return SendSmsResult(False, 400, f"Error: {str(e)}")

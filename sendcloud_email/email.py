#!/usr/bin/env python
# -*- coding: utf-8 -*-
import contextlib
import json

import os
import requests

from sendcloud_email.calendarMail import CalendarMail
from sendcloud_email.commonMail import CommonMail
from sendcloud_email.templateMail import TemplateMail
from sendcloud_email.validationError import ValidationError


class SendEmailResult:

    def __init__(self, result: bool = None, status_code: int = None, message: str = None, info: object = None, json_data=None):
        if json_data is not None:
            # 从JSON数据初始化
            self.result = json_data.get('result', result)
            self.status_code = json_data.get('statusCode', status_code)
            self.message = json_data.get('message', message)
            self.info = json_data.get('info', info)
        else:
            # 直接从参数初始化
            self.result = result
            self.status_code = status_code
            self.message = message
            self.info = info



class SendCloud:
    def __init__(self, api_user: str, api_key: str, api_base: str = "https://api.sendcloud.net/apiv2/mail"):
        self.api_user = api_user
        self.api_key = api_key
        self.api_base = api_base
        self.client = requests.Session()

    def handle_response(self, response):
        if response.status_code == 404:
            return SendEmailResult(False, response.status_code, "Not Found")
        if response.status_code != 200:
            return SendEmailResult(False, response.status_code, "API Error")
        try:
            return SendEmailResult(json_data=response.json())
        except json.JSONDecodeError:
            return SendEmailResult(False, 500, "Invalid JSON response")

    def validateConfig(self):
        if not self.api_user:
            raise ValidationError("apiUser cannot be empty")
        if not self.api_key:
            raise ValidationError("apiKey cannot be empty")

    def send_common_email(self, mail: CommonMail) -> SendEmailResult:
        send_common_url = self.api_base + "/send"
        try:
            self.validateConfig()
            mail.validate_common_email()
        except ValidationError as e:
            return SendEmailResult(False, 400, e.message)
        params = {
            'apiUser': self.api_user,
            'apiKey': self.api_key,
        }
        mail.prepare_send_common_email_params(params)
        try:
            if mail.body.attachments is None:
                response = requests.post(send_common_url, data=params,
                                         headers={'Content-Type': 'application/x-www-form-urlencoded'})
            else:
                files = [
                    ('attachments', (os.path.basename(filename), open(filename, 'rb'), 'application/octet-stream'))
                    for filename in mail.body.attachments
                ]
                with contextlib.ExitStack() as stack:
                    files = [(name, (basename, stack.enter_context(f), mime_type)) for name, (basename, f, mime_type) in
                             files]
                    response = requests.post(send_common_url, data=params, files=files)
            return self.handle_response(response)
        except Exception as e:
            return SendEmailResult(False, 400, f"Error: {str(e)}")

    def send_template_email(self, mail: TemplateMail) -> SendEmailResult:
        send_template_url = self.api_base + '/sendtemplate'
        try:
            self.validateConfig()
            mail.validate_template_mail()
        except ValidationError as e:
            return SendEmailResult(False, 400, e.message)
        params = {
            'apiUser': self.api_user,
            'apiKey': self.api_key,
        }
        mail.prepare_send_template_email_params(params)
        try:
            if mail.body.attachments is None:
                response = requests.post(send_template_url, data=params,
                                         headers={'Content-Type': 'application/x-www-form-urlencoded'})
            else:
                files = [
                    ('attachments', (os.path.basename(filename), open(filename, 'rb'), 'application/octet-stream'))
                    for filename in mail.body.attachments
                ]
                with contextlib.ExitStack() as stack:
                    files = [(name, (basename, stack.enter_context(f), mime_type)) for name, (basename, f, mime_type) in
                             files]
                    response = requests.post(send_template_url, data=params, files=files)
            return self.handle_response(response)
        except Exception as e:
            return SendEmailResult(False, 400, f"Error: {str(e)}")

    def send_calendar_mail(self, mail: CalendarMail) -> SendEmailResult:
        send_calendar_url = self.api_base + '/sendcalendar'
        try:
            self.validateConfig()
            mail.validate_calendar_mail()
        except ValidationError as e:
            return SendEmailResult(False, 400, str(e))
        params = {
            'apiUser': self.api_user,
            'apiKey': self.api_key,
        }
        mail.prepare_send_calendar_mail_params()
        try:
            if mail.body.attachments is None:
                response = requests.post(send_calendar_url, data=params,
                                         headers={'Content-Type': 'application/x-www-form-urlencoded'})
            else:
                files = [
                    ('attachments', (os.path.basename(filename), open(filename, 'rb'), 'application/octet-stream'))
                    for filename in mail.body.attachments
                ]
                with contextlib.ExitStack() as stack:
                    files = [(name, (basename, stack.enter_context(f), mime_type)) for name, (basename, f, mime_type) in
                             files]
                    response = requests.post(send_calendar_url, data=params, files=files)
            return self.handle_response(response)
        except Exception as e:
            return SendEmailResult(False, 400, f"Error: {str(e)}")

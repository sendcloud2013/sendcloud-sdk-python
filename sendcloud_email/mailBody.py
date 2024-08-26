#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, Optional, List, Union

import json

from sendcloud_email.validationError import ValidationError


class XSMTPAPI:
    def __init__(self,
                 to: Optional[List[str]] = None,
                 sub: Optional[Dict[str, List[Union[str, int, float, bool, dict, list]]]] = None,
                 pubsub: Optional[Dict[str, Union[str, int, float, bool, dict, list]]] = None,
                 filters: Optional['Filter'] = None,
                 settings: Optional['Settings'] = None):
        self.to = to
        self.sub = sub
        self.pubsub = pubsub
        self.filters = filters
        self.settings = settings

    def validate_xsmtpapi(self):
        if self.to:
            if len(self.to) > 100:
                raise ValidationError("the total number of receivers exceeds the maximum allowed")

            if len(self.sub) != len(self.to):
                raise ValidationError("Number of Sub values does not match To addresses")

        if self.to and self.sub and isinstance(self.sub, dict):
            for k in self.sub.keys():
                if not (k.startswith('%') and k.endswith('%')):
                    raise ValidationError(f"the key needs to be in the format '%%...%%'; [{k}] does not satisfy this "
                                          f"condition")

        if self.pubsub and isinstance(self.pubsub, dict):
            for k in self.pubsub.keys():
                if not (k.startswith('%') and k.endswith('%')):
                    raise ValidationError(f"the key needs to be in the format '%%...%%'; [{k}] does not satisfy this "
                                          f"condition")
        if self.filters:
            self.filters.validate_filter()

    def to_dict(self):
        return {
            'to': self.to,
            'sub': self.sub,
            'pubsub': self.pubsub,
            'filters': self.filters.to_dict() if self.filters is not None else None,
            'settings': self.settings.to_dict() if self.settings is not None else None
        }


class FilterSettings:
    def __init__(self, enable: str):
        self.enable = enable

    def to_dict(self):
        return {'enable': self.enable}


class TrackingFilter:
    def __init__(self, settings: 'FilterSettings'):
        self.settings = settings

    def to_dict(self):
        return {'settings': self.settings.to_dict()}


class Filter:
    def __init__(self,
                 subscription_tracking: Optional['TrackingFilter'] = None,
                 open_tracking: Optional['TrackingFilter'] = None,
                 click_tracking: Optional['TrackingFilter'] = None):
        self.subscription_tracking = subscription_tracking
        self.open_tracking = open_tracking
        self.click_tracking = click_tracking

    def validate_filter(self):
        if self.subscription_tracking.settings.enable not in ["0", "1"]:
            raise ValidationError("subscriptionTracking invalid value for Enable, must be '0' or '1'")
        if self.open_tracking.settings.enable not in ["0", "1"]:
            raise ValidationError("openTracking invalid value for Enable, must be '0' or '1'")
        if self.click_tracking.settings.enable not in ["0", "1"]:
            raise ValidationError("clickTracking invalid value for Enable, must be '0' or '1'")

    def to_dict(self):
        return {
            'subscription_tracking': self.subscription_tracking.to_dict() if self.subscription_tracking is not None else None,
            'open_tracking': self.open_tracking.to_dict() if self.open_tracking is not None else None,
            'click_tracking': self.click_tracking.to_dict() if self.click_tracking is not None else None
        }


class UnsubscribeSettings:
    def __init__(self, page_id: List[int]):
        self.page_id = page_id

    def to_dict(self):
        return {'page_id': self.page_id}


class Settings:
    def __init__(self, unsubscribe: 'UnsubscribeSettings'):
        self.unsubscribe = unsubscribe

    def to_dict(self):
        return {'unsubscribe': self.unsubscribe.to_dict()}


class MailBody:
    def __init__(self, from_email: str, subject: str,
                 from_name: Optional[str] = None,
                 reply_to: Optional[str] = None,
                 label_name: Optional[str] = None,
                 headers: Optional[Dict[str, str]] = None,
                 attachments: Optional[List[str]] = None,
                 content_summary: Optional[str] = None,
                 xsmtpapi: Optional[XSMTPAPI] = None,
                 send_request_id: Optional[str] = None,
                 resp_email_id: bool = False,
                 use_notification: bool = False):
        self.from_email = from_email
        self.subject = subject
        self.content_summary = content_summary
        self.from_name = from_name
        self.reply_to = reply_to
        self.label_name = label_name
        self.headers = headers
        self.attachments = attachments
        self.xsmtpapi = xsmtpapi
        self.send_request_id = send_request_id
        self.resp_email_id = resp_email_id
        self.use_notification = use_notification

    def validate_mail_body(self):
        if not self.from_email:
            raise ValidationError("from cannot be empty")
        if not self.subject:
            raise ValidationError("subject cannot be empty")

    def prepare_mail_body_params(self, params):
        params['from'] = self.from_email
        params['subject'] = self.subject
        if self.content_summary:
            params['contentSummary'] = self.content_summary
        if self.from_name:
            params['fromName'] = self.from_name
        if self.reply_to:
            params['replyTo'] = self.reply_to
        if self.label_name:
            params['labelName'] = self.label_name
        if self.headers:
            params['headers'] = json.dumps(self.headers)
        if self.xsmtpapi:
            params['xsmtpapi'] = json.dumps(self.xsmtpapi.to_dict())
        if self.send_request_id:
            params['sendRequestId'] = self.send_request_id
        if self.resp_email_id:
            params['respEmailId'] = str(self.resp_email_id)
        if self.use_notification:
            params['useNotification'] = str(self.use_notification)

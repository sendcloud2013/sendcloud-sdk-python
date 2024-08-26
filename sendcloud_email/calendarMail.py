#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sendcloud_email.mailBody import MailBody
from sendcloud_email.mailCalendar import MailCalendar
from sendcloud_email.mailReceiver import MailReceiver
from sendcloud_email.textContent import TextContent
from sendcloud_email.validationError import ValidationError


class CalendarMail:

    def __init__(self, receiver: MailReceiver, body: MailBody, content: TextContent, calendar: MailCalendar):
        self.receiver = receiver
        self.body = body
        self.content = content
        self.calendar = calendar

    def validate_calendar_mail(self):
        if not self.receiver.to and (not self.body.xsmtpapi or not self.body.xsmtpapi.to):
            raise ValidationError("to cannot be empty")

        if not self.body.xsmtpapi or not self.body.xsmtpapi.to or self.receiver.use_address_list:
            self.receiver.validate_receiver()

        if not self.receiver.use_address_list and self.body.xsmtpapi:
            self.body.xsmtpapi.validate_xsmtpapi()

        self.body.validate_mail_body()

        self.calendar.validate_mail_calendar()

    def prepare_send_calendar_mail_params(self, params):
        self.receiver.prepare_mail_receiver_params(params)
        self.body.prepare_mail_body_params(params)
        params['startTime'] = self.calendar.start_time.strftime("%Y-%m-%d %H:%M:%S")
        params['endTime'] = self.calendar.end_time.strftime("%Y-%m-%d %H:%M:%S")
        params['title'] = self.calendar.title
        params['organizerName'] = self.calendar.organizer_name
        params['organizerEmail'] = self.calendar.organizer_email
        params['location'] = self.calendar.location
        params['participatorNames'] = self.calendar.participator_names
        # Add Content Params
        if self.content.plain:
            params['plain'] = self.content.plain
        if self.content.html:
            params['html'] = self.content.html

        if self.calendar.description:
            params["description"] = self.calendar.description

        if self.calendar.participator_emails:
            params["participatorEmails"] = self.calendar.participator_emails

        if self.calendar.uid:
            params["uid"] = self.calendar.uid

        if self.calendar.is_cancel:
            params["isCancel"] = str(self.calendar.is_cancel).lower()

        if self.calendar.is_update:
            params["isUpdate"] = str(self.calendar.is_update).lower()

        if self.calendar.valarm_time:
            params["valarmTime"] = str(self.calendar.valarm_time)
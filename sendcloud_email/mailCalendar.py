#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from typing import Optional

from sendcloud_email.validationError import ValidationError


class MailCalendar:

    def __init__(self,
                 start_time: datetime,
                 end_time: datetime,
                 title: str,
                 organizer_name: str,
                 organizer_email: str,
                 location: str,
                 participator_names: str,
                 description: Optional[str] = None,
                 participator_emails: Optional[str] = None,
                 uid: Optional[str] = None,
                 is_cancel: bool = False,
                 is_update: bool = False,
                 valarm_time: Optional[int] = None):
        self.start_time = start_time
        self.end_time = end_time
        self.title = title
        self.organizer_name = organizer_name
        self.organizer_email = organizer_email
        self.location = location
        self.description = description
        self.participator_names = participator_names
        self.participator_emails = participator_emails
        self.uid = uid
        self.is_cancel = is_cancel
        self.is_update = is_update
        self.valarm_time = valarm_time

    def validate_mail_calendar(self):
        if self.start_time is None:
            raise ValidationError("startTime cannot be empty")
        if self.end_time is None:
            raise ValidationError("endTime cannot be empty")
        if self.start_time > self.end_time:
            raise ValidationError("startTime cannot be after endTime")
        if not self.title:
            raise ValidationError("title cannot be empty")
        if not self.organizer_name:
            raise ValidationError("organizerName cannot be empty")
        if not self.organizer_email:
            raise ValidationError("organizerEmail cannot be empty")
        if not self.location:
            raise ValidationError("location cannot be empty")
        if not self.participator_names:
            raise ValidationError("participatorNames cannot be empty")


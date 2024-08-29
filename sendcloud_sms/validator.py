#!/usr/bin/env python
# -*- coding: utf-8 -*-

SMS = 0
MMS = 1
INTERNAT_SMS = 2
VOICE = 3
QR_CODE = 4
YX = 5


def is_valid_msg_type(msg_type):
    return msg_type in [SMS, MMS, INTERNAT_SMS, VOICE, QR_CODE, YX]


class ValidationError(Exception):

    def __init__(self, message):
        """

        :rtype: object
        """
        self.message = message
        super().__init__(self.message)

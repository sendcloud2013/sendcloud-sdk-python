#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ValidationError(Exception):

    def __init__(self, message):
        """

        :rtype: object
        """
        self.message = message
        super().__init__(self.message)

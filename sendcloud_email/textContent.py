#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional


class TextContent:
    def __init__(self, html: Optional[str] = None, plain: Optional[str] = None):
        self.html = html
        self.plain = plain

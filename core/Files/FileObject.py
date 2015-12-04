# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

class FileObject:
    def __init__(self, data):
        self.data = data
        self.name = 'unknown'
        self.source = 'unknown'
        self.destination = 'unknown'
        self.timestamp = 'unknown'
        self.type = 'unknown'
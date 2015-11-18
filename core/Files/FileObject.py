# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

class FileObject:
    def __init__(self, name, data, source = 'unknown', destination = 'unknown', timestamp = 'unknown'):
        self.name = name
        self.data = data
        self.source = source
        self.destination = destination
        self.timestamp = timestamp
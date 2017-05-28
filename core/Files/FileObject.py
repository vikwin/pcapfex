# -*- coding: utf8 -*-
import hashlib

__author__ = 'Viktor Winkelmann'

import datetime

class FileObject(object):
    def __init__(self, data):
        self.data = data
        self.md5 = hashlib.md5(data)
        self._name = None
        self.source = 'unknown'
        self.destination = 'unknown'
        self.pcapFile = 'unknown'
        self._timestamp = 'unknown'
        self.type = 'unknown'
        self.fileEnding = 'unknown'
        self.firstPacketNumber = None

    @property
    def name(self):
        if self._name:
            return self._name
        else:
            return self.type.split('/')[-1]

    @name.setter
    def name(self, value):
        self._name = value


    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        try:
            self._timestamp = str(datetime.datetime.utcfromtimestamp(value)).replace(':', '-')
        except ValueError:
            self._timestamp = value
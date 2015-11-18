# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from abc import ABCMeta, abstractmethod

class ProtocolDissector:
    __metaclass__ = ABCMeta

    priority = 50

    @abstractmethod
    def getProtocolName(cls):
        """ IMPORTANT: Override as Class Method (using @classmethod) """
        return NotImplemented

    @abstractmethod
    def parseData(cls, data):
        """ IMPORTANT: Override as Class Method (using @classmethod) """
        return NotImplemented

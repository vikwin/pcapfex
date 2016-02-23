# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from abc import ABCMeta, abstractmethod
from Plugin import *

class Decoder(Plugin):
    __metaclass__ = ABCMeta

    @classmethod
    def getPriority(cls):
        return cls.basePriority

    @abstractmethod
    def getDecoderName(cls):
        """ IMPORTANT: Override as Class Method (using @classmethod) """
        return NotImplemented

    @abstractmethod
    def decodeData(cls, data):
        """ IMPORTANT: Override as Class Method (using @classmethod) """
        return NotImplemented

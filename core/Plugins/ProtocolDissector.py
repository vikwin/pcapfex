# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from abc import ABCMeta, abstractmethod, abstractproperty
from Plugin import *

class ProtocolDissector(Plugin):
    __metaclass__ = ABCMeta
    defaultPorts = []
    
    @abstractproperty
    def protocolName(cls):
        """ IMPORTANT: Override as Class Property """
        return NotImplemented

    @classmethod
    def getPriority(cls, streamPorts = ()):
        if any(map(lambda x: x in cls.defaultPorts, streamPorts)):
            return cls.basePriority - 50

        return cls.basePriority
        
    @abstractmethod
    def parseData(cls, data):
        """ IMPORTANT: Override as Class Method (using @classmethod) """
        return NotImplemented

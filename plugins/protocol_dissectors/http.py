# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys
sys.path.append('../..')
from core.Plugins.ProtocolDissector import *

def getClassReference():
    return HTTP

class HTTP(ProtocolDissector):

    @classmethod
    def getProtocolName(cls):
        return "HTTP"

    @classmethod
    def parseData(cls, data):
        pass    # TODO
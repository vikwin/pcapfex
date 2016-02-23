# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.ProtocolDissector import *


def getClassReference():
    return Unknown


class Unknown(ProtocolDissector):
    basePriority = 200

    protocolName = "unknown protocol"

    @classmethod
    def parseData(cls, data):
        return [data]

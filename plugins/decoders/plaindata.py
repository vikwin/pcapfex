# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.Decoder import *


def getClassReference():
    return PlainData


class PlainData(Decoder):
    basePriority = 10

    decoderName = "plain data"

    @classmethod
    def decodeData(cls, data):
        return data
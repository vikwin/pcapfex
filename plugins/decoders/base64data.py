# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys
import base64

sys.path.append('../..')
from core.Plugins.Decoder import *


def getClassReference():
    return Base64Decoder


class Base64Decoder(Decoder):
    decoderName = "base64"

    @classmethod
    def decodeData(cls, data):
        #allowedChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/\r\n\t "
        #for char in data:
        #    if char not in allowedChars:
        #        return None

        try:
            return base64.b64decode(data)
        except TypeError:
            return None

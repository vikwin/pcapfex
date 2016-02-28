# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return PNGFile


class PNGFile(DataRecognizer):
    signatures = [(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', b'\x49\x45\x4E\x44\xAE\x42\x60\x82')]
    fileEnding = "png"
    dataType = "PNG file"
    dataCategory = DataCategory.IMAGE

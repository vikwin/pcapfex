# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return MPGFile


class MPGFile(DataRecognizer):
    signatures = [(b'\x00\x00\x01[\xB0-\xBF]', b'\x00\x00\x01[\xB7\xB9]')]
    fileEnding = "mpg"
    dataType = "MPEG file"
    dataCategory = DataCategory.VIDEO
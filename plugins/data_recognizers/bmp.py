# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return BMPFile


class BMPFile(SimpleDataRecognizer):
    signatures = [(b'\x42\x4D', None)]
    fileEnding = "bmp"
    dataType = "Bitmap file"
    dataCategory = DataCategory.IMAGE

# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return BMPFile


class BMPFile(DataRecognizer):
    signatures = [(b'\x42\x4D.{4}\x00\x00\x00\x00', None)]
    fileEnding = "bmp"
    dataType = "Bitmap file"
    dataCategory = DataCategory.IMAGE

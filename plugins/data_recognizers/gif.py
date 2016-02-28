# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return GIFFile


class GIFFile(DataRecognizer):
    signatures = [(b'\x47\x49\x46\x38[\x37\x39]\x61', b'\x00\x3B')]
    fileEnding = "gif"
    dataType = "GIF file"
    dataCategory = DataCategory.IMAGE

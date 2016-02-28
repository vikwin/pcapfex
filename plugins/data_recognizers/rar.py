# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return RARFile


class RARFile(DataRecognizer):
    signatures = [(b'\x52\x61\x72\x21\x1A\x07', None)]
    fileEnding = "rar"
    dataType = "RAR file"
    dataCategory = DataCategory.COMPRESSED
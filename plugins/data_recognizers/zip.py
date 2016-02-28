# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return ZipFile


class ZipFile(DataRecognizer):
    signatures = [(b'\x50\x4B\x03\x04', None)]
    fileEnding = "zip"
    dataType = "ZIP file"
    dataCategory = DataCategory.COMPRESSED
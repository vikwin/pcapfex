# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return MKVFile


class MKVFile(DataRecognizer):
    signatures = [(b'\x1A\x45\xDF\xA3.{4}matroska', None)]
    fileEnding = "mpg"
    dataType = "MKV file"
    dataCategory = DataCategory.VIDEO
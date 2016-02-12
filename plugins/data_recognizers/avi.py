# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return AviFile


class AviFile(SimpleDataRecognizer):
    signatures = [(b'\x52\x49\x46\x46.{4}\x41\x56\x49\x20\x4C\x49\x53\x54', None)]
    fileEnding = "avi"
    dataType = "AVI file"
    dataCategory = DataCategory.VIDEO
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return JpegFile


class JpegFile(DataRecognizer):
    signatures = [(b'\xFF\xD8\xFF', b'\xFF\xD9'), (b'.{6}\x4A\x46\x49\x46\x00', None)]
    fileEnding = "jpg"
    dataType = "JPEG file"
    dataCategory = DataCategory.IMAGE

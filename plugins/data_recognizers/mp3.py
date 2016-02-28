# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return MP3File


class MP3File(DataRecognizer):
    signatures = [('ID3', None)]
    fileEnding = "mp3"
    dataType = "MP3 file"
    dataCategory = DataCategory.AUDIO
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return WAVFile


class WAVFile(DataRecognizer):
    signatures = [(b'RIFF.{4}WAVEfmt', None)]
    fileEnding = "wav"
    dataType = "WAV file"
    dataCategory = DataCategory.AUDIO
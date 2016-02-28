# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return ELFFile


class ELFFile(DataRecognizer):
    signatures = [(b'\x7F\x45\x4C\x46', None)]
    fileEnding = ""
    dataType = "ELF file"
    dataCategory = DataCategory.EXECUTABLE

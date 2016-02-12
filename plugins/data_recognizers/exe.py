# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return EXEFile


class EXEFile(SimpleDataRecognizer):
    signatures = [('MZ', None)]
    fileEnding = "exe"
    dataType = "DOS/Windows Executable file"
    dataCategory = DataCategory.EXECUTABLE

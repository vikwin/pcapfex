# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
from core.Plugins.DataRecognizer import *


def getClassReference():
    return PDFFile


class PDFFile(DataRecognizer):
    signatures = [(b'\x25\x50\x44\x46', b'.*\x25\x25\x45\x4F\x46[(\x0A)(\x0D)(\x0D\x0A)]?')]
    fileEnding = "pdf"
    dataType = "PDF file"
    dataCategory = DataCategory.DOC

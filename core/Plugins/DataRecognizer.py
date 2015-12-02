# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from abc import ABCMeta, abstractproperty


class DataCategory:
    IMAGE = "Image file"
    VIDEO = "Video file"
    AUDIO = "Audio file"
    DOC = "Document file"
    TEXT = "Plaintext file"

    COMPRESSED = "Compressed file"
    ENCRYPTED = "Encrypted file"
    UNKNOWN = "Unknown data"

    def __iter__(self):
        return self.__dict__.__iter__()


class SimpleDataRecognizer:
    __metaclass__ = ABCMeta

    priority = 50

    @abstractproperty
    def fileHeader(cls):
        """ IMPORTANT: Override as Class Property """
        return NotImplemented

    @abstractproperty
    def fileTrailer(cls):
        """ IMPORTANT: Override as Class Property """
        return NotImplemented

    @abstractproperty
    def fileEnding(cls):
        """ IMPORTANT: Override as Class Property """
        return NotImplemented

    @abstractproperty
    def dataType(cls):
        """ IMPORTANT: Override as Class Property """
        return NotImplemented

    @abstractproperty
    def dataCategory(cls):
        """ IMPORTANT: Override as Class Property """
        return NotImplemented

    @classmethod
    def findNextOccurence(cls, data, startindex=0, endindex=None):
        if endindex is None:
            endindex = len(data) - 1

        occstart = data.find(cls.fileHeader, startindex, endindex)
        if occstart < 0:
            return None

        occend = None
        if cls.fileTrailer:
            # noinspection PyTypeChecker
            occend = data.rfind(cls.fileTrailer, occstart + len(cls.fileHeader), endindex)

        return (occstart, occend)
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from abc import ABCMeta, abstractproperty
import re


class DataCategory:
    IMAGE = "Image file"
    VIDEO = "Video file"
    AUDIO = "Audio file"
    DOC = "Document file"
    TEXT = "Plaintext file"
    EXECUTABLE = "Executable file"

    COMPRESSED = "Compressed file"
    ENCRYPTED = "Encrypted file"
    UNKNOWN = "Unknown data"

    def __iter__(self):
        return self.__dict__.__iter__()


class SimpleDataRecognizer:
    __metaclass__ = ABCMeta

    basePriority = 50

    @classmethod
    def getPriority(cls):
        return cls.basePriority


    @abstractproperty
    def signatures(cls):
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
    def _buildRegexPattern(cls, fileHeader, fileTrailer):
        if fileTrailer is None:
            str = b'%s.*' % (fileHeader,)
        else:
            str = b'%s.*?%s' % (fileHeader, fileTrailer)

        return re.compile(str, re.DOTALL)

    @classmethod
    def findNextOccurence(cls, data, startindex=0, endindex=0):
        if endindex == 0:
            endindex = len(data)

        for (fileHeader, fileTrailer) in cls.signatures:
            regex = cls._buildRegexPattern(fileHeader, fileTrailer)
            match = regex.search(data, startindex, endindex)
            if match:
                return match.span()

        return None

    @classmethod
    def findAllOccurences(cls, data, startindex=0, endindex=0):
        occurences = []
        while startindex < len(data):
            occurence = cls.findNextOccurence(data, startindex, endindex)
            if occurence is None:
                return occurences

            occurences.append(occurence)
            (_, startindex) = occurence

        return occurences
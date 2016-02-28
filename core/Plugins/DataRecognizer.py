# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from abc import ABCMeta, abstractproperty
from Plugin import *
try:
    import regex as re
    print 'Using concurrency enabled regex module.'
except:
    print 'Consider installing the \'regex\' module using \'pip install regex\' to improve performance on multicore systems.'
    import re

#from pympler import tracker

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


class DataRecognizer(Plugin):
    __metaclass__ = ABCMeta

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
    def _buildRegexPatterns(cls):
        regexstr = b''
        for (fileHeader, fileTrailer) in cls.signatures:   
            if fileTrailer is None:
                regexstr += b'(%s.*)|' % (fileHeader,)
            else:
                regexstr += b'(%s.*?%s)|' % (fileHeader, fileTrailer)
       
        cls._regex = re.compile(regexstr[:-1], re.DOTALL)

    @classmethod
    def findNextOccurence(cls, data, startindex=0, endindex=0):
        if not hasattr(cls, '_regex'):
            cls._buildRegexPatterns()
            
        if endindex == 0:
            endindex = len(data)

        match = cls._regex.search(data, startindex, endindex)
       
        return match.span() if match else None

    @classmethod
    def findAllOccurences(cls, data, startindex=0, endindex=0):
        if not hasattr(cls, '_regex'):
            cls._buildRegexPatterns()
        
        if endindex == 0:
            endindex = len(data)

        #tr = tracker.SummaryTracker()
        occurences = [m.span() for m in cls._regex.finditer(data, startindex, endindex)]

        #tr.print_diff()
        return occurences

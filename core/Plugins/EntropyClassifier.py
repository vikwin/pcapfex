# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'
import math

class EntropyClass:
    PLAIN = 'rawdata/plain file'
    COMPRESSED = 'rawdata/compressed file'
    ENCRYPTED = 'rawdata/encrypted file'
    UNCATEGORIZED = 'rawdata/uncategorized file'

class EntropyClassifier:
    RANDOM_ENTROPY = 7.9
    CHI2_LOWER_BOUND = 206
    CHI2_UPPER_BOUND = 311

    MINIMUM_DATA_LENGTH = 256 * 5
    MAXIMUM_DATA_LENGTH = 1024 * 100

    @classmethod
    def classify(cls, data):
        data = data[:cls.MAXIMUM_DATA_LENGTH]
        l = len(data)
        if l < cls.MINIMUM_DATA_LENGTH:
            return EntropyClass.UNCATEGORIZED

        h = cls._histogram(data)
        s = cls._shannonEntropy(h, l)

        if s >= cls.RANDOM_ENTROPY:
            c = cls._chiSquare(h, l)
            if c > cls.CHI2_LOWER_BOUND and c < cls.CHI2_UPPER_BOUND:
                return EntropyClass.ENCRYPTED
            else:
                return EntropyClass.COMPRESSED

        else:
            return EntropyClass.PLAIN

    @classmethod
    def _shannonEntropy(cls, histogram, datalength):
        return abs(reduce(lambda acc,x: acc + (x/datalength) * math.log(x/datalength, 2) if x > 0 else  acc + x,
                          histogram, 0))

    @classmethod
    def _chiSquare(cls, histogram, datalength):
        exp = float(datalength) / 256
        return reduce(lambda acc,x: acc + ((x-exp)**2)/exp, histogram, 0)

    @classmethod
    def _histogram(cls, data):
        h = [0.0] * 256
        for char in data:
            h[ord(char)] += 1.0
        return h
#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
import unittest, zlib, random
from core.Plugins.EntropyClassifier import *
from Crypto.Cipher import AES, ARC4

class TestEntropyClassifier(unittest.TestCase):
    def setUp(self):
        self.text = '''
        Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore
        et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
        Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet,
        consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
        sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea
        takimata sanctus est Lorem ipsum dolor sit amet.
        ''' * 16

        randomData = ''.join(chr(random.randint(0, 255)) for _ in range(5000))

        self.zip6 = zlib.compress(self.text + randomData, 6)
        self.zip9 = zlib.compress(self.text + randomData, 9)

        pwd = '0123456789ABCDEF'
        aes = AES.new(pwd, AES.MODE_CBC, IV='\x42'*16)
        arc4 = ARC4.new(pwd)
        print len(self.text)
        self.enc1 = aes.encrypt(self.text)
        self.enc2 = arc4.encrypt(self.text)


    def test_classifier(self):
        self.assertRaises(DataLengthException, EntropyClassifier.classify, 'Too short')
        self.assertEqual(EntropyClass.PLAIN, EntropyClassifier.classify(self.text))
        self.assertEqual(EntropyClass.COMPRESSED, EntropyClassifier.classify(self.zip6))
        self.assertEqual(EntropyClass.COMPRESSED, EntropyClassifier.classify(self.zip9))
        self.assertEqual(EntropyClass.ENCRYPTED, EntropyClassifier.classify(self.enc1))
        self.assertEqual(EntropyClass.ENCRYPTED, EntropyClassifier.classify(self.enc2))


if __name__ == '__main__':
    unittest.main()
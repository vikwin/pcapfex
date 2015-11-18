#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys
sys.path.append('../..')
import unittest

from core.Streams.StreamBuilder import *


class TestZipExtract(unittest.TestCase):
    def setUp(self):
        inputfile = 'zipdownload.pcap'
        self.zipfile = 'testfile.zip'

        self.builder = StreamBuilder(inputfile)

        self.zipheader = b'\x50\x4B\x03\x04'

        self.testfile = open(self.zipfile, 'rb')

    def tearDown(self):
        self.testfile.close()

    def test_tcp_streams(self):
        self.assertEqual(len(self.builder.tcpStreams), 2)
        self.assertEqual(len(self.builder.tcpStreams[0]), 1)
        self.assertEqual(len(self.builder.tcpStreams[1]), 1032)

    def test_extract_zip(self):
        targetdata = self.testfile.read()
        zipstream = self.builder.tcpStreams[1]

        zipindex = zipstream.getFirstBytes(1024).find(self.zipheader)
        zipfile = zipstream.getAllBytes()[zipindex:]
        self.assertEqual(zipindex, 276)
        self.assertEqual(targetdata, zipfile)


if __name__ == '__main__':
    unittest.main()
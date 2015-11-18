#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
import unittest
from core.Streams.StreamBuilder import *
from core.Plugins.PluginManager import *


class TestZipExtract(unittest.TestCase):
    def setUp(self):
        inputfile = 'zipdownload.pcap'
        self.zipfile = 'testfile.zip'

        self.builder = StreamBuilder(inputfile)

        self.pm = PluginManager()
        self.zipplugin = self.pm.dataRecognizers["zip"]

        self.testfile = open(self.zipfile, 'rb')

    def tearDown(self):
        self.testfile.close()

    def test_extract_zip(self):
        targetdata = self.testfile.read()
        streamdata = self.builder.tcpStreams[1].getAllBytes()

        zipindices = self.zipplugin.findNextOccurence(streamdata, 0, 1024)
        zipfile = streamdata[zipindices[0]:]
        self.assertEqual(targetdata, zipfile)


if __name__ == '__main__':
    unittest.main()

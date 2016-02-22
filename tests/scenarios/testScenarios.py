#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys

sys.path.append('../..')
import unittest

from core.Dispatcher import Dispatcher
import shutil
import os


class TestScenarios(unittest.TestCase):
    OUTPUT_PATH = 'tmp_testscenarios'

    @classmethod
    def findFile(cls, target):
        foundFiles = []
        for root, dirs, files in os.walk(cls.OUTPUT_PATH):
            for file in files:
                with open(os.path.join(root, file), 'rb') as f:
                    foundFiles.append(f.read())

        return target in foundFiles

    def setUp(self):
        if os.path.exists(self.OUTPUT_PATH):
            shutil.rmtree(self.OUTPUT_PATH)

    def tearDown(self):
        if os.path.exists(self.OUTPUT_PATH):
            shutil.rmtree(self.OUTPUT_PATH)

    def test_scenario4_1(self):
        target = open('4.1/file.zip', 'rb').read()

        d = Dispatcher('4.1/4.1.pcap', self.OUTPUT_PATH, verifyChecksums=False)
        d.run()
        self.assertTrue(self.findFile(target))

    def test_scenario4_2(self):
        target = open('4.2/file.jpg', 'rb').read()

        d = Dispatcher('4.2/4.2.pcap', self.OUTPUT_PATH, verifyChecksums=False)
        d.run()
        self.assertTrue(self.findFile(target))

    def test_scenario4_3(self):
        target = open('4.3/file.pdf', 'rb').read()

        d = Dispatcher('4.3/4.3.pcap', self.OUTPUT_PATH, verifyChecksums=False)
        d.run()
        self.assertTrue(self.findFile(target))

    def test_scenario4_4(self):
        target = open('4.4/file.mp3', 'rb').read()

        d = Dispatcher('4.4/4.4.pcap', self.OUTPUT_PATH, verifyChecksums=False)
        d.run()
        self.assertTrue(self.findFile(target))

    def test_scenario4_5(self):
        target = open('4.5/file.mp3', 'rb').read()

        d = Dispatcher('4.5/4.5.pcap', self.OUTPUT_PATH, verifyChecksums=False)
        d.run()
        self.assertTrue(self.findFile(target))


    def test_scenario4_6(self):
        target = open('4.6/file.aes', 'rb').read()

        d = Dispatcher('4.6/4.6.pcap', self.OUTPUT_PATH, True, verifyChecksums=False)
        d.run()

        h = 'this is the header!(§$%113550987'
        t = 'TRAILER_'
        self.assertTrue(self.findFile(h + target + t))


if __name__ == '__main__':
    unittest.main()
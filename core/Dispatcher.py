# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import multiprocessing
from multiprocessing import Pool, Lock
from Files.FileManager import *
from Streams.StreamBuilder import *
from Plugins.PluginManager import *

class Dispatcher():
    def __init__(self, pcapfile):
        self.pcapfile = pcapfile
        self.filemanager = FileManager()
        self.pluginmanager = PluginManager()
        self.resultLock = Lock()
        self.printLock = Lock()


    def _lockedPrint(self, output):
        with self.printLock.acquire():
            print output

    def _finishedSearch(self, (streaminfos, result)):
        with self.resultLock.acquire():
                print "Found %d files in stream %s" % (len(result), streaminfos)
                map(self.filemanager.addFile, result)

    def run(self):
        streambuilder = StreamBuilder(self.pcapfile)
        allstreams = streambuilder.tcpStreams + streambuilder.udpStreams
        workers = Pool(processes=multiprocessing.cpu_count())
        workers.map_async(self._findFiles, allstreams, 1, self._finishedSearch)


    def _findFiles(self, stream):
        files = []




        return (stream.infos, files)


if __name__ == '__main__':
    d = Dispatcher('../tests/zipextract/zipdownload.pcap')
    d.run()
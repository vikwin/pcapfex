# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import multiprocessing
from ThreadPool.Pool import Pool
from threading import Lock
from Files.FileManager import *
from Streams.StreamBuilder import *
from Plugins.PluginManager import *

class Dispatcher():
    def __init__(self, pcapfile):
        self.pcapfile = pcapfile
        self.filemanager = FileManager()
        self.pm = PluginManager()
        self.printLock = Lock()
        self.resultLock = Lock()


    def _lockedPrint(self, output):
        with self.printLock:
            print output

    def _finishedSearch(self, (streaminfos, result)):
        with self.resultLock:
                print "Found %d files in stream %s" % (len(result), streaminfos)
                map(self.filemanager.addFile, result)

    def run(self):
        streambuilder = StreamBuilder(self.pcapfile)
        allstreams = streambuilder.tcpStreams + streambuilder.udpStreams

        print "File %s has a total of %d single-direction streams." % (self.pcapfile, len(allstreams))

        workers = Pool(multiprocessing.cpu_count())
        workers.map_async(self._findFiles, allstreams, self._finishedSearch)
        workers.join()

        print "Search has finished."


    def _findFiles(self, stream):
        files = []

        self.zipplugin = self.pm.dataRecognizers["zip"]
        streamdata = stream.getAllBytes()
        zipindices = self.zipplugin.findNextOccurence(streamdata, 0, 1024)

        if not zipindices is None:
            files.append(streamdata[zipindices[0]:])

        return (stream.infos, files)


if __name__ == '__main__':
    d = Dispatcher('../tests/zipextract/zipdownload.pcap')
    d.run()
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import multiprocessing
from ThreadPool.Pool import Pool
from threading import Lock
from Files.FileManager import *
from Files.FileObject import *
from Streams.StreamBuilder import *
from Plugins.PluginManager import *
from Plugins.EntropyClassifier import DataLengthException

class Dispatcher:
    def __init__(self, pcapfile, outputdir='output', entropy=False):
        self.pcapfile = pcapfile
        self.filemanager = FileManager(outputdir)
        self.pm = PluginManager()
        self.printLock = Lock()
        self.resultLock = Lock()
        self.outputdir = outputdir
        self.useEntropy = entropy


    def _lockedPrint(self, output):
        with self.printLock:
            print output

    def _finishedSearch(self, (stream, result)):
        with self.resultLock:
                print "Found %d files in %s stream %s" % (len(result), stream.protocol, stream.infos)
                map(self.filemanager.addFile, result)

    def run(self):
        if os.path.exists(self.outputdir):
            print "Output folder \'%s\' already exists! Exiting..." % self.outputdir,
            self.filemanager.exit()
            return

        streambuilder = StreamBuilder(self.pcapfile)
        allstreams = streambuilder.tcpStreams + streambuilder.udpStreams

        print "File %s has a total of %d single-direction streams." % (self.pcapfile, len(allstreams))

        workers = Pool(multiprocessing.cpu_count())
        #workers = Pool(1)  # for debugging only
        workers.map_async(self._findFiles, allstreams, self._finishedSearch)
        workers.join()

        print "Data search has finished."
        self.filemanager.exit()



    def _findFiles(self, stream):
        files = []
        payloads= []
        streamdata = stream.getAllBytes()
        streamPorts = (stream.ipSrc, stream.ipDst)

        for protocol in self.pm.getProtocolsByHeuristics(streamPorts):
            payloads = self.pm.protocolDissectors[protocol].parseData(streamdata)

            if payloads is not None:
                stream.protocol = self.pm.protocolDissectors[protocol].getProtocolName()
                break

        for encPayload in payloads:
            for decoder in self.pm.decoders:
                payload = self.pm.decoders[decoder].decodeData(encPayload)
                if payload is None:
                    continue


                for datarecognizer in self.pm.dataRecognizers:
                    for occ in self.pm.dataRecognizers[datarecognizer].findAllOccurences(payload):
                        file = FileObject(payload[occ[0]:occ[1]])
                        file.source = stream.ipSrc
                        file.destination = stream.ipDst
                        file.fileEnding = self.pm.dataRecognizers[datarecognizer].fileEnding
                        file.type = self.pm.dataRecognizers[datarecognizer].dataCategory
                        if stream.tsFirstPacket:
                            file.timestamp = stream.tsFirstPacket
                        files.append(file)

                if self.useEntropy:
                    try:
                        type = self.pm.entropyClassifier.classify(payload)
                        file = FileObject(payload)
                        file.source = stream.ipSrc
                        file.destination = stream.ipDst
                        file.type = type
                        if stream.tsFirstPacket:
                            file.timestamp = stream.tsFirstPacket
                        files.append(file)
                    except DataLengthException:
                        pass

        return (stream, files)

if __name__ == '__main__':
    d = Dispatcher(os.path.dirname(__file__) + '/../tests/webextract/web_light.pcap')
    d.run()
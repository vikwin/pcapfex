# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'
import os, imp
from collections import OrderedDict
from EntropyClassifier import EntropyClassifier


class PluginManager:
    PD_PATH = '/../../plugins/protocol_dissectors/'
    DR_PATH = '/../../plugins/data_recognizers/'
    DC_PATH = '/../../plugins/decoders/'

    def __init__(self):
        modulepath = os.path.dirname(__file__)
        self.protocolDissectors = OrderedDict()
        self.dataRecognizers = OrderedDict()
        self.decoders = OrderedDict()
        self.entropyClassifier = EntropyClassifier()
        self.__loadPlugins(modulepath + self.__class__.PD_PATH, self.protocolDissectors)
        self.__loadPlugins(modulepath + self.__class__.DR_PATH, self.dataRecognizers)
        self.__loadPlugins(modulepath + self.__class__.DC_PATH, self.decoders)

        self.protocolDissectors = OrderedDict(
            sorted(self.protocolDissectors.iteritems(), key=lambda x: x[1].getPriority()))
        self.dataRecognizers = OrderedDict(
            sorted(self.dataRecognizers.iteritems(), key=lambda x: x[1].getPriority()))
        self.decoders = OrderedDict(
            sorted(self.decoders.iteritems(), key=lambda x: x[1].getPriority()))


    def getProtocolsByHeuristics(self, streamPorts):
        return OrderedDict(
            sorted(self.protocolDissectors.iteritems(), key=lambda x: x[1].getPriority(streamPorts)))

    def __loadPlugins(self, path, targetdict):
        for pluginfile in os.listdir(path):
            if not os.path.isfile(path + pluginfile):
                continue
            if not pluginfile[-3:] == ".py":
                continue
            if pluginfile.endswith("__init__.py"):
                continue

            name = pluginfile.split('/')[-1][:-3]
            module = imp.load_source(name, path + pluginfile)
            targetdict[name] = module.getClassReference()

            
if __name__ == "__main__":
    pm = PluginManager()
    print pm.protocolDissectors['http11'].getPriority()

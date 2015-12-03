# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'
import os, imp
from collections import OrderedDict


class PluginManager:
    PD_PATH = '/../../plugins/protocol_dissectors/'
    DR_PATH = '/../../plugins/data_recognizers/'

    def __init__(self):
        modulepath = os.path.dirname(__file__)
        self.protocolDissectors = OrderedDict()
        self.dataRecognizers = OrderedDict()
        self.__loadPlugins(modulepath + self.__class__.PD_PATH, self.protocolDissectors)
        self.__loadPlugins(modulepath + self.__class__.DR_PATH, self.dataRecognizers)

        self.protocolDissectors = OrderedDict(
            sorted(self.protocolDissectors.iteritems(), key=lambda x: x[1].priority))
        self.dataRecognizers = OrderedDict(
            sorted(self.dataRecognizers.iteritems(), key=lambda x: x[1].priority))


    def __loadPlugins(self, path, targetdict):
        for pluginfile in os.listdir(path):
            if not os.path.isfile(path + pluginfile):
                continue
            if not pluginfile[-3:] == ".py":
                continue

            name = pluginfile.split('/')[-1][:-3]
            module = imp.load_source(name, path + pluginfile)
            targetdict[name] = module.getClassReference()


if __name__ == "__main__":
    pm = PluginManager()
    print pm.protocolDissectors['http'].priority

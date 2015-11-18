# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'
import os, imp


class PluginManager:
    PD_PATH = '../../plugins/protocol_dissectors/'
    DR_PATH = '../../plugins/data_recognizers/'

    def __init__(self):
        self.protocolDissectors = dict()
        self.dataRecognizers = dict()
        self.__loadPlugins(self.__class__.PD_PATH, self.protocolDissectors)
        self.__loadPlugins(self.__class__.DR_PATH, self.dataRecognizers)

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

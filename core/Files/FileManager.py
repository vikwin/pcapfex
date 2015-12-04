# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import os

class FileManager:
    def __init__(self):
        self.files = []

    def __iter__(self):
        return self.files.__iter__()

    def addFile(self, file):
        self.files.append(file)

    def writeAllFiles(self, outputdir):
        for file in self.files:
            path = "%s/%ss/%s_%s/" % (outputdir, file.type, file.source, file.destination)
            if not os.path.exists(path):
                os.makedirs(path)

            number = 1
            filename = '%s %d.%s' % (file.name, number, file.fileEnding)

            while os.path.exists(path + filename):
                number += 1
                filename = '%s %d.%s' % (file.name, number, file.fileEnding)

            with open(path + filename, 'wb') as outfile:
                outfile.write(file.data)
                print "Wrote file: " + path + filename
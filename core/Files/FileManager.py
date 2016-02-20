# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import os
from Queue import Queue
from threading import Thread

class FileManager(Thread):
    def __init__(self, outputdir):
        Thread.__init__(self)
        self.files = Queue()
        self.outputdir = outputdir
        self.stop = False
        self.start()

    def addFile(self, file):
        self.files.put(file)

    def exit(self):
        self.files.join()
        self.stop = True
        self.files.put(None)

    def run(self):
        while not self.stop or not self.files.empty():
            file = self.files.get()

            if not file:
                self.files.task_done()
                continue

            path = "%s/%ss/%s_%s/%s/" % (self.outputdir, file.type, file.source, file.destination, file.timestamp)
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

            self.files.task_done()
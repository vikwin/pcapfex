# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from threading import Thread
import Queue

class Worker(Thread):
    def __init__(self, id, tasks):
        Thread.__init__(self)
        self.setName('Workerthread %d' % (id,))
        self.tasks = tasks
        self.daemon = True
        self.stop = False

    def run(self):
        while not self.stop:
            try:
                (func, object, callback) = self.tasks.get_nowait()
                callback(func(object))
            except Queue.Empty:
                self.stop = True
            except Exception as ex:
                print ex
                self.stop = True

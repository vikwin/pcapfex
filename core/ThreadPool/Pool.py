# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from Queue import Queue
from Worker import Worker

class Pool:
    def __init__(self, size):
        self.size = size
        self.workers = []
        self.tasks = Queue()

    def _removeDeadWorkers(self):
        self.workers = [w for w in self.workers if w.isAlive()]

    def map_async(self, func, objects, callback):
        self._removeDeadWorkers()
        if not len(self.workers) == 0:
            raise Exception('ThreadPool is still working! Adding new jobs is not allowed!')

        for object in objects:
            self.tasks.put((func, object, callback))

        for id in range(self.size):
            self.workers.append(Worker(id, self.tasks))

        for worker in self.workers:
            worker.start()

    def join(self):
        for worker in self.workers:
            worker.join()
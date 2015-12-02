# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

class FileManager:
    def __init__(self):
        self.files = []

    def __iter__(self):
        return self.files.__iter__()

    def addFile(self, file):
        self.files.append(file)

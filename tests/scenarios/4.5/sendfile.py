# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from socket import *

CHUNKSIZE = 1400

with open('file.mp3', 'rb') as inputfile:
    s = socket(AF_INET, SOCK_DGRAM)

    data = inputfile.read(CHUNKSIZE)
    while data != '':
        s.sendto(data, ('192.168.123.37', 4242))
        data = inputfile.read(CHUNKSIZE)

    s.close()







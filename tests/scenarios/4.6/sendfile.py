# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from socket import socket

with open('file.aes', 'rb') as inputfile:
    data = inputfile.read()

    h = 'this is the header!(§$%113550987'
    t = 'TRAILER_'

    s = socket()
    s.connect(('192.168.123.37', 4242))
    s.sendall(h + data + t)
    s.close()

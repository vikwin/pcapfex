# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import base64
from socket import socket

with open('file.mp3', 'rb') as inputfile:
    data = inputfile.read()
    b64data = base64.b64encode(data)

    s = socket()
    s.connect(('192.168.123.37', 4242))
    s.sendall(b64data)
    s.close()

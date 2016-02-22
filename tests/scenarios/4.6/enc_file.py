# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from Crypto.Cipher import AES

PASSWORD='0123456789ABCDEF'

with open('orig_file.exe', 'rb') as input:
    with open('file.aes', 'wb') as output:
        aes = AES.new(PASSWORD, AES.MODE_CBC, '\x00'*16)
        data = input.read()
        while len(data) % 16 != 0:
            data += '\x00'
        output.write(aes.encrypt(data))
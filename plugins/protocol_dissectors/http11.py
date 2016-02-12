# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys
sys.path.append('../..')

from core.Plugins.ProtocolDissector import *
from cStringIO import StringIO
from contextlib import closing

def getClassReference():
    return HTTP11

# Parses HTTP Requests / Responses according to http://tools.ietf.org/html/rfc7230
class HTTP11(ProtocolDissector):
    defaultPorts = [80, 8080, 8000, 443]

    @classmethod
    def getProtocolName(cls):
        return "HTTP 1.1"

    @classmethod
    def getRequestPayload(cls, data):
        return None #TODO

    @classmethod
    def getResponsePayload(cls, data):
        headers = cls.parseHeaders(data)
        if 'Content-Length' in headers:
            length = int(headers['Content-Length'])
            return data.read(length)

        #TODO Bei anderen Feldkonstellationen Payload liefern
        return None

    @classmethod
    def parseHeaders(cls, data):
        headers = dict()
        line = data.readline()
        while line not in ['\r\n','']:
            keyval = line.split(':')
            headers[keyval[0].strip()] = keyval[1].strip()
            line = data.readline()
        return headers

    @classmethod
    def parseData(cls, data):
        with closing(StringIO(data)) as data:
            # check start line for HTTP 1.1 tag
            line = data.readline()
            if 'HTTP/1.1' not in line:
                return None

            payloads = []

            #loop to allow HTTP pipelining
            while line != '':
                # classify as Request or Response
                if line.startswith('HTTP'):
                    payload = cls.getResponsePayload(data)
                else:
                    payload = cls.getRequestPayload(data)

                if payload:
                    payloads.append(payload)

                line = data.readline()
            return payloads










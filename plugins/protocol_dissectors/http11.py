# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import sys
sys.path.append('../..')

from core.Plugins.ProtocolDissector import *
from cStringIO import StringIO
from contextlib import closing
from gzip import GzipFile

def getClassReference():
    return HTTP11


# Parses HTTP Requests / Responses according to http://tools.ietf.org/html/rfc7230
class HTTP11(ProtocolDissector):
    defaultPorts = [80, 8080, 8000, 443]

    decoders = {
        'gzip':     lambda x: GzipFile(fileobj=StringIO(x)).read(),
        'x-gzip':   lambda x: GzipFile(fileobj=StringIO(x)).read(),
        'deflate':  lambda x: x.decode('zlib'),
    }

    protocolName = "HTTP 1.1"

    @classmethod
    def getRequestPayload(cls, data):
        return cls.getResponsePayload(data)     # No special case found yet that has to be handled differently

    @classmethod
    def decode(cls, payload, encoding):
        if not payload:
            return None

        if encoding not in cls.decoders.keys():
            return payload

        try:
            return cls.decoders[encoding](payload)
        except Exception as e:
            return payload

    @classmethod
    def getResponsePayload(cls, data):
        payload = None
        encoding = None
        headers = cls.parseHeaders(data)
        if 'Content-Length' in headers:
            length = int(headers['Content-Length'])
            payload = data.read(length)

        if 'Content-Encoding' in headers:
            encoding = headers['Content-Encoding']
            encoding = encoding.split(':')[-1].strip().lower()

        if 'Transfer-Encoding' in headers:
            encoding = headers['Transfer-Encoding']
            encoding = encoding.split(':')[-1].strip().lower()

        return cls.decode(payload, encoding)

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










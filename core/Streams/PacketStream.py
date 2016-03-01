# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'
from abc import ABCMeta, abstractmethod


class PacketStream:
    __metaclass__ = ABCMeta

    def __init__(self, ipSrc, portSrc, ipDst, portDst):
        self.ipSrc = ipSrc
        self.portSrc = portSrc
        self.ipDst = ipDst
        self.portDst = portDst
        self.infos = "%s:%s to %s:%s" % (ipSrc, portSrc, ipDst, portDst)
        self.protocol = 'unknown protocol'
        self.tsFirstPacket = None
        self.tsLastPacket = None
        self.closed = False

    # def __eq__(self, other):
    #     if other is None:
    #         return False
    #     if not isinstance(other, self.__class__):
    #         return False
    #     return self.ipSrc == other.ipSrc \
    #         and self.portSrc == other.portSrc \
    #         and self.ipDst == other.ipDst \
    #         and self.portDst == other.portDst \
    #
    # def __ne__(self, other):
    #     return not self.__eq__(other)
    #
    # def __hash__(self):
    #     return (str(self.ipSrc) + str(self.portSrc) + str(self.ipDst) + str(self.portDst)).__hash__()

    @abstractmethod
    def getAllBytes(self):
        return NotImplemented

    @abstractmethod
    def getFirstBytes(self, count):
        return NotImplemented

    @abstractmethod
    def addPacket(self, packet, ts):
        return NotImplemented
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from PacketStream import *
import dpkt

class UDPStream(PacketStream):
    def __init__(self, ipSrc, portSrc, ipDst, portDst, tsFirstPacket = None):
        PacketStream.__init__(self, ipSrc, portSrc, ipDst, portDst, tsFirstPacket)

        self.packets = []

    def addPacket(self, packet):
        if type(packet) != dpkt.udp.UDP:
            raise TypeError('Packet is no UDP packet!')

        self.packets.append(packet)

    def __iter__(self):
        return iter(self.packets)

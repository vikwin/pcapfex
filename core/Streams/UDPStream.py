# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from PacketStream import *
import dpkt

class UDPStream(PacketStream):
    def __init__(self, ipSrc, portSrc, ipDst, portDst):
        PacketStream.__init__(self, ipSrc, portSrc, ipDst, portDst)

        self.packets = []
        self.tsLastPacket = None

    def addPacket(self, packet, ts):
        if type(packet) != dpkt.udp.UDP:
            raise TypeError('Packet is no UDP packet!')

        if len(packet.data) == 0:
            return

        if len(self.packets) == 0:
            self.tsFirstpacket = ts

        self.packets.append(packet)
        self.tsLastPacket = ts

    def __iter__(self):
        return iter(self.packets)

    def getFirstBytes(self, count):
        bytes = b''
        index = 0
        while len(bytes) < count and index < len(self.packets):
            bytes += self.packets[index].data
            index += 1
        return bytes[:count]

    def getAllBytes(self):
        bytes = b''
        for packet in self.packets:
            bytes += packet.data
        return bytes

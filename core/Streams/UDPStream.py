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

        if len(self.packets) == 0:
            pass    # TODO: Zeitstempel herausfinden und setzen

        self.packets.append(packet)

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
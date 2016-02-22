# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

from cStringIO import StringIO
from contextlib import closing
from PacketStream import *
import dpkt

class TCPStream(PacketStream):
    def __init__(self, ipSrc, portSrc, ipDst, portDst):
        PacketStream.__init__(self, ipSrc, portSrc, ipDst, portDst)

        self.packets = dict()

    def __len__(self):
        return len(self.packets)

    def addPacket(self, packet, ts):
        if type(packet) != dpkt.tcp.TCP:
            raise TypeError('Packet is not a TCP packet!')

        if len(packet.data) == 0:
            return

        if packet.seq not in self.packets:
            self.packets[packet.seq] = packet

        if self.tsFirstPacket is None or ts < self.tsFirstPacket:
            self.tsFirstPacket = ts

        if self.tsLastPacket is None or ts > self.tsLastPacket:
            self.tsLastPacket = ts


    def __iter__(self):
        sortedPackets = sorted(self.packets.items(), key=lambda kv: kv[0])
        for k,v in sortedPackets:
            yield v

    def getFirstBytes(self, count):
        with closing(StringIO()) as bytes:
            index = 0
            sortedPackets = sorted(self.packets.items(), key=lambda kv: kv[0])
            while len(bytes) < count and index < len(sortedPackets):
                bytes.write(sortedPackets[index][1].data)
                index += 1

            return bytes.getvalue()[:count]

    def getAllBytes(self):
        with closing(StringIO()) as bytes:
            for (seq, packet) in sorted(self.packets.items(), key=lambda kv: kv[0]):
                bytes.write(packet.data)

            return bytes.getvalue()


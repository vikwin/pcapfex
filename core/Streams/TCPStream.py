# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'
from PacketStream import *
import dpkt
from collections import OrderedDict

class TCPStream(PacketStream):
    def __init__(self, ipSrc, portSrc, ipDst, portDst, tsFirstPacket = None):
        PacketStream.__init__(self, ipSrc, portSrc, ipDst, portDst, tsFirstPacket)

        self.packets = OrderedDict()

    def __len__(self):
        return len(self.packets)

    def addPacket(self, packet):
        if type(packet) != dpkt.tcp.TCP:
            raise TypeError('Packet is not a TCP packet!')

        # Pakete ohne Payload werden hier ignoriert, so kann es nicht passieren dass ein leeres ACK mit
        # einer zuvor bereits genutzen Sequenznummer Daten "überschreibt"
        if len(packet.data) > 0:
            self.packets[packet.seq] = packet


    def __iter__(self):
        sortedPackets = sorted(self.packets.items(), key=lambda kv: kv[0])
        for k,v in sortedPackets:
            yield v

    # def getFirstBytes(self, count):
    #     bytes = bytearray()
    #     index = 0
    #     sortedPackets = sorted(self.packets.items(), key=lambda kv: kv[0])
    #     while len(bytes) < count and index < len(sortedPackets):
    #         bytes = bytes.join(sortedPackets[index][1].data)
    #         index += 1
    #
    #     return bytes[:count]

    def getFirstBytes(self, count):
        bytes = b''
        index = 0
        sortedPackets = sorted(self.packets.items(), key=lambda kv: kv[0])
        while len(bytes) < count and index < len(sortedPackets):
            bytes += sortedPackets[index][1].data
            index += 1

        return bytes[:count]

    def getAllBytes(self):
        bytes = b''
        for (seq, packet) in sorted(self.packets.items(), key=lambda kv: kv[0]):
            bytes += packet.data

        return bytes


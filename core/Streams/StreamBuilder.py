# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'


from TCPStream import *
from UDPStream import *
import socket

class StreamBuilder:
    def __init__(self, pcapfile = None):
        self.tcpStreams = []
        self.udpStreams = []
        self.__parsePcapfile(pcapfile)

    def __parsePcapfile(self, pcapfile):
        if pcapfile is None:
            return

        with open(pcapfile) as pcap:
            packets = dpkt.pcap.Reader(pcap)
            for ts, rawpacket in packets:
                eth = dpkt.ethernet.Ethernet(rawpacket)
                if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                    continue

                ip = eth.data
                packet = ip.data
                if ip.p == dpkt.ip.IP_PROTO_TCP:
                    tcpStream = TCPStream(socket.inet_ntoa(ip.src), packet.sport,
                                          socket.inet_ntoa(ip.dst), packet.dport)
                    if tcpStream not in self.tcpStreams:
                        self.tcpStreams.append(tcpStream)

                    index = self.tcpStreams.index(tcpStream)
                    self.tcpStreams[index].addPacket(packet)

                elif ip.p == dpkt.ip.IP_PROTO_UDP:
                    udpStream = UDPStream(socket.inet_ntoa(ip.src), packet.sport,
                                          socket.inet_ntoa(ip.dst), packet.dport)
                    if udpStream not in self.udpStreams:
                        self.udpStreams.append(udpStream)

                    index = self.udpStreams.index(udpStream)
                    self.udpStreams[index].addPacket(packet)

                else:
                    continue
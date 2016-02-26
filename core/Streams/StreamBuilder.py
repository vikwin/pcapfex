# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'


from TCPStream import *
from UDPStream import *
import socket
import os
import sys
import dpkt

# Workaround to get access to pcap packet record capture length field
def myIter(self):
    while 1:
        buf = self._Reader__f.read(dpkt.pcap.PktHdr.__hdr_len__)
        if not buf:
            break
        hdr = self._Reader__ph(buf)
        buf = self._Reader__f.read(hdr.caplen)
        yield (hdr.tv_sec + (hdr.tv_usec / 1000000.0), hdr.caplen == hdr.len, buf)

class StreamBuilder:
    def __init__(self, pcapfile = None, **kwargs):
        self.tcpStreams = []
        self.udpStreams = []
        self.UDP_TIMEOUT = 120
        self.VERIFY_CHECKSUMS = True   # Might need to be disabled if Checksum Offloading
                                        # was used on the capturing NIC

        if 'udpTimeout' in kwargs:
            self.UDP_TIMEOUT = kwargs['udpTimeout']

        if 'verifyChecksums' in kwargs:
            self.VERIFY_CHECKSUMS = kwargs['verifyChecksums']

        self.__parsePcapfile(pcapfile)


    # Verify Layer3/4 Checksums, see dpkt/ip.py __str__ method
    @classmethod
    def __verify_checksums(cls, ippacket):
        if dpkt.in_cksum(ippacket.pack_hdr() + str(ippacket.opts)) != 0:
            return False

        if (ippacket.off & (dpkt.ip.IP_MF | dpkt.ip.IP_OFFMASK)) != 0:
            return True

        p = str(ippacket.data)
        s = dpkt.struct.pack('>4s4sxBH', ippacket.src, ippacket.dst,
                             ippacket.p, len(p))
        s = dpkt.in_cksum_add(0, s)
        s = dpkt.in_cksum_add(s, p)
        return dpkt.in_cksum_done(s) == 0

    def __parsePcapfile(self, pcapfile):
        if pcapfile is None:
            return


        with open(pcapfile, 'rb') as pcap:
            dpkt.pcap.Reader.__iter__ = myIter
            packets = dpkt.pcap.Reader(pcap)
            caplenError = False

            fsize = float(os.path.getsize(pcapfile))
            progress = -1

            print '  Size of file %s: %.2f mb' % (pcapfile, fsize / 1000000)
            for ts, complete, rawpacket in packets:

                if not complete:
                    caplenError = True


                pos = int((pcap.tell() / fsize) * 100)
                if pos > progress:
                    sys.stdout.write("\r\t%d%%" % (pos,))
                    sys.stdout.flush()
                    progress = pos

                eth = dpkt.ethernet.Ethernet(rawpacket)
                if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                    continue

                ip = eth.data

                if self.VERIFY_CHECKSUMS and not self.__verify_checksums(ip):
                    continue

                packet = ip.data
                if ip.p == dpkt.ip.IP_PROTO_TCP:

                    tcpStream = TCPStream(socket.inet_ntoa(ip.src), packet.sport,
                                          socket.inet_ntoa(ip.dst), packet.dport)
                    if tcpStream not in self.tcpStreams:
                        if not (packet.flags & dpkt.tcp.TH_SYN) != 0:
                            continue
                        self.tcpStreams.append(tcpStream)

                    # get index of last stream occurence
                    index = len(self.tcpStreams) - 1 - self.tcpStreams[::-1].index(tcpStream)

                    if not self.tcpStreams[index].closed:
                        self.tcpStreams[index].addPacket(packet, ts)
                        if (packet.flags & dpkt.tcp.TH_FIN) != 0:
                            if self.tcpStreams[index].isValid():
                                self.tcpStreams[index].closed = True
                            else:
                                del self.tcpStreams[index]

                elif ip.p == dpkt.ip.IP_PROTO_UDP:
                    udpStream = UDPStream(socket.inet_ntoa(ip.src), packet.sport,
                                          socket.inet_ntoa(ip.dst), packet.dport)
                    udpStream.tsFirstPacket = ts

                    if udpStream not in self.udpStreams:
                        self.udpStreams.append(udpStream)

                    # get index of last stream occurence
                    index = len(self.udpStreams) - 1 - self.udpStreams[::-1].index(udpStream)

                    lastSeen = self.udpStreams[index].tsLastPacket
                    if lastSeen and (ts - lastSeen) > self.UDP_TIMEOUT:
                        self.udpStreams[index].closed = True
                        self.udpStreams.append(udpStream)
                        index = -1

                    self.udpStreams[index].addPacket(packet, ts)

                else:
                    continue

            if caplenError:
                print '\nWarning: Packet loss due to too small capture length!'


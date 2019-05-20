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
    while True:
        buf = self._Reader__f.read(dpkt.pcap.PktHdr.__hdr_len__)
        if not buf:
            break
        else:
            try:
                hdr = self._Reader__ph(buf)
            except:
                print(' > Finish with error')
                break
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

            openTcpStreams = []
            openUdpStreams = []
            badPackets, firstError, lastError = 0, 0, 0

            print '  Size of file %s: %.2f mb' % (pcapfile, fsize / 1000000)
            for packetNumber, (ts, complete, rawpacket) in enumerate(packets, 1):

                if not complete:
                    caplenError = True


                pos = int((pcap.tell() / fsize) * 100)
                if pos > progress:
                    sys.stdout.write("\r\t%d%%" % (pos,))
                    sys.stdout.flush()
                    progress = pos
                    #if progress > 15: break

                try:
                    eth = dpkt.ethernet.Ethernet(rawpacket)
                except:
                    if packetNumber > lastError:
                        lastError = packetNumber
                        badPackets = badPackets + 1
                        if not firstError:
                            firstError = packetNumber
                    sys.stdout.write("\r\t%d%% < Bad packet %d (%d)" % (pos, packetNumber, badPackets,))
                    sys.stdout.flush()
                    continue

                if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                    continue

                ip = eth.data

                if self.VERIFY_CHECKSUMS and not self.__verify_checksums(ip):
                    continue

                packet = ip.data
                if ip.p == dpkt.ip.IP_PROTO_TCP:

                    # get last matching stream occurrence for packet
                    tcpStream = self.__findLastStreamOccurenceIn(openTcpStreams,
                                                                 ip.src, packet.sport,
                                                                 ip.dst, packet.dport)

                    # no matching open stream found, create new stream if syn flag is set
                    if tcpStream is None:
                        if not packet.flags & dpkt.tcp.TH_SYN:
                            continue

                        tcpStream = TCPStream(socket.inet_ntoa(ip.src), packet.sport,
                                              socket.inet_ntoa(ip.dst), packet.dport, packetNumber, pcapfile)
                        openTcpStreams.append(tcpStream)

                    # add packet to currently referenced stream
                    tcpStream.addPacket(packet, ts)

                    # check if stream needs to be closed due to fin flag and verify stream
                    if packet.flags & dpkt.tcp.TH_FIN:
                        if tcpStream.isValid():
                            tcpStream.closed = True
                            self.tcpStreams.append(tcpStream)
                        openTcpStreams.remove(tcpStream)


                elif ip.p == dpkt.ip.IP_PROTO_UDP:
                    if len(packet.data) == 0:
                        continue

                    #get last matching stream occurrence for packet
                    udpStream = self.__findLastStreamOccurenceIn(openUdpStreams,
                                                             ip.src, packet.sport,
                                                             ip.dst, packet.dport)


                    # no matching open stream found, create new stream
                    if udpStream is None or udpStream.closed:
                        udpStream = UDPStream(socket.inet_ntoa(ip.src), packet.sport,
                                              socket.inet_ntoa(ip.dst), packet.dport, packetNumber, pcapfile)
                        openUdpStreams.append(udpStream)

                    else:
                        lastSeen = udpStream.tsLastPacket

                        # timeout happened, close old and create new stream
                        if lastSeen and (ts - lastSeen) > self.UDP_TIMEOUT:
                            udpStream.closed = True
                            openUdpStreams.remove(udpStream)
                            self.udpStreams.append(udpStream)

                            udpStream = UDPStream(socket.inet_ntoa(ip.src), packet.sport,
                                                  socket.inet_ntoa(ip.dst), packet.dport, packetNumber, pcapfile)
                            openUdpStreams.append(udpStream)

                    # add packet to currently referenced udpStream
                    udpStream.addPacket(packet, ts)
                else:
                    continue

            self.tcpStreams += filter(lambda s: s.isValid(), openTcpStreams)
            self.udpStreams += openUdpStreams

            if caplenError:
                print '\nWarning: Packet loss due to too small capture length!'
            if badPackets:
                print '\nWarning: %d bad packets between %d and %d.' % (badPackets, firstError, lastError)

    def __findLastStreamOccurenceIn(cls, list, ipSrc, portSrc, ipDst, portDst):
        for stream in list[::-1]:
            if stream.portSrc == portSrc \
                    and stream.portDst == portDst \
                    and stream.ipSrc == socket.inet_ntoa(ipSrc) \
                    and stream.ipDst == socket.inet_ntoa(ipDst):

                    return stream

        return None

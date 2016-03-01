#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import argparse
from core.Dispatcher import Dispatcher

VERSION = "1.0"

parser = argparse.ArgumentParser(description='Extract files from a pcap-file.')
parser.add_argument('input', metavar='PCAP_FILE', help='the input file')
parser.add_argument('output', metavar='OUTPUT_FOLDER', help='the target folder for extraction',
                    nargs='?', default='output')
parser.add_argument("-e", dest='entropy', help="use entropy based rawdata extraction",
                    action="store_true", default=False)
parser.add_argument("-nv", dest='verifyChecksums', help="disable IP/TCP/UDP checksum verification",
                    action="store_false", default=True)
parser.add_argument("--T", dest='udpTimeout', help="set timeout for UDP-stream heuristics",
                    type=int, default=120)


print 'pcapfex - Packet Capture Forensic Evidence Extractor - version %s' % (VERSION,)
print '----------=------===-----=--------=---------=------------------' + '-'*len(VERSION) + '\n'
args = parser.parse_args()

if not args.verifyChecksums:
    print 'Packet checksum verification disabled.'
if args.entropy:
    print 'Using entropy and statistical analysis for raw extraction and classification of unknown data.'


dispatcher = Dispatcher(args.input, args.output, args.entropy,
                        verifyChecksums=args.verifyChecksums,
                        udpTimeout=args.udpTimeout,
                        )
dispatcher.run()

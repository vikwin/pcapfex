#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import argparse
from core.Dispatcher import Dispatcher

VERSION = "0.1"

parser = argparse.ArgumentParser(description='Extract files from a pcap-file.')
parser.add_argument('input', metavar='PCAP_FILE', help='the input file')
parser.add_argument('output', metavar='OUTPUT_FOLDER', help='the target folder for extraction',
                    nargs='?', default='output')
parser.add_argument("-e", dest='entropy', help="use entropy based rawdata extraction", action="store_true", default=False)

print 'pcapfex - Packet Capture Forensic Evidence Extractor - version %s\n' % VERSION,

args = parser.parse_args()

if args.entropy:
    print 'Using entropy and statistical analysis for raw extraction and classification of unknown data.'

dispatcher = Dispatcher(args.input, args.output, args.entropy)
dispatcher.run()

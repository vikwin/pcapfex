# -*- coding: utf8 -*-
__author__ = 'Viktor Winkelmann'

import argparse
from core.Dispatcher import Dispatcher

VERSION = "0.1"

parser = argparse.ArgumentParser(description='Extract files from a pcap-file.')
parser.add_argument('input', metavar='PCAP_FILE', help="the input file")
parser.add_argument('output', metavar='OUTPUT_FOLDER', help="the target folder for extraction", default='output')

print "pcapfex - Packet Capture Forensic Evidence Extractor - version %s\n" % VERSION,

args = parser.parse_args()


dispatcher = Dispatcher(args.input, args.output)
dispatcher.run()

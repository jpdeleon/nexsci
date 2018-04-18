#!/usr/bin/env python

from nexsci import downloader as dl
#print(nexsci.__version__)
import argparse
parser = argparse.ArgumentParser(description="""
                query star and planet properties and show summary""",
                usage='use "%(prog)s --help" for more information',
                formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('hostname', help='hostname (e.g. WASP-33)', type=str)
parser.add_argument('-l', '--letter', help='planet letter (default=b)',
    type=str, default='b')
parser.add_argument('-v', '--verbose', help='verbose (default=False)', action='store_true', default=True)
parser.add_argument('-r', '--replace', help='re-download the data from database; (default=False: use previously downloaded file for faster query)',
    action='store_true', default=False)
parser.add_argument('-p', '--precision', help='number of decimal numbers (default=6)',
    type=int, default=6)

#parser.set_defaults(batch_download=False)

args = parser.parse_args()
hostname = args.hostname
letter   = args.letter
verbose  = args.verbose
replace  = args.replace
precision= args.precision

summary = dl.query_summary(hostname,letter=letter,precision=precision,replace=replace,verbose=verbose)
print(summary)
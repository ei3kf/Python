#!/usr/bin/python

"""
find_create_time.py
-------------------

"""

import os.path
import argparse
import time
import sys


def print_time(file):
    print "last modified: %s" % time.ctime(os.path.getmtime(file))
    print "created: %s" % time.ctime(os.path.getctime(file))
    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    parser.add_argument(
        "--file",
        help="name of file to check",
        type=str)

    args = parser.parse_args()

    if args.file:
        print_time(args.file)

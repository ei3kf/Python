#!/usr/bin/python

"""
whats_my_ip : returns your IP address 
"""

import urllib
import re
import sys


def my_ip():
    http_response = get_www()
    my_ip = get_ip(http_response)
    return my_ip


def get_www():
    url = "http://checkip.dyndns.org:8245/"
    try:
        http_response = urllib.urlopen(url).read()
        return http_response
    except Exception, e:
        print "Error: Can't reach", url
        sys.exit(1)


def get_ip(http_response):
    response_ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", http_response)
    my_ip = ''.join(response_ip)
    return my_ip


if __name__ == "__main__":

    print my_ip()

#!/usr/bin/env python

from __future__ import print_function

"""
 ssl_certifcate_check.py
 displays servername, current datetime, expire datetime of certificate,
 and the delta of the two dates.
"""

import socket
import ssl
import datetime
import argparse
import sys


def get_host_ssl_expiry_date(hostname, port):
    """
    Returns certificate expiry date.
    """
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET), server_hostname=hostname,)
    conn.settimeout(3.0)
    conn.connect((hostname, port))
    ssl_info = conn.getpeercert()
    cert_expiry_date = datetime.datetime.strptime(
        ssl_info['notAfter'], '%b %d %H:%M:%S %Y %Z')
    return cert_expiry_date


def date_delta_days(host_cert_notAfter, datetime_now):
    """
    Returns days delta of two dates.
    """
    delta = host_cert_notAfter - datetime_now
    return delta.days

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--hostname",
        help="Name of the host to query.",
        type=str)

    args = parser.parse_args()

    hostname = args.hostname
    port = 443

    try:
        cert_expiry_date = get_host_ssl_expiry_date(hostname, port)
        datetime_now = datetime.datetime.utcnow()
        delta_days = date_delta_days(cert_expiry_date, datetime_now)
        print("{} - {} - {} - {}".format(
            hostname, cert_expiry_date,
            unicode(datetime_now.replace(microsecond=0)),
            delta_days))
    except Exception, e:
        print("Error : {}".format(e))
        sys.exit()

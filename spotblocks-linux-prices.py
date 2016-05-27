#!/usr/bin/python

"""
spotblocks-linux-prices.py
-------------------

Display current AWS spot prices for
defined durations for Linux instances.
"""

import urllib2
import json


def get_spot_prices_data(url):
    """
    Retrieved response is in JSONP format,
    strip uncessary characters to return response
    in JSON format.
    """
    response = urllib2.urlopen(url).read()
    response = response[9:]
    response = response[:-2]
    return response


def fettle_spot_price(spotblock_price_data):
    """
    Do some fettling.
    """
    response_json = json.loads(spotblock_price_data)
    results = response_json['config']['regions']
    return results


def print_spotblock_prices(results):
    """
    Display by AWS region, instance type, current price and
    duration.
    """
    for result in results:
        print result['region']
        for r in result['instanceTypes']:
            for rr in r['sizes']:
                for rrr in rr['valueColumns']:
                    for usd, price in rrr['prices'].iteritems():
                        duration = rrr['name']
                        instance_type = rr['size']
                    print instance_type, price, duration
        print("\n")

if __name__ == "__main__":

    url = "https://spot-price.s3.amazonaws.com/spotblocks-generic.js"
    spotblock_price_data = get_spot_prices_data(url)
    results = fettle_spot_price(spotblock_price_data)
    print_spotblock_prices(results)

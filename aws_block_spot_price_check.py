#!/usr/bin/env python

"""
Return current block price for given Linux spot instance and duration.
"""

import urllib
import json
import re
import sys


class SpotPrice(object):
    def __init__(self):
        self.url = "https://spot-price.s3.amazonaws.com/spotblocks-generic.js"
        self.http_response = None
        self.aws_region = "us-east-1"
        self.response_ip = None
        self.aws_price = None

    def get_spot_data(self):
        """
        Returns Linux Spot Price Duration Data
        """
        self.http_response = urllib.urlopen(self.url).read()
        self.http_response_unpadded = self.http_response[self.http_response.index("(") + 1: self.http_response.rindex(")")]
        self.http_response_json = json.loads(self.http_response_unpadded)
        self.spot_results = self.http_response_json['config']['regions']

    def get_price(self, aws_instance_type, aws_duration):
        """
        Returns Price in USD for given instance and duration.
        """
        self.aws_instance_type = aws_instance_type
        self.aws_duration = aws_duration
        for self.result in self.spot_results:
            if self.result['region'] == self.aws_region:
                for self.r in self.result['instanceTypes']:
                    for self.rr in self.r['sizes']:
                        for self.rrr in self.rr['valueColumns']:
                            for self.usd, self.price in self.rrr['prices'].iteritems():
                                self.duration = int(self.rrr['name'][0])
                                self.instance_type = self.rr['size']
                                if (self.aws_instance_type == self.instance_type and
                                        self.aws_duration == self.duration):
                                        self.aws_price = self.price


def get_aws_price(aws_instance, aws_duration):
    """
    Return price in USD.
    """
    if (aws_duration == 1 or aws_duration == 6):
        my_spot_price = SpotPrice()
        my_spot_price.get_spot_data()
        my_spot_price.get_price(aws_instance, aws_duration)
        spot_price = my_spot_price.aws_price
        return spot_price
    else:
        print("Invalid Duration. Select 1 or 6.")
        sys.exit()


if __name__ == "__main__":

    aws_instance = "r3.large"
    aws_duration = 6
    print aws_instance, aws_duration, get_aws_price(aws_instance, aws_duration)

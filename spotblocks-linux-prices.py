#!/usr/bin/python

"""
Display current spot-price in USD for defined-hour EC2 Spot instances.
"""

import urllib2
import json
import argparse

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


def fettle_spotblock_price(spotblock_price_data):
    """
    Do some fettling.
    """
    response_json = json.loads(spotblock_price_data)
    results = response_json['config']['regions']
    return results


def display_spotblock_prices(results, aws_region):
    """
    Display 
    """
    for result in results:
        if result['region'] == aws_region:	
            print result['region']
            for r in  result['instanceTypes']:
                for rr in r['sizes']:
                    for rrr in rr['valueColumns']:
                        for usd, price in rrr['prices'].iteritems():
                            duration = rrr['name']
                            instance_type = rr['size']
                        print instance_type, price, duration


def get_aws_regions():
    """
    Change this to pull from AWS
    """
    aws_regions = ['eu-west-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'ap-northeast-2', 'ap-northeast-1', 'us-east-1', 'sa-east-1', 'us-west-1', 'us-west-2']
    return aws_regions

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--region",
        help="AWS Region",
	default="all",
        type=str)

    args = parser.parse_args()

    url = "https://spot-price.s3.amazonaws.com/spotblocks-generic.js"
    spotblock_price_data = get_spot_prices_data(url)
    results = fettle_spotblock_price(spotblock_price_data)

    aws_regions = []

    if args.region != "all":
       aws_regions = [ args.region ]
    else:
       aws_regions = get_aws_regions()
    
    for aws_region in aws_regions:
        display_spotblock_prices(results, aws_region)


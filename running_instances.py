#!/usr/bin/python

"""
    running_instances.py
    --------------------
     List running EC2 instances across all AWS regions.
     Specify region with --region <region_name>
"""

import boto3
import argparse

def get_aws_regions():
    """
    returns current AWS regions as a list. 
    """
    regions = []
    aws_regions = boto3.client('ec2').describe_regions()
    for aws_region in aws_regions['Regions']:
        regions.append(aws_region['RegionName'])
    return regions


def instances(aws_region):
    """
    Display running EC2 instances in given region.
    """
    ec2 = boto3.resource('ec2', aws_region)
    try:
        instances = ec2.instances.all()
        for instance in instances:
            if instance.state['Name'] == "running":
                print("{} : state {}").format(instance.id, instance.state['Name'])
    except Exception, e:
        print(e)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--region",
        help="AWS Region",
        type=str)

    args = parser.parse_args()

    if args.region:
        aws_regions = []
        aws_regions.append(args.region)
    else:
        aws_regions = get_aws_regions()

    for aws_region in aws_regions:
        print("Region : {}".format(aws_region))
        instances(aws_region)

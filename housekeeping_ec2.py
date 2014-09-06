#!/usr/bin/python

"""
   housekeeping_ec2.py
   -------------------

   lists running EC2 instances across all AWS regions by default, 
   unless region is passed with --region
   
"""

import sys
import boto.ec2
import argparse

def get_regions():
    regions = []
    aws_regions = boto.ec2.regions()
    for region in aws_regions:
        regions.append(region.name)
    return regions


def get_instances(region):
    ec2 = boto.ec2.connect_to_region(region)
    try:
        instances = ec2.get_all_instances()
        print_instances(instances)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception,e:
        return


def print_instances(instances):
    for instance in instances:
        for instance_data in instance.instances:
            if instance_data.state == "running":
                print("\t{} => {} ".format(instance_data.id,instance_data.state))
    return

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--region",
        help="AWS Region",
        type=str)

    args = parser.parse_args()

    if args.region:
        regions = []
        regions.append(args.region)
    else:
        regions = get_regions()
 
    for region in regions:
        print("Region : {}".format(region))
        get_instances(region)
        print("\n")
        


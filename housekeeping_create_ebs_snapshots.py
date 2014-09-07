#!/usr/bin/python

"""
housekeeping_create_ebs_snapshots.py
--------------------------------

Create EBS snapshots for all EBS volumes
across all AWS regions or specify a region.

"""

import boto.ec2
import argparse
import sys


def get_regions():
    regions = []
    aws_regions = boto.ec2.regions()
    for region in aws_regions:
        regions.append(region.name)
    return regions


def create_ebs_snapshot(ebs_volume):
    ec2_instance = str(ebs_volume.attach_data.instance_id)
    print "Snap-shotting ebs_volume : " + ebs_volume.id + " description : [ " + ec2_instance + " ] "
    ec2.create_snapshot(ebs_volume.id, ec2_instance)


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
        print region
        try:
            ec2 = boto.ec2.connect_to_region(region)
            ebs_volumes = ec2.get_all_volumes()
            if ebs_volumes == []:
                print "No EBS volumes found. Nothing to do."
            else:
                for ebs_volume in ebs_volumes:
                    create_ebs_snapshot(ebs_volume)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception, e:
            print e

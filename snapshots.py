#!/usr/bin/python

"""
    snapshots.py
    ------------
    list snapshots
    create snapshots

    to do:
        specify individual volumes to snapshot.
        add logging
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


def get_ebs_snapshots(ec2):
    """
    Return current EBS snapshots.
    """
    try:
        snapshots = ec2.describe_snapshots(OwnerIds=['self'])
    except Exception, e:
        print(e)
        raise e
    return snapshots


def get_ebs_volumes(ec2):
    """
    Return current EBS volumes.
    """
    try:
        ebs_volumes = ec2.describe_volumes()
    except Exception, e:
        print(e)
        raise e
    return ebs_volumes


def list_ebs_snapshots(ebs_snapshots):
    """
    List current EBS snapshots.
    """
    for ebs_snapshot in ebs_snapshots['Snapshots']:
        print("{} ==> {}").format(ebs_snapshot['SnapshotId'] , ebs_snapshot['VolumeId'])


def create_ebs_snapshot(ec2, ebs_volume):
    """
    Create an EBS snapshot from given EBS volume.
    """
    try:
        response = ec2.create_snapshot(VolumeId=ebs_volume)
        print response
    except Exception, e:
        print(e)
        raise e


def create_ebs_snapshots(ec2, ebs_volumes):
    """
    """
    for ebs_volume in ebs_volumes['Volumes']:
        print("Trying to create snapshot from EBS volume {}").format(ebs_volume['VolumeId'])
        create_ebs_snapshot(ec2, ebs_volume['VolumeId'])


def connect_ec2(aws_region):
    """
    Connect to EC2
    """
    ec2 = boto3.client('ec2', aws_region)
    return ec2

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--region",
        help="AWS Region",
        type=str)

    parser.add_argument(
        "--list",
        help="List EBS snapshots.",
        action='store_true',
        default=False)

    parser.add_argument(
        "--create",
        help="Create EBS snapshots.",
        action='store_true',
        default=False)

    args = parser.parse_args()

    if args.region:
        aws_regions = []
        aws_regions.append(args.region)
    else:
        aws_regions = get_aws_regions()

    if args.list:
        for aws_region in aws_regions:
            ec2 = connect_ec2(aws_region)
            ebs_snapshots = get_ebs_snapshots(ec2)
            print("=" * 30)
            print("Region : {}".format(aws_region))
            print("=" * 30)
            print("SnapshotID    ==> VolumeID")
            print("=" * 30)
            list_ebs_snapshots(ebs_snapshots)
    elif args.create:
        for aws_region in aws_regions:
            ec2 = connect_ec2(aws_region)
            ebs_volumes = get_ebs_volumes(ec2)
            print("=" * 30)
            print("Region : {}".format(aws_region))
            print("=" * 30)
            create_ebs_snapshots(ec2, ebs_volumes)




#!/usr/bin/python

"""
housekeeping_cleanup_ebs_snapshots.py
-------------------------------------
Delete any snapshots across all AWS regions or
specified region older than given age in days.
"""

import boto.ec2
import datetime
import argparse
import sys


def get_regions():
    regions = []
    aws_regions = boto.ec2.regions()
    for region in aws_regions:
        regions.append(region.name)
    return regions


def date_compare(date1, date2):
    y1, m1, d1 = date1.split('-')
    y2, m2, d2 = date2.split('-')
    new_date1 = datetime.date(int(y1), int(m1), int(d1))
    new_date2 = datetime.date(int(y2), int(m2), int(d2))
    date_delta = new_date2 - new_date1
    d = date_delta.total_seconds() / 86400
    return int(d)


def cleanup_ebs_snapshots(aws_region, days):
    try:
        print "Checking " + aws_region + " snapshots >= " + str(days) + " days"
        ec2 = boto.ec2.connect_to_region(aws_region)
        ebs_snapshots = ec2.get_all_snapshots(owner=['self'])
        for ebs_ss in ebs_snapshots:
            try:
                date_now = str(datetime.datetime.now().strftime('%Y-%m-%d'))
                snapshot_time = str(ebs_ss.start_time).split("T")
                date_delta = date_compare(snapshot_time[0], date_now)
                if date_delta >= days:
                    print "Deleting " ebs_ss.id
                    ec2.delete_snapshot(ebs_ss.id)
            except Exception, e:
                print e.response
        return
    except Exception, e:
        print e
        return

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--region",
        help="AWS Region",
        type=str)
    parser.add_argument(
        "--days",
        help="AWS Region",
        default=7,
        type=int)

    args = parser.parse_args()

    if args.region:
        aws_regions = []
        aws_regions.append(args.region)
    else:
        aws_regions = get_regions()

    for aws_region in aws_regions:
        cleanup_ebs_snapshots(aws_region, args.days)
        print "\n"

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


def cleanup_ebs_snapshots(region, days):
    date_now = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    try:
        ec2 = boto.ec2.connect_to_region(region)
        ebs_volumes = ec2.get_all_volumes()
        for ebs_volume in ebs_volumes:
            print ebs_volume
            for snapshot in ebs_volume.snapshots():
                ss_time = str(snapshot.start_time).split("T")
                date_delta = date_compare(ss_time[0], date_now)
                if date_delta > days:
                    print "Deleting " + snapshot.id
                    ec2.delete_snapshot(snapshot.id)
            print ""
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception, e:
        return
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
        regions = []
        regions.append(args.region)
    else:
        regions = get_regions()

    for region in regions:
        print("Region : {}".format(region))
        cleanup_ebs_snapshots(region, args.days)
        print("\n")

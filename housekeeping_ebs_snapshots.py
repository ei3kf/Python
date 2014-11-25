#!/usr/bin/python

"""
housekeeping_ebs_snapshots.py
-------------------------------------
default: List and delete EBS snapshots
in AWS account by age.

arguments: 
  --delete : deletes snapshot
  --region : run in specified AWS region
  --days   : snapshots => to delete
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


def snapshots(aws_region, days, ss_delete):
    try:
        ec2 = boto.ec2.connect_to_region(aws_region)
        ebs_snapshots = ec2.get_all_snapshots(owner=['self'])
        for ebs_ss in ebs_snapshots:
            try:
                date_now = str(datetime.datetime.now().strftime('%Y-%m-%d'))
                snapshot_time = str(ebs_ss.start_time).split("T")
                date_delta = date_compare(snapshot_time[0], date_now)
                if date_delta >= days:
                    print ebs_ss.id
                    if ss_delete:
       			try:
                            ec2.delete_snapshot(ebs_ss.id) 
			    print "deleting.\n"
            		except Exception, e:
                            print e.response
            except Exception, e:
                print e
    except KeyboardInterrupt:
        sys.exit(0)
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
        help="Number of days",
        default=7,
        type=int)
    parser.add_argument(
        "--delete",
        action='store_true',
	help='delete valid snapshots'
	)

    args = parser.parse_args()

    if args.region:
        aws_regions = []
        aws_regions.append(args.region)
    else:
        aws_regions = get_regions()

    for aws_region in aws_regions:
        print "AWS Region: ", aws_region
        snapshots(aws_region, args.days, args.delete)
        print ""


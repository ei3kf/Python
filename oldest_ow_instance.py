#!/usr/bin/python
"""
 - Return the oldest OW instance in given stack.
"""

import os
import sys
import boto3
import datetime


def ow_connect():
    """
    Connect to OpsWorks ( OpsWorks only in us-east-1 )
    """
    ow = boto3.client('opsworks', region_name='us-east-1')
    return ow


def ow_instances(ow, ow_stack):
    """
    Return sorted dictionary of OpsWork Instance IDs by CreatedAt epochtime.
    """
    try:
        instances = ow.describe_instances(StackId=ow_stack)
    except Exception, e:
        print(e)
        sys.exit()
    ow_launch_data = {}
    for instance in instances['Instances']:
        created_at = datetime.datetime.strptime(
            instance['CreatedAt'], '%Y-%m-%dT%H:%M:%S+00:00').strftime('%s')
        ow_launch_data[instance['InstanceId']] = created_at
    return ow_launch_data

if __name__ == '__main__':

    ow_stack = "00000000-0000-0000-0000-000000000000"

    ow = ow_connect()
    ow_launch_data = ow_instances(ow, ow_stack)

    for key, value in sorted(ow_launch_data.iteritems(),
                             key=lambda (k, v): (v, k)):
        print "%s: %s" % (key, value)
    print("")
    sorted_ow_launch_data = sorted(ow_launch_data.items())
    print("Oldest OW instance ==> {}".format(sorted_ow_launch_data[0]))

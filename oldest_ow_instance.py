#!/usr/bin/python
"""
 - Return the oldest OW instance in given stack.
 - Stop oldest OW instance 
 - Delete oldest OW instance
"""

import os
import sys
import boto3
import datetime
import time
import json
import logging
import argparse


def ow_connect():
    """
    Connect to OpsWorks ( OpsWorks only in us-east-1 )
    """
    ow = boto3.client('opsworks', region_name='us-east-1')
    return ow


def ow_logging(logfile):
    """
    Logging function
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        filename=logfile,
        filemode='a')
    log = logging.getLogger(__name__)
    return log


def ow_instances(ow, ow_stack):
    """
    Return sorted dictionary of OpsWork Instance IDs by CreatedAt epochtime.
    """
    log.info("ow_instances( %s )", ow_stack)
    try:
        instances = ow.describe_instances(StackId=ow_stack)
    except Exception, e:
        print(e)
        log.info(e)
        sys.exit()
    ow_launch_data = {}
    for instance in instances['Instances']:
        created_at = datetime.datetime.strptime(
            instance['CreatedAt'], '%Y-%m-%dT%H:%M:%S+00:00').strftime('%s')
        ow_launch_data[instance['InstanceId']] = created_at
        log.info("instance %s, created %s", instance, created_at)
    return ow_launch_data


def oldest_ow_instance(ow_launch_data):
    """
    Return oldest OpsWorks Instance ID
    """
    log.info("oldest_ow_instance( %s )", ow_launch_data)
    sorted_ow_launch_data = sorted(ow_launch_data.items(), key=lambda x: x[1])
    log.info("sorted_ow_launch_data = %s", sorted_ow_launch_data)
    oldest_ow_instance = sorted_ow_launch_data[0]
    ow_instance_id, launch_time = oldest_ow_instance
    log.info("ow_instance_id = %s, ow_launch_data = %s",
             ow_instance_id, ow_launch_data)
    print("Oldest OW instance ==> {}".format(ow_instance_id))
    log.info("Oldest OW instance ==> %s", ow_instance_id)
    return ow_instance_id


def terminate_ow_instance(ow, ow_instance_id):
    """
    Terminate OpsWorks Instance ( stop & delete )
    """
    log.info("terminate_ow_instance( %s )", ow_instance_id)
    try:
        ow.stop_instance(InstanceId=ow_instance_id)
    except Exception, e:
        print(e)
        log.info(e)
        sys.exit()
    while True:
        data = ow.describe_instances(InstanceIds=[ow_instance_id])['Instances']
        raw = json.dumps(data)
        ow_instance_json = json.loads(raw)
        print(ow_instance_json[0]['InstanceId'], ow_instance_json[0]['Status'])
        log.info("%s %s", ow_instance_json[0]['InstanceId'],
                 ow_instance_json[0]['Status'])
        if ow_instance_json[0]['Status'] == "stopped":
            print(ow_instance_json[0]['InstanceId'],
                  ow_instance_json[0]['Status'])
            log.info("%s %s", ow_instance_json[0]['InstanceId'],
                     ow_instance_json[0]['Status'])
            response = ow.delete_instance(InstanceId=ow_instance_id)
            print(response)
            log.info("Delete instance = %s", response)
            break
        else:
            time.sleep(60)
            continue

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stackid",
        help="OpsWorks StackID",
        type=str,
        default="00000000-0000-0000-0000-000000000000"
    )
    parser.add_argument(
        "--logfile",
        help="Log file",
        type=str,
        default="oldest_opsworks_instance.log"
    )

    args = parser.parse_args()
    log = ow_logging(args.logfile)
    ow_stack = args.stackid
    ow = ow_connect()
    ow_launch_data = ow_instances(ow, ow_stack)
    ow_instance_id = oldest_ow_instance(ow_launch_data)
    terminate_ow_instance(ow, ow_instance_id)

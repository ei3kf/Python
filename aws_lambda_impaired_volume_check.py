from __future__ import print_function

"""
Run as lambda function, triggered by CW scheduled
event every X minutes.
"""

import boto3
import argparse
import json
import urllib2
from time import sleep

def get_volumes_status(client):
    """
    Return status of all volumes.
    """
    response = client.describe_volume_status()
    return response


def get_volumes_state(client):
    """
    Return all volumes.
    """
    response = client.describe_volumes()
    return response


def check_states(volumes_status, volumes_state, environment, aws_region):
    """
    Check for volumes in error, if found post to slack channel.
    - if volume to be ignored - add to ignore_volumes list.
    """
    ignore_volumes = ['vol-xxxxxxxx']
    for volume_status in volumes_status['VolumeStatuses']:
        volume_id = volume_status['VolumeId']
        if volume_id not in ignore_volumes:
            volume_status_check = volume_status['VolumeStatus']['Status']
            volume_status_check_details = volume_status['VolumeStatus']['Details']
            for volume_state in volumes_state['Volumes']:
                volume_state_id = volume_state['VolumeId']
                if volume_state_id == volume_id:
                    volume_state_check = volume_state['State']
                if (volume_status_check) != 'ok' or (volume_state_check) == 'error':
                    msg = (environment.upper() +
                           ":" +
                           aws_region +
                           ":IMPAIRED VOLUME:" +
                           volume_id +
                           " - Status:" +
                           volume_status_check +
                           " - State:" +
                           volume_state_check +
                           " = Please investigate."
                           )
                    post_to_slack(msg)


def post_to_slack(msg):
    """
    Post to slack
    """
    SLACK_ENDPOINT = ""
    SLACK_CHANNEL = ""
    SLACK_USERNAME = ""
    SLACK_TEXT = (str(msg))
    SLACK_JSON = {
        'channel': SLACK_CHANNEL,
        'username': SLACK_USERNAME,
        'text': SLACK_TEXT,
        }
    request = urllib2.Request(SLACK_ENDPOINT)
    request.add_header('Content-Type', 'application/json')
    urllib2.urlopen(request, json.dumps(SLACK_JSON))


def lambda_handler(event, context):
    global client
    client = boto3.client('ec2')
    environment = ''
    aws_region = 'us-east-1'
    volumes_status = get_volumes_status(client)
    volumes_state = get_volumes_state(client)
    check_states(volumes_status, volumes_state, environment, aws_region)

#!/usr/bin/env python

import boto3
import time

client = boto3.client('ec2', region_name='eu-west-1')

i = 'put instance ID here'
modifiedInstanceTypeValue = 't2.small'

try:
    instanceType = client.describe_instance_attribute(InstanceId=i,Attribute='instanceType')['InstanceType']
    currentInstanceTypeValue = instanceType.get('Value')
    while (currentInstanceTypeValue != modifiedInstanceTypeValue):
        instanceType = client.describe_instance_attribute(InstanceId=i,Attribute='instanceType')['InstanceType']
        currentInstanceTypeValue = instanceType.get('Value')
        print(currentInstanceTypeValue)
        print(modifiedInstanceTypeValue)
        time.sleep(5)
except Exception as e:
    msg = "describe_instance_attribute() has encountered an exception %s , error --> %s ' % (i, str(e))
    print(msg)
        

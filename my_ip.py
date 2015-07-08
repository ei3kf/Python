#!/usr/bin/python

"""
my_ip.py
 - check if my IP address is in my AWS Security Group.
 - add my IP address to my AWS Security Group.
 - delete my IP address from my AWS Security Group.
 - display current IPs in my AWS Security Group.
"""

import urllib
import re
import sys
import boto.ec2
import argparse


def my_ip():
    http_response = get_www()
    my_ip = get_ip(http_response)
    return my_ip


def get_www():
    url = "http://checkip.dyndns.org:8245/"
    try:
        http_response = urllib.urlopen(url).read()
        return http_response
    except Exception, e:
        print "Error: Can't reach", url
        sys.exit(1)


def check_my_ip(my_region, my_ip_address, my_security_group):
    ec2 = boto.ec2.connect_to_region(my_region)
    security_group = ec2.get_all_security_groups(group_ids=my_security_group)
    for sg in security_group:
        for rule in sg.rules:
            for ip in rule.grants:
	        if str(ip) == my_ip_address:
		    print my_ip_address + " found in " + my_security_group
		    return
    print my_ip_address + " NOT found in " + my_security_group
    return


def display_my_security_group(my_region,my_security_group):
    ec2 = boto.ec2.connect_to_region(my_region)
    security_group = ec2.get_all_security_groups(group_ids=my_security_group)
    for sg in security_group:
        for rule in sg.rules:
            for ip in rule.grants:
	        print ip
    return


def add_my_ip(my_region, my_ip_address, my_security_group):
    ec2 = boto.ec2.connect_to_region(my_region)
    rule = ec2.authorize_security_group(
	group_id=my_security_group,
	ip_protocol="-1", 
	from_port=-1,
	to_port=-1,
	cidr_ip=my_ip_address) 
    return
  

def delete_my_ip(my_region, my_ip_address, my_security_group):
    ec2 = boto.ec2.connect_to_region(my_region)
    rule = ec2.revoke_security_group(
	group_id=my_security_group,
	ip_protocol="-1",
	from_port=-1,
	to_port=-1,
	cidr_ip=my_ip_address) 
    return


def get_ip(http_response):
    response_ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", http_response)
    my_ip = ''.join(response_ip) + "/32"
    return my_ip


if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--region",
        help="AWS Region",
	default="eu-west-1",
        type=str)

    parser.add_argument(
        "--check",
        help="Is my IP address already in my Security Group?",
        action='store_true',
        default=False)

    parser.add_argument(
        "--show",
        help="Show IPs in my Security Group",
        action='store_true',
        default=False)

    parser.add_argument(
        "--sg",
        help="My Security Group",
        action='store_true',
        default="sg-284ea747")

    parser.add_argument(
       "--ip",
        help="Display my IP Address.",
        action='store_true',
        default=False)

    parser.add_argument(
       "--add",
        help="Add my IP address to my Security Group.",
        action='store_true',
        default=False)

    parser.add_argument(
       "--delete",
        help="Delete my IP address from my Security Group.",
        action='store_true',
        default=False)

    args = parser.parse_args()

    my_ip_address = my_ip()
    my_security_group = args.sg
    my_region = args.region
   
    try:
        if args.check:
            print "Checking for " + my_ip_address + " in " + my_security_group
            check_my_ip(my_region, my_ip_address, my_security_group)
	elif args.show:
	    print "Displaying IPs in " + my_security_group
	    display_my_security_group(my_region,my_security_group)
        elif args.ip:
            print "Your IP address is " + my_ip_address
        elif args.add:
	    print "Adding " + my_ip_address + " to " + my_security_group
            add_my_ip(my_region, my_ip_address, my_security_group)
        elif args.delete:
	    print "Deleting " + my_ip_address + " from " + my_security_group
            delete_my_ip(my_region, my_ip_address, my_security_group)
        else:
            print "Niks te doen."
    except KeyboardInterrupt:
	sys.exit(0)
    except Exception, e:
        print "Computer says " + e

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
    """
    Returns the IP address of the client where the script is run.
    """
    http_response = get_www(url)
    my_ip = get_ip(http_response)
    return my_ip


def get_www(url):
    """
    Connect to a URL, and return the response.
    """
    try:
        http_response = urllib.urlopen(url).read()
        return http_response
    except Exception, e:
        print("Error: Can't reach {}").format(url)
        sys.exit(1)


def check_my_ip(my_region, my_ip_address, my_security_group):
    """
    Checks to see if the given IP exists in the given AWS security group.
    """
    ec2 = boto.ec2.connect_to_region(my_region)
    security_group = ec2.get_all_security_groups(group_ids=my_security_group)
    for sg in security_group:
        for rule in sg.rules:
            for ip in rule.grants:
                if str(ip) == my_ip_address:
		    print("My IP {} found in Security Group {}").format(my_ip_address,my_security_group)
                    return True
    print("My IP {} NOT found in Security Group {}").format(my_ip_address,my_security_group)
    return False


def display_my_security_group(my_region,my_security_group):
    """
    List all the IP addresses in the given AWS security group.
    """
    ec2 = boto.ec2.connect_to_region(my_region)
    security_group = ec2.get_all_security_groups(group_ids=my_security_group)
    for sg in security_group:
        for rule in sg.rules:
            for ip in rule.grants:
                print ip
    return


def add_my_ip(my_region, my_ip_address, my_security_group):
    """
    Add the given IP to the given AWS security group, allowing all protocols and all network ports.
    """
    ec2 = boto.ec2.connect_to_region(my_region)
    rule = ec2.authorize_security_group(
        group_id=my_security_group,
        ip_protocol="-1", 
        from_port=-1,
        to_port=-1,
        cidr_ip=my_ip_address) 
    return
  

def delete_my_ip(my_region, my_ip_address, my_security_group):
    """
    Delete the given IP from the given AWS security group.
    """
    ec2 = boto.ec2.connect_to_region(my_region)
    rule = ec2.revoke_security_group(
        group_id=my_security_group,
        ip_protocol="-1",
        from_port=-1,
        to_port=-1,
        cidr_ip=my_ip_address) 
    return


def get_ip(http_response):
    """
    Find the IP address in the url response.
    Return that IP   
    """
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
        "--url",
        help="URL to retrieve current IP address",
        default="http://checkip.dyndns.org:8245/",
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

    add_delete = parser.add_mutually_exclusive_group()

    add_delete.add_argument(
       "--add",
        help="Add my IP address to my Security Group.",
        action='store_true',
        default=False)

    add_delete.add_argument(
       "--delete",
        help="Delete my IP address from my Security Group.",
        action='store_true',
        default=False)

    args = parser.parse_args()

    url = args.url

    my_ip_address = my_ip()
    my_security_group = args.sg
    my_region = args.region
   
    try:
        if args.check:
            print("Checking for {} in {}").format(my_ip_address, my_security_group)
            check_my_ip(my_region, my_ip_address, my_security_group)
        elif args.show:
            print("Displaying IPs in {}").format(my_security_group)
            display_my_security_group(my_region,my_security_group)
        elif args.ip:
            print("Your IP address is {}").format(my_ip_address)
        elif args.add:
	    checked_my_ip = check_my_ip(my_region, my_ip_address, my_security_group)
	    if checked_my_ip:
                print("{} already exists in {}, nothing further to do.").format(my_ip_address, my_security_group)
	    else:
                print("Adding {} to {}").format(my_ip_address, my_security_group)
                add_my_ip(my_region, my_ip_address, my_security_group)
        elif args.delete:
	    checked_my_ip = check_my_ip(my_region, my_ip_address, my_security_group)
	    if checked_my_ip:
                print("Deleting {} from {}").format(my_ip_address, my_security_group)
                delete_my_ip(my_region, my_ip_address, my_security_group)
	    else:
                print("{} NOT found in {}, nothing further to do.").format(my_ip_address, my_security_group)

        else:
            print "Niks te doen."
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception, e:
        print "Computer says " + e


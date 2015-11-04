#!/usr/bin/python

"""
    mijn_ip.py
    - display my current IP address
    - show the current IP addresses in the given AWS Security Group
    - check to see if my current IP is in the given AWS Security Group
    - Add my current IP to the given AWS Security Group
    - Delete my current IP from the given AWS Security Group
"""

import urllib
import re
import sys
import boto.ec2
import argparse


class MijnIp(object):
    """
     MijnIp - class to find and return an IP address
    """
    def __init__(self, url):
        self.url = url
        self.http_response = None
        self.response_ip = None

    def read_url(self):
        """
          read_url() - this function will access a URL and return the response.
        """
        self.http_response = urllib.urlopen(self.url).read()

    def return_ip(self):
        """
          return_ip() - assign the IP address found to an variable.
        """
        self.response_ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", self.http_response)[0]


class SecurityGroups(object):
    """
    Class to query security group.
    """
    def __init__(self, region, security_group):
        self.region = region
        self.security_group = security_group
        self.ec2 = boto.ec2.connect_to_region(self.region)
        self.ec2_security_group = self.ec2.get_all_security_groups(group_ids=self.security_group)
        self.ip_list = []

    def security_group_rules(self):
        """
        creates a list of IPs in given security group.
        """
        for self.sg in self.ec2_security_group:
            for self.rule in self.sg.rules:
                for self.ip in self.rule.grants:
                    self.ip_list.append(self.ip)

    def security_group_add_rule(self, my_ip):
        """
        Add a rule to the given security group, allowing all traffic from given IP.
        """
        self.my_ip = my_ip
        self.add_rule = self.ec2.authorize_security_group(
            group_id=self.security_group,
            ip_protocol="-1",
            from_port=-1,
            to_port=-1,
            cidr_ip=self.my_ip)

    def security_group_delete_rule(self, my_ip):
        """
        Delete the rule that contains the given IP.
        """
        self.my_ip = my_ip
        self.delete_rule = self.ec2.revoke_security_group(
            group_id=self.security_group,
            ip_protocol="-1",
            from_port=-1,
            to_port=-1,
            cidr_ip=self.my_ip)


def get_my_ip():
    """
    Get my current IP.
    """
    my_ip_query = MijnIp(args.url)
    my_ip_query.read_url()
    my_ip_query.return_ip()
    ip = my_ip_query.response_ip + "/32"
    return ip


def list_my_sg():
    """
    Returns the list of IPs in a security group.
    """
    my_security_group = SecurityGroups(args.region, args.sg)
    my_security_group.security_group_rules()
    ip_list = my_security_group.ip_list
    return ip_list


def check_my_sg():
    """
    Does the IP exist in the IP list from the security group.
    """
    ip = get_my_ip()
    for ips in list_my_sg():
        if str(ips) == ip:
            return True


def add_my_ip(my_ip):
    """
    add the IP
    """
    my_security_group = SecurityGroups(args.region, args.sg)
    my_security_group.security_group_add_rule(my_ip)


def delete_my_ip():
    """
    delete the IP
    """
    my_security_group = SecurityGroups(args.region, args.sg)
    my_security_group.security_group_delete_rule(my_ip)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--region",
        help="AWS Region",
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
        type=str)

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

    try:
        if args.check:
            if not args.region:
                print("AWS Region needs to be specified.")
		sys.exit(1)
            elif not args.sg:
                print("AWS security group needs to be specified.")
		sys.exit(1)
            my_ip = get_my_ip()
            print("Checking for IP address {} in security group {}").format(my_ip, args.sg)
            if check_my_sg():
                print("IP {} found.").format(my_ip)
            else:
                print("IP {} NOT found.").format(my_ip)
        elif args.show:
            if not args.region:
                print("AWS Region needs to be specified.")
            elif not args.sg:
                print("AWS security group needs to be specified.")
            else:
                print("Listing IP addresses in security group {}").format(args.sg)
                for ip in list_my_sg():
                    print ip
        elif args.ip:
            my_ip = get_my_ip()
            print("Your IP address is {}").format(my_ip)
        elif args.add:
            if not args.region:
                print("AWS Region needs to be specified.")
		sys.exit(1)
            elif not args.sg:
                print("AWS security group needs to be specified.")
		sys.exit(1)
            else:
                my_ip = get_my_ip()
                if check_my_sg():
                    print("IP {} already in security group {}").format(my_ip, args.sg)
                else:
                    print("IP {} adding to security group {}").format(my_ip, args.sg)
                    add_my_ip(my_ip)
        elif args.delete:
            if not args.region:
                print("AWS Region needs to be specified.")
            elif not args.sg:
                print("AWS security group needs to be specified.")
            else:
               my_ip = get_my_ip()
               if check_my_sg():
                    print("IP {} deleting from security group {}").format(my_ip, args.sg)
                    delete_my_ip()
               else:
                    print("IP {} not found in security group {}").format(my_ip, args.sg)
        else:
            my_ip = get_my_ip()
            print("Your IP address is {}").format(my_ip)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception, e:
        str(e)
        print("Computer says: {}").format(e)

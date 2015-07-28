#!/usr/bin/python

"""

Find and return your IP address.
- refactored to use a class object for mentorship.

"""

import urllib
import re
import sys

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
        self.response_ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", self.http_response)




url = "http://checkip.dyndns.org:8245/"

my_ip_query = MijnIp(url)
my_ip_query.read_url()
my_ip_query.return_ip()

print my_ip_query.response_ip

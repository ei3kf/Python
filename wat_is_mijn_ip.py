#!/usr/bin/python

"""
Find and return your IP address.
- refactored to use a class object. 
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
	self.response = ""

    def read_url(self):
	"""	
	  read_url() - this function will access a URL and return the response.
	"""	
        http_response = urllib.urlopen(self.url).read()
	return http_response

    def return_ip(self, http_response):
	"""
	  return_ip() - this function will return the IP address found in the read_url() returned response.
	"""
        response_ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", http_response) 
	return response_ip

url = "http://checkip.dyndns.org:8245/"

my_ip_query = MijnIp(url)
my_ip = my_ip_query.return_ip(my_ip_query.read_url())
print my_ip



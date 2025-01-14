#!/usr/bin/env python3

# Fair easier way of finding my internet facing IP address....

import requests
print(requests.get('https://checkip.amazonaws.com').text.strip())

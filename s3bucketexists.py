#!/usr/bin/env python3

'''

Returns TRUE if bucket exists, otherwise returns FALSE.

Usage: 
$ BUCKET="my-lovely-bucket" python3 ./s3bucketexists.py

'''

import boto3
import os

class S3BucketExists():
    def __init__(self):                                 
        self.session = boto3.Session(profile_name="REPLACE_WITH_YOUR_PROFILE")
        self.s3_client = self.session.client('s3')
        self.bucket_name_exists = os.environ['BUCKET']

    def bucket_exists(self):
        response = self.s3_client.list_buckets()
        for bucket in response['Buckets']:
            if self.bucket_name_exists == bucket['Name']:
                return True
        return False


if __name__ == '__main__':
    buckets = S3BucketExists()
    bucket_exists = buckets.bucket_exists()
    print(f"{bucket_exists}")

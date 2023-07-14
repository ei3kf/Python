#!/usr/bin/env python3

'''
Usage: 
$ BUCKET="my-lovely-bucket" python3 ./unittest_s3_bucket_exists.py
'''

import boto3
import os
import unittest
 
class S3BucketExistsTest(unittest.TestCase):
    def setUp(self):                                
        self.session = boto3.Session(profile_name="REPLACE_WITH_YOUR_PROFILE")
        self.s3_client = self.session.client('s3')
        self.bucket_name = os.environ['bucket_name']

    def test_bucket_exists_assert_true(self):
        response = self.s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        self.assertTrue(self.bucket_name in buckets, f"Bucket '{self.bucket_name} does not exist.")


if __name__ == '__main__':
    unittest.main()

import boto3
import random 
import string
import json

import boto3
s3 = boto3.resource("s3")
s3client = boto3.client("s3")
bucket_name=(f"{''.join(random.choices(string.ascii_lowercase+string.digits, k=6))}-akutasevych")
try:
    s3.create_bucket(Bucket=bucket_name)
    print (f"Created a bucket with a name {bucket_name}")
except Exception as error:
    print (f"Failed to create a bucket: {error}")

try:
    s3client.delete_public_access_block(Bucket=bucket_name)
    bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
    {
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": ["s3:GetObject"],
        "Resource": f"arn:aws:s3:::{bucket_name}/*"
    }
    ]
    }
    s3.Bucket(bucket_name).Policy().put(Policy=json.dumps(bucket_policy))
    print("Bucket policy successfully updated")
except Exception as error:
    print(f"Error updating bucket policy: {error}")

try:
    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
    }
    bucket_website = s3.BucketWebsite(bucket_name)
    bucket_website.put(WebsiteConfiguration=website_configuration)
    print("Website configuration added successfully")
except Exception as error:
    print(f"Error configuring website configuration: {error}")
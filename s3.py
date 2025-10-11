import boto3
import random 
import string
import json
import subprocess

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

url = "http://devops.setudemo.net/logo.jpg" #URL for the file

subprocess.run(["curl", "-L", "-o", "logo.jpg", url], check=True)
object_name = "logo.jpg"
index_name = "index.html"

try:
    s3.Object(bucket_name,object_name).put(Body=open(object_name, 'rb'),ContentType='image/jpg')
    print (f"Logo.jpg has been successfully added to bucket {bucket_name}")
    #index.html
    html_content = f"""
            <html><body>
            <img src="logo.jpg" alt="Sorry logo url has changed, come back later"> 
            </body></html>
        """
    s3.Object(bucket_name, "index.html").put(Body=html_content,ContentType="text/html")
    print (f"index.html has been successfully added to bucket {bucket_name}")
    #error.html
    html_content = f"""
            <html><body>
            <h2>Sorry an error has occured</h2>
            </body></html>
        """
    s3.Object(bucket_name, "error.html").put(Body=html_content,ContentType="text/html")
    print (f"error.html has been successfully added to bucket {bucket_name}")
except Exception as error:
    print (f"Failed to add item in a bucket: {error}")


website_url = f"http://{bucket_name}.s3-website-us-east-1.amazonaws.com"
print(f"Website available at: {website_url}")

#writing s3 url into file
try:
    print("trying to write s3 url into a file...")
    with open("akutasevych-websites.txt", "a", encoding="utf-8") as f:
        f.write(f"{website_url}\n")

    print("reading the file contents")

    with open("akutasevych-websites.txt", "r", encoding="utf-8") as f:
        print(f.read())
except Exception as error:
    print(f"Error writing IP into a file: {error}")
f.close()
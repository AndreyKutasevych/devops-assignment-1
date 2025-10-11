import boto3
import os
import time
ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')

#terminating instances
print("Terminating instances...")
for instance in ec2.instances.all():
    try:
        print (f"Terminating instance {instance.id}")
        instance.terminate()
        print("Terminated")
    except Exception as error:
        print(f"Error deleting an instance: {error}")
print("........")

#terminating s3 buckets
print("Terminating buckets...")
for bucket in s3.buckets.all():
    for key in bucket.objects.all():
        try:
            key.delete()
            print (f"Contents of bucket {bucket.name} deleted successfully")
        except Exception as error:
            print (f"Error emptying bucket {bucket.name}: {error}")
    try:
        bucket.delete()
        print (f"Bucket {bucket.name} removed successfully")
    except Exception as error:
        print (f"Error deleting a bucket: {error}")
print(".........")

#removing url text file
print("Removing the URL text file...")
try:
    if os.path.exists("akutasevych-websites.txt"):
        os.remove("akutasevych-websites.txt")
        print("URL file removed successfully")
    else:
        print("The file does not exist")
except Exception as error:
    print(f"Error removing the file: {error}")

#removing image file
print("Removing the default jpg file...")
try:
    if os.path.exists("logo.jpg"):
        os.remove("logo.jpg")
        print("Jpg file removed successfully")
    else:
        print("The file does not exist")
except Exception as error:
    print(f"Error removing the file: {error}")

#removing personal AMIs
    print("Removing personal AMIs")

for image in ec2.images.filter(Owners=['self']):
    try:
        print(f"Deleting {image.id}: {image.name}")
        image.deregister()
        time.sleep(10)
        for bdm in image.block_device_mappings:
            if 'Ebs' in bdm:
                ec2.Snapshot(bdm['Ebs']['SnapshotId']).delete()
        print("personal AMI removed")
    except Exception as error:
        print(f"Failed to remove personal AMIs: {error}")
        continue 
    print("All AMIs removed")
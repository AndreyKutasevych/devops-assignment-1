import boto3
ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')

#listing ec2 instances
print("EC2 instances:")
try:
    for instance in ec2.instances.all():
        print (instance.id, instance.state, instance.public_ip_address if instance.public_ip_address else "No public ip address asigned")
except Exception as error:
    print(f"Error listing instances: {error}")

#listing s3 buckets
print("Buckets and their contents:")
try:
    for bucket in s3.buckets.all():
        print (bucket.name)
        print ("---")
        try:
            for item in bucket.objects.all():
                print ("\t%s" % item.key)
        except Exception as error:
            print(f"Error listing content of bucket {bucket.name}: {error}")
except Exception as error:
    print(f"Error listing buckts: {error}")

    #listing AMIs
try:
    print("Personal AMIs:")
    for image in ec2.images.filter(Owners=['self']):
        print(f"{image.id}: {image.name}")
except Exception as error:
    print(f"Error printing personal AMIs: {error}")
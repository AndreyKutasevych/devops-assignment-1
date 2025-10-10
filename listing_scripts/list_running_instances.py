import boto3
ec2 = boto3.resource('ec2')
print("EC2 instances:")
try:
    for instance in ec2.instances.all():
        if(instance.state['Name']=="running"):
            print (instance.id, instance.public_ip_address)
except:
    print("Error listing instances")
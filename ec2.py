import boto3
import subprocess
import time
from datetime import datetime
ec2 = boto3.resource("ec2")

# ec2 instance
try:
    print("Creating an instance....")
    new_instances = ec2.create_instances(
        ImageId='ami-052064a798f08f0d3',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.nano',
        SecurityGroupIds=['sg-0ef9666e04df0d6d5'],
        Placement={
            'AvailabilityZone':'us-east-1a'
        },#getting instance metadata
        KeyName='my-key',
        UserData="""#!/bin/bash
            yum install httpd -y
            systemctl enable httpd
            systemctl start httpd
            echo '<html>' > index.html
            echo 'Private IP address: ' >> index.html
            TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
            curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html

            echo '<br> Instance id: ' >> index.html
            TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
            curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id >> index.html

            echo '<br> Availability Zone: ' >> index.html
            TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
            curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/availability-zone >> index.html

            echo '<br> Instance type: ' >> index.html
            TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
            curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type >> index.html
            cp index.html /var/www/html/index.html""")
    print("Done!")
    print(f"Instance {new_instances[0].id} is created")
except Exception as error:
    print(f"Failed to create an instance: {error}")
#launching the instance
try:
    print("Launching the instance...")
    name_tag = {'Key': 'Name', 'Value': 'Demo instance'}
    new_instances[0].create_tags(Tags=[name_tag])
    new_instances[0].wait_until_running()
    new_instances[0].reload()
    print("Done!")
    print(f"Successfully ran an instance with an id of {new_instances[0].id} and a public ip of {new_instances[0].public_ip_address}")
    print("Waiting for SSH to become available...")
    time.sleep(45)
    print("Done!")
    try:
        print("trying to write IP into a file...")
        with open("akutasevych-websites.txt", "w", encoding="utf-8") as f:
            f.write(f"{new_instances[0].public_ip_address}\n")

        print("reading the file contents")

        with open("akutasevych-websites.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as error:
        print(f"Error writing IP into a file: {error}")
    f.close()
except Exception as error:
    print(f"Failed to retrive a page metadata: {error}")

try:
    print("trying to upload a monitor script file...")
    cmd = 'scp -o StrictHostKeyChecking=no -i my-key.pem monitoring.sh ec2-user@$(head -n 1 akutasevych-websites.txt):.'
    subprocess.run(cmd, shell=True)
    print("monitoring script file uploaded successfully")

    try:
        print("Making script executable...")
        cmd = "ssh -o StrictHostKeyChecking=no -i my-key.pem ec2-user@$(head -n 1 akutasevych-websites.txt) 'chmod 700 monitoring.sh'"
        subprocess.run(cmd, shell=True)
        print("file has been made executable")
    except Exception as error:
        print(f"failed to make the script file executable: {error}")
    try:
        print("running checks...")
        cmd = "ssh -o StrictHostKeyChecking=no -i my-key.pem ec2-user@$(head -n 1 akutasevych-websites.txt) './monitoring.sh'"
        subprocess.run(cmd, shell=True)
    except Exception as error:
        print(f"Failed executing monitor script commands: {error}")

except Exception as error:
    print(f"Error uploading script file: {error}")

#AMI creation
try:
    print("Creating AMI...")
    image=new_instances[0].create_image(Name=f'AK-{datetime.now().strftime("%Y-%m-%d")}-{int(time.time()) % 1000000}')
    print(f"AMI created: {image.name}")
except Exception as error:
    print(f"Failed to create AMI: {error}")
#!/usr/bin/python3

import boto3
from datetime import datetime, timezone, timedelta
import time
import sys

cloudwatch = boto3.resource('cloudwatch')
ec2 = boto3.resource('ec2')

def get_running_instance():
    for instance in ec2.instances.all():
        if instance.state['Name'] == "running":
            return instance.id

try:
    instid = sys.argv[1] if len(sys.argv) > 1 else get_running_instance()
    instance = ec2.Instance(instid)
    instance.monitor() 
    print("Getting instance metrics from cloudwatch...")
    while True:
        try:
            metric_iterator = cloudwatch.metrics.filter(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instid}]
            )

            metric = list(metric_iterator)[0]  # may raise IndexError

            response = metric.get_statistics(
                StartTime=datetime.now(timezone.utc) - timedelta(minutes=10),
                EndTime=datetime.now(timezone.utc),
                Period=300,
                Statistics=['Average']
            )

            if not response['Datapoints']:
                raise Exception("No datapoints yet")

            print("Average CPU utilisation:",
                  response['Datapoints'][0]['Average'],
                  response['Datapoints'][0]['Unit'])
            break

        except Exception:
            time.sleep(5)

except Exception:
    print("No running instances found")

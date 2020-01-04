#!/usr/bin/python

import boto3
from botocore.exceptions import ClientError
import sys
import csv
import re

### User defined vars
region = sys.argv[1]
group_name = sys.argv[2]
env_name = sys.argv[3]
aws_access_key = sys.argv[4]
aws_secret_key = sys.argv[5]
description = sys.argv[6]
vpc_id = sys.argv[7]




ec2 = boto3.resource('ec2',
            aws_access_key_id = aws_access_key ,
            aws_secret_access_key = aws_secret_key ,
            region_name = region,
)

client = boto3.client('ec2',
            aws_access_key_id = aws_access_key ,
            aws_secret_access_key = aws_secret_key ,
            region_name = region,
)



def security_group_config(group_name, vpc_id, env_name):
    sg_id = []
    existing_rules = []
    vpc = ec2.Vpc(vpc_id)
    response = client.describe_security_groups()
    count3 = len(response['SecurityGroups'])
    print(count3)
    for x in range(0,count3):
      count4 = len(response['SecurityGroups'])
      if response['SecurityGroups'][x]['VpcId'] ==  vpc_id and response['SecurityGroups'][x]['GroupName'] == group_name:
        #sg_id.append
        sg_id.append(response['SecurityGroups'][x]['GroupId'])
        existing_rules.append(response['SecurityGroups'][x]['IpPermissions'])
    count1 = len(sg_id)
    count2 = len(existing_rules)
    print(count2)
    print(existing_rules)
    if count1 > 0 and count2 > 0:
      security_group = ec2.SecurityGroup(sg_id[0])
      data = security_group.revoke_ingress(
          IpPermissions=existing_rules[0])
    if count1 == 0:
      security_group = vpc.create_security_group(
            Description=description,
            GroupName=group_name,
            DryRun=False,
            )
      sg = str(security_group)
      sg_id.append(sg[22:42])
    csv_name = '{0}{1}'.format(group_name, '.csv')
    print(csv_name)
    path = '{0}{1}'.format('./security-groups/', csv_name)
    IpPermissions = []
    f = open(path)
    csv_f = csv.reader(f)
    headers = next(csv_f)
    print(csv_f)
    for row in csv_f:
        IpPermissions_loop={'IpProtocol': row[0],
            'FromPort': int(row[1]),
            'ToPort': int(row[2]),
            'IpRanges': [{
            'CidrIp': row[3], 
            'Description': row[4]}]}
        IpPermissions.append(IpPermissions_loop) 
    security_group = ec2.SecurityGroup(sg_id[0])
    data = security_group.authorize_ingress(
        IpPermissions=IpPermissions)
    group_name = group_name.upper()
    value = '{0}{1}{2}'.format(env_name, '-', group_name)
    tag = security_group.create_tags(
            DryRun=False,
            Tags=[
            {
                'Key': 'Name',
                'Value': value
            },
        ]
    )


boop69 = security_group_config(group_name, vpc_id, env_name)

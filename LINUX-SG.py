import boto3
from botocore.exceptions import ClientError
import sys

### User definedvars
region = 'us-east-2'
group_name = 'LINUX-SG'
env_name = 'USE2-SB-LAB1'

IpPermissions=[{'IpProtocol': 'tcp',
    'FromPort': 22,
    'ToPort': 22,
    'IpRanges': [{
    'CidrIp': '24.63.0.0/16', 
    'Description': 'Lab CIDR'}]},
    ]


#aws_access_key = sys.argv[1]
#aws_secret_key = sys.argv[2]
description = '{0} {1}'.format(env_name, 'linux instance security group')

ec2 = boto3.resource('ec2',
            #aws_access_key_id = aws_access_key ,
            #aws_secret_access_key = aws_secret_key ,
            region_name = region,
)

client = boto3.client('ec2',
            #aws_access_key_id = aws_access_key ,
            #aws_secret_access_key = aws_secret_key ,
            region_name = region,
)


vpc_name = '{0}{1}'.format(env_name, '-VPC')
vpc_id = []

response = client.describe_vpcs()

count0 = len(response['Vpcs'])

response['Vpcs'][1]['Tags'][0]['Key']

for x in range(0,count0):
    count1 = len(response['Vpcs'][x]['Tags'])
    #print(count1)
    for y in range(0,count1):
        if response['Vpcs'][x]['Tags'][y]['Key'] == 'Name' and response['Vpcs'][x]['Tags'][y]['Value'] == vpc_name:
            vpc_id.append(response['Vpcs'][x]['VpcId'])
        else:
            continue

vpc = ec2.Vpc(vpc_id[0])

###########################################################################
####### Uncomment if you are creating a new security-group ################
###########################################################################
"""
security_group = vpc.create_security_group(
            Description=description,
            GroupName=group_name,
            DryRun=False,
)

sg = str(security_group)
sg_id = sg[22:42]
"""
##########################################################################
##########################################################################
##########################################################################

sg_name = '{0}{1}'.format(env_name, group_name)

sg_id = []

response = client.describe_security_groups()

count3 = len(response['SecurityGroups'])

for x in range(0,count3):
    count4 = len(response['SecurityGroups'])
    for y in range(0,count4):
        if response['SecurityGroups'][y]['VpcId'] ==  vpc_id[0] and response['SecurityGroups'][y]['GroupName'] == group_name:
            sg_id.append(response['SecurityGroups'][y]['GroupId'])
        else:
            continue   
#print(sg_id[0])

security_group = ec2.SecurityGroup(sg_id[0])

##########################################################################
################# comment out if creating new security-group #############
##########################################################################

# First, we remove all existing rules in the group:
security_group.revoke_ingress(IpPermissions=security_group.ip_permissions)


##########################################################################
########################### Security group rules #########################
##########################################################################

sg_rule={'IpProtocol': '-1',
    'FromPort': -1,
    'ToPort': -1,
    'UserIdGroupPairs': [{
    'GroupId': sg_id[0]}]}                              #This will permit hosts, in this security group to talk to themselves

IpPermissions.append(sg_rule)

#Second, we re-apply the rules
data = security_group.authorize_ingress(
        IpPermissions=IpPermissions)


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


import boto3
from botocore.exceptions import ClientError

###vars
sg_id = ''
vpc_id = ''
region = 'us-east-2'

#aws_access_key = sys.argv[1]
#aws_secret_key = sys.argv[2]


###########################################################################
####### Uncomment if you are creating a new security-group ################
###########################################################################

ec2 = boto3.resource('ec2',
            #aws_access_key_id = aws_access_key ,
            #aws_secret_access_key = aws_secret_key ,
            region_name = region,
)

vpc = ec2.Vpc(vpc_id)


security_group = vpc.create_security_group(
            Description='Linux instance security groups',
            GroupName='LINUX-SG',
            DryRun=False,
)

sg = str(security_group)
sg_id = sg[22:42]

##########################################################################
##########################################################################
##########################################################################

security_group = ec2.SecurityGroup(sg_id)

##########################################################################
################# comment out if creating new security-group #############
##########################################################################

# First, we remove all existing rules in the group:
#security_group.revoke_ingress(IpPermissions=security_group.ip_permissions)


##########################################################################
########################### Security group rules #########################
##########################################################################

#Second, we re-apply the rules
data = security_group.authorize_ingress(
        IpPermissions=[
            {'IpProtocol': 'tcp',
            'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{
             'CidrIp': '24.63.0.0/16', 
             'Description': 'Lab CIDR'}]},
            {'IpProtocol': '-1',
            'FromPort': -1,
             'ToPort': -1,
             'UserIdGroupPairs': [{
             'GroupId': sg_id}]}                              #This will permit hosts, in this security group to talk to themselves
            ])

tag = security_group.create_tags(
        DryRun=False,
        Tags=[
        {
            'Key': 'Name',
            'Value': 'USE2-SB-LINUX-SG'
        },
    ]
)

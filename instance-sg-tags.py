import boto3
from botocore.exceptions import ClientError
import sys


region = 'us-east-2'

#aws_access_key = sys.argv[1]
#aws_secret_key = sys.argv[2]


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


###########################################################################
################ Grab a list of all instances in region ###################
###########################################################################

response = client.describe_instances()

count0 = len(response['Reservations'])  #counts how many instances are returned


###########################################################################
################ Run through all instances in returned ####################
###########################################################################

for x in range(0,count0):
    inst_id = response['Reservations'][x]['Instances'][0]['InstanceId']
    #print(inst_id)
    instance = ec2.Instance(inst_id)
    tags = instance.tags
    vpc = instance.vpc
    vpc_str = str(vpc)          # converts aws source to string
    vpc_id = vpc_str[12:33]     # pulls just the vpc_id out of the string
    i = []                      # contains the instance id of instances with tags
    i_dict = {}                 # creates a dictonary, which contains instance id as keyword, and list of security group id's as value
    sg_linux = []               # contains security group id of vpc's linux security group
    sg_windows = []             # contains security group id of vpc's windows security group
    sg_wfe = []                 # contains security group id of vpc's web front end security group
    sg_vpc = []                 # contains all security groups in vpc
    sg_inst = []                # list of security groups, this will become the value in the dictonary
    sg_default = []

###########################################################################
############# Grab a list of all security groups in region ################
###########################################################################

    sg_response = client.describe_security_groups()
    count1 = len(sg_response['SecurityGroups'])
   
    for y in range(0,count1):
        # if a security group belongs to the same vpc as an instance, it will added them to the list sg_vpc
        if sg_response['SecurityGroups'][y]['VpcId'] == vpc_id:
            sg_vpc.append(sg_response['SecurityGroups'][y]['GroupId'])
            #print(sg_response['SecurityGroups'][y]['GroupName']
            i_dict[inst_id] = []

###########################################################################
################# Start searching for matching tags #######################             #if adding a new tag seach, create a list variable in top for loop
###########################################################################

            if sg_response['SecurityGroups'][y]['GroupName'] == 'WFE-SG':               # Searches for Web front end
                gid = (sg_response['SecurityGroups'][y]['GroupId'])
                for tag in tags:
                    #print(tag)
                    if tag['Key'] == 'security:wfe' and tag['Value'] == 'true':
                        i.append(inst_id)
                        sg_inst.append(gid)
                    else:
                        continue

            if sg_response['SecurityGroups'][y]['GroupName'] == 'LINUX-SG':             # Searches for linux instances
                gid = sg_response['SecurityGroups'][y]['GroupId']
                for tag in tags:
                        #print(tag)
                    if tag['Key'] == 'security:linux' and tag['Value'] == 'true':
                        i.append(inst_id)
                        sg_inst.append(gid)
                    else:
                        continue

            if sg_response['SecurityGroups'][y]['GroupName'] == 'WINDOWS-SG':           # Searches for windows instances
                gid = sg_response['SecurityGroups'][y]['GroupId']
                for tag in tags:
                        #print(tag)
                    if tag['Key'] == 'security:windows' and tag['Value'] == 'true':
                        i.append(inst_id)
                        sg_inst.append(gid)
                    else:
                        continue

            if sg_response['SecurityGroups'][y]['GroupName'] == 'default':           # Searches for windows instances
                gid = sg_response['SecurityGroups'][y]['GroupId']
                for tag in tags:
                        #print(tag)
                    if tag['Key'] == 'security:default' and tag['Value'] == 'true':
                        i.append(inst_id)
                        sg_inst.append(gid)
                    else:
                        continue

###########################################################################
################### End search for matching tags #########################
###########################################################################

    i_dict.get(inst_id, []).append(sg_inst)                
    #print(i_dict[inst_id][0])
    if i_dict[inst_id][0] != []:                                                        # For instances with empty security groups skip
        #print(inst_id)
        sg_list = i_dict[inst_id][0]                                                    # security group list is made from list in dictonary
        #print(sg_list)
        sg_instance = ec2.Instance(inst_id)                                            # Select instance 
        sg_instance.modify_attribute(Groups=sg_list)                                   # Update instances using list
    else:
        continue






import boto3
from botocore.exceptions import ClientError


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


response = client.describe_instances()

count0 = len(response['Reservations'])




for x in range(0,count0):
    inst_id = response['Reservations'][x]['Instances'][0]['InstanceId']
    #print(inst_id)
    instance = ec2.Instance(inst_id)
    tags = instance.tags
    vpc = instance.vpc
    vpc_str = str(vpc)
    vpc_id = vpc_str[12:33]
    i = []
    i_dict = {}
    sg_linux = []
    sg_windows = []
    sg_wfe = []
    sg_vpc = []
    sg_inst = []
    #print(vpc_id)
    sg_response = client.describe_security_groups()
    #print(sg_response)
    count1 = len(sg_response['SecurityGroups'])
   
    for y in range(0,count1):
        if sg_response['SecurityGroups'][y]['VpcId'] == vpc_id:
            sg_vpc.append(sg_response['SecurityGroups'][y]['GroupId'])
            #print(sg_response['SecurityGroups'][y]['GroupName']
            i_dict[inst_id] = []
            if sg_response['SecurityGroups'][y]['GroupName'] == 'WFE-SG':
                wfe_id = (sg_response['SecurityGroups'][y]['GroupId'])
                for tag in tags:
                    #print(tag)
                    if tag['Key'] == 'security:wfe' and tag['Value'] == 'true':
                        i.append(inst_id)
                        sg_inst.append(wfe_id)
                    else:
                        continue                      
            if sg_response['SecurityGroups'][y]['GroupName'] == 'LINUX-SG':
                linux_id = sg_response['SecurityGroups'][y]['GroupId']
                for tag in tags:
                        #print(tag)
                    if tag['Key'] == 'security:linux' and tag['Value'] == 'true':
                        i.append(inst_id)
                        sg_inst.append(linux_id)
                    else:
                        continue
            if sg_response['SecurityGroups'][y]['GroupName'] == 'WINDOWS-SG':
                windows_id = sg_response['SecurityGroups'][y]['GroupId']
                for tag in tags:
                        #print(tag)
                    if tag['Key'] == 'security:windows' and tag['Value'] == 'true':
                        i.append(inst_id)
                        sg_inst.append(windows_id)
                    else:
                        continue
    i_dict.get(inst_id, []).append(sg_inst)                
    #print(i_dict[inst_id][0])
    if i_dict[inst_id][0] != []:
        print(inst_id)
        sg_list = i_dict[inst_id][0]
        print(sg_list)
        #sg_instance = ec2.Instance(inst_id)
        #sg_instance.modify_attribute(Groups=sg_list)
    else:
        continue


#!/usr/bin/python
import json
from lxml import etree
from jnpr.junos.op import arp
from jnpr.junos import Device
import requests
import sys

lookup_ip = sys.argv[1]

username = "root"
password = sys.argv[2]
api_token = sys.argv[3]


ipam_server = "http://192.168.1.131"
app_name = "lab"


session = requests.Session()
headers = {'Content-Type': 'application/json',
		 'phpipam-token': api_token'}



def ip_address_search(ip_address):
	xpath = '{0}{1}{2}{3}{4}'.format('/api/', app_name, '/addresses/search/', ip_address, "/")
	url = '{0}{1}'.format(ipam_server, xpath)	
	device_response = session.get(url, verify=False, headers=headers)
	json_device_response = json.loads(device_response.content)
	return json_device_response['data'][0]['subnetId']



def subnet_lookup(subnet_id):
	xpath = '{0}{1}{2}{3}{4}'.format('/api/', app_name, '/subnets/', subnet_id, "/")
	url = '{0}{1}'.format(ipam_server, xpath)	
	device_response = session.get(url, verify=False, headers=headers)
	json_device_response = json.loads(device_response.content)
	return json_device_response['data']['device']


def device_lookup(device_id):
	xpath = '{0}{1}{2}{3}{4}'.format('/api/', app_name, '/devices/', device_id, "/")
	url = '{0}{1}'.format(ipam_server, xpath)	
	device_response = session.get(url, verify=False, headers=headers)
	json_device_response = json.loads(device_response.content)
	return json_device_response['data']['ip']




subnet_id = ip_address_search(lookup_ip)
device_id = subnet_lookup(subnet_id)
device_ip = device_lookup(device_id)
print(device_ip)




dev = Device(host=device_ip, user=username, password=password)
dev.open()


arp_table = arp.ArpTable(dev)
arp_table.get(hostname=lookup_ip)


mac_key = arp_table.keys()
mac_value = arp_table.values()
mac_add = mac_key[0]
mac_info = mac_value[0]


print("IP Addresses")
print(mac_info[1][1])
print("Interface")
print(mac_info[0][1])
print("MAC Address")
print(mac_info[2][1])

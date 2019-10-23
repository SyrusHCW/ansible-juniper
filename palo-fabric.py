#!/usr/bin/python2.7
from pandevice import firewall
from pandevice import network
from pandevice import policies
from pandevice import panorama
from pandevice import base
from pandevice import device
import pan.xapi
import sys

#vars
username = sys.argv[1]
password = sys.argv[2]
panorama_dns = sys.argv[3]
template = sys.argv[4]
vlan_id = sys.argv[5]
virtual_router = sys.argv[6]
interface_id = sys.argv[7]
interface_prefix = sys.argv[8]
interface_octet = sys.argv[9]
vsys_name = sys.argv[10]
name = virtual_router.split("vr-")
vlan_name = name[1]
zone_name = name[1]
router_id = sys.argv[11]
present = sys.argv[12]
ospf_area = sys.argv[13]


if present == "false":
        quit()

panorama_instance = firewall.Firewall(panorama_dns, username, password)

ip_addr1 = '{0}{1}{2}{3}{4}'.format('169.254.', vlan_id, '.', interface_octet, '/30')


interface1 = '{0}{1}{2}{3}'.format(interface_id, '.', interface_prefix, vlan_id)

tag1 = '{0}{1}'.format(interface_prefix, vlan_id)


device_template = panorama.Template(template)
panorama_instance.add(device_template)

vsys = device.Vsys(vsys_name)
device_template.add(vsys)

# Create Interface 1

subeth = network.Layer3Subinterface(interface1, \
        tag = tag1, \
        ip = ip_addr1)

vsys.add(subeth)

try:
	subeth.create()
except:
	print('nah')
	
subeth.create()


#Attach interface1 to routing instance, and zone

routing_instance = network.VirtualRouter(virtual_router,\
			interface = interface1)

vsys.add(routing_instance)
routing_instance.create()


zone = network.Zone(zone_name, \
        mode = "layer3", \
        interface = interface1)

vsys.add(zone)
zone.create()

#Attach interface1 to routing instance, and zone

routing_ospf = network.Ospf(enable = "True",\
                        router_id = router_id,\
                        reject_default_route = "False")

vsys.add(routing_ospf)
routing_ospf.create()


routing_area = network.OspfArea(name = ospf_area,\
                        type = "nssa",\
                        accept_summary = "true")

vsys.add(routing_area)
routing_area.create()




zone = network.Zone(zone_name, \
        mode = "layer3", \
        interface = interface1)

vsys.add(zone)
zone.create()


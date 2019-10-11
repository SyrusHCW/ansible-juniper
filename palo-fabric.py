#!/usr/bin/python
from pandevice import firewall
from pandevice import network
from pandevice import policies
from pandevice import panorama
from pandevice import base
from pandevice import device
import pan.xapi
import sys

#vars
panorama_dns = '18.214.36.168'
username = sys.argv[1]
password = sys.argv[2]
vlan_id = sys.argv[3]
eth1_23_prefix = sys.argv[4]
eth1_23_octet = sys.argv[5]
template = sys.argv[6]
virtual_router = sys.argv[7]
vsys_name = sys.argv[8]
zone_name = sys.argv[9]

panorama_instance = firewall.Firewall(panorma_dns, username, password)


ip_addr = '{0}{1}{2}{3}{4}'.format('169.254.', vlan_id, '.', eth1_23_octet, '/30')


interface1 = '{0}{1}{2}'.format('ethernet1/3.', eth1_23_prefix, vlan_id)
tag = '{0}{1}'.format(eth1_23_prefix, vlan_id)


device_template = panorama.Template(template)
panorama_instance.add(device_template)

vsys = device.Vsys(vsys_name)
device_template.add(vsys)

# Create Interface

subeth = network.Layer3Subinterface(interface1, \
        tag = tag, \
        ip = ip_addr,\
        mtu = '9178')

vsys.add(subeth)

try:
	subeth.create()
except:
	print('nah')


subeth.create()

#Attach interface to routing instance

routing_instance = network.VirtualRouter(virtual_router,\
			interface = interface1)

vsys.add(routing_instance)
routing_instance.create()


zone = network.Zone(zone_name, \
        mode = "layer3", \
        interface = interface1)

vsys.add(zone)
zone.create()


xapi = pan.xapi.PanXapi(api_username = username, \
        api_password = password, \
        hostname= panorama_dns)


ospf_xml = "<bfd><profile>Inherit-vr-global-setting</profile></bfd><enable>yes</enable><passive>no</passive><gr-delay>10</gr-delay><metric>10</metric><priority>1</priority><hello-interval>10</hello-interval><dead-counts>4</dead-counts><retransmit-interval>5</retransmit-interval><transit-delay>1</transit-delay><link-type><p2p /></link-type>"
xpath1 = '{0}{1}{2}{3}{4}{5}{6}'.format("/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='", template, "']/config/devices/entry[@name='localhost.localdomain']/network/virtual-router/entry[@name='", virtual_router, "']/protocol/ospf/area/entry[@name='0.0.0.0']/interface/entry[@name='",interface1, "']")

xapi.set(xpath = xpath1, \
                element = ospf_xml)



ecmp_xml = "<ecmp><algorithm><ip-hash><use-port>yes</use-port></ip-hash></algorithm><enable>yes</enable><max-path>4</max-path></ecmp>"
xpath1 = '{0}{1}{2}{3}{4}'.format("/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='", template, "']/config/devices/entry[@name='localhost.localdomain']/network/virtual-router/entry[@name='", virtual_router, "']")

xapi.set(xpath = xpath1, \
                element = ecmp_xml)

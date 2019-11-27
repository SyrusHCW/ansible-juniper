#!/usr/bin/python
import pan.xapi
from pandevice import network
from pandevice import panorama
import sys


username = sys.argv[1]
password = sys.argv[2]
panorama_name = sys.argv[3]             # DNS name or IP address of Panorama instance
template = sys.argv[4]
zone = sys.argv[5]

# Function for creating template variables in a template
def create_template_variable(username, password, panorama_name, variable, value, variable_type, template):
    xapi = pan.xapi.PanXapi(api_username = username, \
        api_password = password, \
        hostname= panorama_name)
    xpath = '{0}{1}{2}'.format("/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='", template, "']/variable")
    element = '{0}{1}{2}{3}{4}{5}{6}{7}{8}'.format('<entry name="', variable, '"><type><', variable_type, '>', value, '</', variable_type, '></type></entry>')
    xapi.set(xpath = xpath, \
        element = element)

var_suffix = zone.replace("-", "_")
lower_var_suffix = var_suffix.lower()

# Format BGP Variable names
variable_bgp_neighbor_az1 = '{0}{1}{2}'.format('$bgp_neighbor_', lower_var_suffix, '_az1')
variable_bgp_neighbor_az2 = '{0}{1}{2}'.format('$bgp_neighbor_', lower_var_suffix, '_az2')

bgp_neighbor_az1 = create_template_variable(username = username,\
        password =  password,\
        panorama_name = panorama_name,\
        variable = variable_bgp_neighbor_az1,\
        value = '169.254.0.0',\
        variable_type = 'ip-netmask',\
        template = template)

bgp_neighbor_az2 = create_template_variable(username = username,\
        password =  password,\
        panorama_name = panorama_name,\
        variable = variable_bgp_neighbor_az2,\
        value = '169.254.0.0',\
        variable_type = 'ip-netmask',\
        template = template)

# Format Tunnel Variable names
variable_tunnel_az1 = '{0}{1}{2}'.format('$tunnel_', lower_var_suffix, '_az1_cidr')
variable_tunnel_az2 = '{0}{1}{2}'.format('$tunnel_', lower_var_suffix, '_az2_cidr')

tunnel_az1 = create_template_variable(username = username,\
        password =  password,\
        panorama_name = panorama_name,\
        variable = variable_tunnel_az1,\
        value = '169.254.0.0',\
        variable_type = 'ip-netmask',\
        template = template)

tunnel_az2 = create_template_variable(username = username,\
        password =  password,\
        panorama_name = panorama_name,\
        variable = variable_tunnel_az1,\
        value = '169.254.0.0',\
        variable_type = 'ip-netmask',\
        template = template)

print(variable_bgp_neighbor_az1)
print(variable_bgp_neighbor_az2)
print(variable_tunnel_az1)
print(variable_tunnel_az2)

#!/usr/bin/python

zone = 'USE1-QE'
var_suffix = zone.replace("-", "_")
lower_var_suffix = var_suffix.lower()

# Format BGP Variable names
variable_bgp_neighbor_az1 = '{0}{1}{2}'.format('$bgp_neighbor_', lower_var_suffix, '_az1')
variable_bgp_neighbor_az2 = '{0}{1}{2}'.format('$bgp_neighbor_', lower_var_suffix, '_az2')

print(variable_bgp_neighbor_az1)
print(variable_bgp_neighbor_az2)

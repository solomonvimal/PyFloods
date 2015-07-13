# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 22:22:58 2015
HydroShare: learning to use API
@author: Solo
"""

from hs_restclient import HydroShare
hs = HydroShare()
resources = []
for resource in hs.getResourceList():
    resources.append(resource)
    
len(resources)

from hs_restclient import HydroShare, HydroShareAuthBasic
auth = HydroShareAuthBasic(username='solomon.vimal@gmail.com', password='n0m0l0slamiv')
hs = HydroShare(auth=auth)
for resource in hs.getResourceList():
    print(resource)
    resources.append(resource)
    
# To create a resource:

from hs_restclient import HydroShare, HydroShareAuthBasic
auth = HydroShareAuthBasic(username='solomon.vimal@gmail.com', password='n0m0l0slamiv')
hs = HydroShare(auth=auth)
abstract = 'My abstract'
title = 'My resource'
keywords = ('North Carolina', 'HEC-RAS', 'Flood Risk Information System')
rtype = 'GenericResource'
fpath = '/path/to/a/file'
resource_id = hs.createResource(rtype, title, resource_file=fpath, keywords=keywords, abstract=abstract)
#!/usr/bin/env python

import os
from os import listdir
from os.path import isfile, join

mypath = '/home/dmaher/Development/GLOS/glider/'
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

for each in onlyfiles if each.endswith('ebd'):
    os.system('./dbd2asc %s | ./dba_sensor_filter -f standard_sensors.txt  > %s.asc'%(each,each))

for each in onlyfiles if each.endswith('dbd'):
    os.system('./dbd2asc %s | ./dba_sensor_filter -f standard_sensors.txt  > %s.asc'%(each,each))

for each in onlyfiles if each.endswith('ebd'):
    each = each.split('.')
    os.system('./dba_merge %s.ebd.asc %s.dbd.asc > %s.dba '%(each[0],each[0],each[0]))





#!/usr/bin/env python

import sys
import os

# Catch arguments
FileNameIn = str(sys.argv[1])
FileNameOut = str(sys.argv[2])

session_name = str(sys.argv[3])
work_dir = str(sys.argv[4])
save_dir = str(sys.argv[5])
config_dir = str(sys.argv[6])
dir_reference = str(sys.argv[7])
poly_dir = str(sys.argv[8])

# Open and read launcher file
In = open(FileNameIn, 'r')
lines = In.readlines()
In.close()

# Write launcher file
Out = open(FileNameOut, 'w')

for l in lines:
    if ('$session_name' in l):
        Out.write(l.replace('$session_name',session_name))
    elif ('$work_dir' in l):
        Out.write(l.replace('$work_dir',work_dir))
    elif ('$save_dir' in l):
        Out.write(l.replace('$save_dir',save_dir))
    elif ('$config_dir' in l):
        Out.write(l.replace('$config_dir',config_dir))
    elif ('$dir_reference' in l):
        Out.write(l.replace('$dir_reference',dir_reference))
    elif ('$poly_dir' in l):
        Out.write(l.replace('$poly_dir',poly_dir))
    else:
        Out.write(l)
        
Out.close()

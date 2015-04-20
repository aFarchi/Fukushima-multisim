#!/usr/bin/env python

import sys
import os

# Catch arguments
FileNameIn = str(sys.argv[1])
FileNameOut = str(sys.argv[2])

# Open and read launcher file
In = open(FileNameIn, 'r')
lines = In.readlines()
In.close()

# Write launcher file
Out = open(FileNameOut, 'w')

for l in lines:
    nbr_nodes, server_name = l.split('/')
    Out.write('1/'+server_name)
        
Out.close()

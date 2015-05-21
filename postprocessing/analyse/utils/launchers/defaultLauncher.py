#!/usr/bin/env python
import os
import sys

fileProcesses = '$fileProcesses$'
nProcessors   = 4
launcher      = '$launcher$'
interpretor   = '$interpretor$'

f             = open(fileProcesses, 'r')
lines         = f.readlines()
f.close()

header        = lines.pop(0).replace('\n','')
argsNames     = header.split('\t')

currentNTask  = 0

print('$startString$')

for line in lines:

    if (currentNTask == nProcessors):
        print(os.wait())
    else:
        currentNTask += 1
        
    pid = os.fork()
        
    if (pid == 0):
        args    = line.replace('\n','').split('\t')
        command = interpretor + ' ' + launcher
        for (argName, arg) in zip(argsNames, args):
            command += ' ' + argName + '=' + arg

        print command
        sys.exit(os.system(command))
        
for i in xrange(currentNTask):
    print(os.wait())


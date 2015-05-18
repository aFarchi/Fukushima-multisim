#!/bin/bash

fileProcesses='$fileProcesses$'
nodes='$nodesFile$'
logfile='$logFile$'
launcher='$launcher$'

echo '$startString$ ...'
echo 'algo start --argument-file='$fileProcesses' --computer-file='$nodes' --log='$logfile' run '$launcher
algo start --argument-file=$fileProcesses --computer-file=$nodes --log=$logfile run $launcher
#!/bin/bash

fileProcesses='$fileProcesses$'
nodes='$fileNodes$'
logfile='$logFile$'
launcher='$launcher$'

echo '$startString$ ...'
echo 'algo start --argument-file='$fileProcesses' --computer-file='$nodes' --log='$logfile' run '$launcher
algo start --argument-file=$fileProcesses --computer-file=$nodes --log=$logfile run $launcher
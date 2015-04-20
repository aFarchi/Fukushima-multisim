#!/bin/bash

# Arborescence:
# -------------
# work_fukushima:
#    * config
#    * reference_data
#    * output
#    * launchers
#        * utils
#        * list_of_processes
#        * list_of_nodes

work_dir='/libre/farchia/output-multisim/'
poly_dir='/cerea_raid/users/farchia/Polyphemus-1.8.1-work-12-05-2014/'
dir_work_fukushima='/cerea_raid/users/farchia/work_fukushima/'

dir_config=$dir_work_fukushima'config/'
dir_reference_data=$dir_work_fukushima'reference_data/'
dir_output=$dir_work_fukushima'output/'
dir_launchers=$dir_work_fukushima'launchers/'

file_processes_final=$dir_work_fukushima'/launchers/list_processes.dat'
launcher=$dir_launchers'utils/launcher.py'

if [[ $1='' ]]
then
    session_name='sim-test'
else
    session_name=$1
fi

if [[ $2='' ]]
then
    launcher_to_complete=$dir_launchers'utils/launcher_to_complete.py'
else
    launcher_to_complete=$2
fi

if [[ $3='' ]]
then
    file_processes=$dir_launchers'list_of_processes/list_processes_shift.dat'
else
    file_processes=$3
fi

if [[ $4='' ]]
then
    nodes=$dir_launchers'list_of_nodes/nodes_om_rest.dat'
else
    nodes=$4
fi

if [[ $5='' ]]
then
logfile=$dir_output$session_name'/log'
else
logfile=$dir_output$session_name'/'$5
fi

echo 'Creating output directory : '$dir_output$session_name
mkdir -p $dir_output$session_name
cp $file_processes $dir_output$session_name

echo 'Making list of processes to execute : '$file_processes
rm -f $file_processes_final
python utils/make_list_of_processes.py $file_processes $file_processes_final
cp $file_processes_final $dir_output$session_name

echo 'Filling in launcher file : '$launcher_to_complete
rm -f $launcher
python utils/make_launcher.py $launcher_to_complete $launcher $session_name $work_dir $dir_output $dir_config $dir_reference_data $poly_dir
chmod +x $launcher

echo 'Starting algorithm ...'
echo 'algo start --argument-file='$file_processes_final' --computer-file='$nodes' --log='$logfile' run '$launcher
algo start --argument-file=$file_processes_final --computer-file=$nodes --log=$logfile run $launcher

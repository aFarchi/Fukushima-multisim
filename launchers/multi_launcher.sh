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
#
# Fill here the coresponding directories
#

work_dir='/libre/farchia/output-multisim/'
poly_dir='/cerea_raid/users/farchia/Polyphemus-1.8.1-work-12-05-2014/'
dir_work_fukushima='/cerea_raid/users/farchia/Fukushima-multisim/'

dir_config=$dir_work_fukushima'config/'
dir_reference_data=$dir_work_fukushima'reference_data/'
dir_output=$dir_work_fukushima'output/'
dir_launchers=$dir_work_fukushima'launchers/'

file_processes_final=$dir_work_fukushima'/launchers/list_processes.dat'
launcher=$dir_launchers'utils/launcher.py'
synchronizer=$dir_launchers'utils/synchronizer.py'
nodes_rest=$dir_launchers'list_of_nodes/nodes_om_rest.dat'

if [[ $1='' ]]
then
    session_name='sim-test-2'
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
    synchronizer_to_complete=$dir_launchers'utils/synchronizer_to_complete.py'
else
    synchronizer_to_complete=$3
fi

if [[ $4='' ]]
then
    file_processes=$dir_launchers'list_of_processes/list_processes_shift.dat'
else
    file_processes=$4
fi

if [[ $5='' ]]
then
    nodes=$dir_launchers'list_of_nodes/nodes_om_rest.dat'
else
    nodes=$5
fi

if [[ $6='' ]]
then
logfile=$dir_output$session_name'/log'
else
logfile=$dir_output$session_name'/'$6
fi

echo 'Creating output directory : '$dir_output$session_name
mkdir -p $dir_output$session_name
cp $file_processes $dir_output$session_name

echo 'Making list of processes to execute : '$file_processes
rm -f $file_processes_final
python $dir_launchers'utils/make_list_of_processes.py' $file_processes $file_processes_final
cp $file_processes_final $dir_output$session_name

echo 'Filling in launcher file : '$launcher_to_complete
rm -f $launcher
python $dir_launchers'utils/make_launcher.py' $launcher_to_complete $launcher $session_name $work_dir $dir_output $dir_config $dir_reference_data $poly_dir
chmod +x $launcher

echo 'Filling in synchronizer file : '$synchronizer_to_complete
rm -f $synchronizer
python $dir_launchers'utils/make_launcher.py' $synchronizer_to_complete $synchronizer $session_name $work_dir $dir_output $dir_config $dir_reference_data $poly_dir
chmod +x $synchronizer

cp $dir_config'dir_config' $dir_output$session_name

echo 'Reading nodes list :'$nodes
rm -f $nodes_rest
python $dir_launchers'list_of_nodes/make_list_of_nodes_rest.py' $nodes $nodes_rest

echo 'Starting synchronizing heavy data ...'
echo 'algo start --argument-file='$file_processes_final' --computer-file='$nodes_rest' --log='$logfile' run '$synchronizer
algo start --argument-file=$file_processes_final --computer-file=$nodes_rest --log=$logfile run $synchronizer

echo 'Starting algorithm ...'
echo 'algo start --argument-file='$file_processes_final' --computer-file='$nodes' --log='$logfile' run '$launcher
algo start --argument-file=$file_processes_final --computer-file=$nodes --log=$logfile run $launcher

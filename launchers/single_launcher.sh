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

resolution=0d05
source_term=Winiarek_d22
psd_source=Jaenicke_Remote_continental_AP
meteo=WRF 
kz=TM
rain=Radar
ics=water_dependent_aer
icsunder=IRSN
bcs=rain_dependent_aer
bcsunder=IRSN
dry_dep=constant
dx=0p0
dy=0p0 
dz=0p0
dt=0p0

if [[ $3='' ]]
then
    logfile=$dir_output$session_name'/log'
else
    logfile=$dir_output$session_name'/'$3
fi

echo 'Creating output directory : '$dir_output$session_name
mkdir -p $dir_output$session_name

echo 'Filling in launcher file : '$launcher_to_complete
rm -f $launcher
python utils/make_launcher.py $launcher_to_complete $launcher $session_name $work_dir $dir_output $dir_config $dir_reference_data $poly_dir
chmod +x $launcher

echo 'Starting algorithm ...'
echo 'python '$launcher' RESOLUTION='$resolution' SOURCE='$source_term' PSD_SOURCE='$psd_source' METEO='$meteo' KZ='$kz' RAIN='$rain' ICS='$ics' ICSunder='$icsunder' BCS='$bcs' BCSunder='$bcsunder' DRY_DEP='$dry_dep' DX='$dx' DY='$dy' DZ='$dz' DT='$dt' > '$logfile

python $launcher RESOLUTION=$resolution SOURCE=$source_term PSD_SOURCE=$psd_source METEO=$meteo KZ=$kz RAIN=$rain ICS=$ics ICSunder=$icsunder BCS=$bcs BCSunder=$bcsunder DRY_DEP=$dry_dep DX=$dx DY=$dy DZ=$dz DT=$dt > $logfile


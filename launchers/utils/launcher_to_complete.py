#!/usr/bin/env python

import os
import sys
import utils_synchronize_heavy_data as ushd
import utils_write_source as uws
import utils_write_config as uwc

def myrun(command):
	status = os.system(command)
	print command
	if status != 0:
		sys.exit(status)

def myrun_test(command):
	status = os.system(command)
	print command
	if status != 0:
		sys.exit(status)

#####################################################
# Read the list of parameters
sys.argv.pop(0)
parameters=dict()
for arg in sys.argv:
	members=arg.split('=')
	parameters[members[0]]=members[1]
print parameters

# Extraction of the parameters
BCS_proc = parameters['BCS']
BCSunder_proc = parameters['BCSunder']
ICS_proc = parameters['ICS']
ICSunder_proc = parameters['ICSunder']
DryDep_proc = parameters['DRY_DEP']
Reso_proc = parameters['RESOLUTION']
Source_proc = parameters['SOURCE']
PSD_Source_proc = parameters['PSD_SOURCE']
Met_proc = parameters['METEO']
Kz_proc = parameters['KZ']
Rain_proc = parameters['RAIN']
dx_proc = parameters['DX']
dy_proc = parameters['DY']
dz_proc = parameters['DZ']
dt_proc = parameters['DT']

session_name = '$session_name'
work_dir = '$work_dir'
save_dir = '$save_dir'
config_dir = '$config_dir'
dir_reference = '$dir_reference'
poly_dir = '$poly_dir'

suffix_proc = uws.fn_of_shifts(dx_proc,dy_proc,dz_proc,dt_proc)

#####################################################
# Writes the source term for the appropriate shift of the source
DX_Unit = 1.
DY_Unit = 1.
DZ_Unit = 1.
DT_Unit = 1.
SourceFile = dir_reference+'source_shift/D22.bin'
uws.write_source_term(SourceFile, work_dir, PSD_Source_proc, dx_proc, dy_proc, dz_proc, dt_proc, DX_Unit, DY_Unit, DZ_Unit, DT_Unit)
uws.writeSourceTermGas(dir_reference+'source/IRSN_one_Gases.dat', work_dir, dx_proc, dy_proc, dz_proc, dt_proc, DX_Unit, DY_Unit, DZ_Unit, DT_Unit)

#####################################################
# File destruction and creation
relative_path = (session_name+'/'
		 +Reso_proc +'-'
		 +Source_proc+'_'+PSD_Source_proc +'-'
		 +Met_proc +'-'
		 +Kz_proc +'-'
		 +Rain_proc +'-'
		 +DryDep_proc +'-'
		 +ICS_proc +'-'
		 +ICSunder_proc +'-'
		 +BCS_proc +'-'
		 +BCSunder_proc+'-'
		 +suffix_proc)

myrun('rm -fr  ' + work_dir + relative_path)
for rep in ['nesting', 'dry', 'wet/InCloud', 'wet/BelowCloud']:
	myrun('mkdir -p ' + work_dir + relative_path + '/' + rep)

#####################################################
# Writes the config files
uwc.write_config_general(config_dir, work_dir, relative_path, Reso_proc, BCS_proc, ICS_proc, DryDep_proc)
uwc.write_config_data(config_dir, work_dir, relative_path, Met_proc, Source_proc, PSD_Source_proc, suffix_proc, Reso_proc, Kz_proc, Rain_proc, DryDep_proc)
uwc.write_config_saver(config_dir, work_dir, relative_path, Reso_proc)
uwc.write_config_species(config_dir, work_dir, relative_path, BCS_proc, BCSunder_proc, ICS_proc, ICSunder_proc)
uwc.write_config_land(config_dir, work_dir, relative_path, Reso_proc)

#####################################################
# Launches of the program
os_name = os.environ['OS_NAME']
if os_name[0:8]=='debian-5':
	myrun_test(poly_dir + 'processing/decay/polair3d-decay-lenny '+ work_dir + relative_path + '/general.cfg')
elif os_name[0:8]=='debian-6':
	myrun_test(poly_dir + 'processing/decay/polair3d-decay-lenny '+ work_dir + relative_path + '/general.cfg')
#	myrun_test(poly_dir + 'processing/decay/polair3d-decay-squeeze '+ work_dir + relative_path + '/general.cfg')
elif os_name=='ubuntu-12.04':
	myrun_test(poly_dir + 'processing/decay/polair3d-decay-lenny '+ work_dir + relative_path + '/general.cfg')
#	myrun_test(poly_dir + 'processing/decay/polair3d-decay-ubuntu12 '+ work_dir + relative_path + '/general.cfg')
elif os_name=='ubuntu-14.04':
	myrun_test(poly_dir + 'processing/decay/polair3d-decay-lenny '+ work_dir + relative_path + '/general.cfg')
#	myrun_test(poly_dir + 'processing/decay/polair3d-decay-ubuntu14 '+ work_dir + relative_path + '/general.cfg')
else:
	print 'No program for the os '+os_name
	sys.exit(1)

#####################################################
# If the run is successful
# Saves to the local hard drive
myrun('hostname')
myrun('mkdir -p '+save_dir+relative_path+'/')
myrun_test('rm -rf '+save_dir+relative_path+'/')
myrun_test('time rsync -aP --append-verify '+work_dir+relative_path+'/ '+save_dir+relative_path+'/')
# clean the computing server
myrun_test('rm -rf '+work_dir+relative_path+'/')

import os
import sys
import platform

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

def synchronize_heavy_data(work_dir, dir_reference):
    # Import machine where the program is running
    machine = platform.node()
    print(machine)

    # Synchronyse the heavy (dep, meteo and ground)
    # data with the reference data
    myrun('/bin/mkdir -p ' + work_dir + 'heavy_data/0d05/')
    myrun_test('/usr/bin/time /usr/bin/rsync -arP --append-verify '
               + dir_reference + '0d05/'
               + ' '
               + work_dir
               + 'heavy_data/0d05/')

    # Synchronyses basic source term
    myrun('/bin/mkdir -p ' + work_dir + 'heavy_data/source/')
    myrun('/bin/mkdir -p ' + work_dir + 'heavy_data/source_shift/')
    myrun_test('/usr/bin/time /usr/bin/rsync -arP --append-verify '
               + dir_reference + 'source/'
               + ' '
               + work_dir
               + 'heavy_data/source_shift/')
    return 0


#!/usr/bin/env python

from numpy import *
import os
import sys
import string
import re

def myrun(command):
  status = os.system(command)
  if status != 0:
    sys.exit(status)


#####################################################
# Read the list of processes
filename = str(sys.argv[1])
fn = open(filename, 'r')
line = fn.readlines()

processes = []
j = 0
for i in range(len(line)):
  # Remove blank, tab and \n
  temp = line[i].strip()
  temp = temp.replace(" ", "")
  # Remove comment
  temp = temp.split("#")[0]
  if (temp != ''):
    # Split the data
    processes.append(re.split('[:|,=]', temp))

#######################################################
# Read the file name for the output
filenameout = str(sys.argv[2])

#######################################################
# Header
Out = open(filenameout,'w')
Out.write('RESOLUTION\t'
          +'SOURCE\t'
          +'PSD_SOURCE\t'
          +'METEO\t'
          +'KZ\t'
          +'RAIN\t'
          +'ICS\t'
          +'ICSunder\t'
          +'BCS\t'
          +'BCSunder\t'
          +'DRY_DEP\t'
          +'DX\t'
          +'DY\t'
          +'DZ\t'
          +'DT\t'
          +'\n')

# Extraction of the processes nums
for num in range(len(processes)):
  if processes[num][0] == 'BCS':
    BCS_num = num
  elif processes[num][0] == 'ICS':
    ICS_num = num
  elif processes[num][0] == 'DRY_DEP':
    DryDep_num = num
  elif processes[num][0] == 'RESOLUTION':
    Reso_num = num
  elif processes[num][0] == 'SOURCE':
    Source_num = num
  elif processes[num][0] == 'PSD_SOURCE':
    PSD_Source_num = num
  elif processes[num][0] == 'METEO':
    Met_num = num
  elif processes[num][0] == 'KZ':
    Kz_num = num
  elif processes[num][0] == 'RAIN':
    Rain_num = num
  elif processes[num][0] == 'DX':
    dx_num = num
  elif processes[num][0] == 'DY':
    dy_num = num
  elif processes[num][0] == 'DZ':
    dz_num = num
  elif processes[num][0] == 'DT':
    dt_num = num

def write_to_file(f,Reso,Source,PSD_Source,Met,Kz,Rain,ICS,ICSunder,BCS,BCSunder,DryDep,dx,dy,dz,dt):
  f.write(Reso+'\t'+Source+'\t'+PSD_Source+'\t'+Met+'\t'+Kz+'\t'+Rain+'\t'+ICS+'\t'+ICSunder+'\t'+BCS+'\t'+BCSunder+'\t'+DryDep+'\t'
          +dx+'\t'+dy+'\t'+dz+'\t'+dt+'\t'+'\n')
  
def write_line(file,i,j,k,l,m,q,n,o,p,idx,idy,idz,idt):
  BCS = processes[BCS_num][i]
  ICS = processes[ICS_num][j]
  DryDep = processes[DryDep_num][k]
  Reso = processes[Reso_num][l]
  Source = processes[Source_num][m]
  PSD_Source = processes[PSD_Source_num][q]
  Met = processes[Met_num][n]
  Kz = processes[Kz_num][o]
  Rain = processes[Rain_num][p]
  dx = processes[dx_num][idx]
  dy = processes[dy_num][idy]
  dz = processes[dz_num][idz]
  dt = processes[dt_num][idt]

  if ((BCS == 'monodispersed_slinn'
       or BCS == 'monodispersed_mod'
       or BCS == 'polydispersed_slinn'
       or BCS == 'polydispersed_mod'
       or BCS == 'rain_dependent_aer')
      and (ICS == 'water_dependent_aer')): # undermodel for both ICS and BCS
    for num in range(len(processes)):
      if processes[num][0] == BCS:
        BCSunder_num = num
      elif processes[num][0] == ICS:
        ICSunder_num = num
    for y in range(1,len(processes[BCSunder_num])):
      for z in range(1,len(processes[ICSunder_num])):
        BCSunder = processes[BCSunder_num][y]
        ICSunder = processes[ICSunder_num][z]
        write_to_file(file,Reso,Source,PSD_Source,Met,Kz,Rain,ICS,ICSunder,BCS,BCSunder,DryDep,dx,dy,dz,dt)

  elif (BCS == 'monodispersed_slinn'
        or BCS == 'monodispersed_mod'
        or BCS == 'polydispersed_slinn'
        or BCS == 'polydispersed_mod'
        or BCS == 'rain_dependent_aer'): # undermodel for BCS       
    for num in range(len(processes)):
      if processes[num][0] == BCS:
        BCSunder_num = num
    for y in range(1,len(processes[BCSunder_num])):
      BCSunder = processes[BCSunder_num][y]
      ICSunder = 'none'
      write_to_file(file,Reso,Source,PSD_Source,Met,Kz,Rain,ICS,ICSunder,BCS,BCSunder,DryDep,dx,dy,dz,dt)

  elif (ICS == 'rain_dependent_aer'): # undermodel for ICS
    for num in range(len(processes)):
      if  processes[num][0] == ICS:
        ICSunder_num = num
    for z in range(1,len(processes[ICSunder_num])):
      ICSunder = processes[ICSunder_num][z]
      BCSunder = 'none'
      write_to_file(file,Reso,Source,PSD_Source,Met,Kz,Rain,ICS,ICSunder,BCS,BCSunder,DryDep,dx,dy,dz,dt)
      

  else: # no under model
    BCSunder = 'none'
    ICSunder = 'none'
    write_to_file(file,Reso,Source,PSD_Source,Met,Kz,Rain,ICS,ICSunder,BCS,BCSunder,DryDep,dx,dy,dz,dt)
  return

# N Loop on the N processes
for i in range(1,len(processes[BCS_num])):
  for j in range(1,len(processes[ICS_num])):
    for k in range(1,len(processes[DryDep_num])):
      for l in range(1,len(processes[Reso_num])):
        for m in range(1,len(processes[Source_num])):
          for n in range(1,len(processes[Met_num])):
            for o in range(1,len(processes[Kz_num])):
              for p in range(1,len(processes[Rain_num])):
                  for q in range(1,len(processes[PSD_Source_num])):
                    for idx in range(1,len(processes[dx_num])):
                      for idy in range(1,len(processes[dy_num])):
                        for idz in range(1,len(processes[dz_num])):
                          for idt in range(1,len(processes[dt_num])):
                            write_line(Out,i,j,k,l,m,q,n,o,p,idx,idy,idz,idt)



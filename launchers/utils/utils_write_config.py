import sys
import os

def write_config_general(config_dir, work_dir, relative_path, Reso_proc, BCS_proc, ICS_proc, DryDep_proc):
    In = open(config_dir+'general.cfg','r')
    line = In.readlines()
    In.close()
    FileName = work_dir+relative_path+'/general.cfg'
    Out = open(FileName, 'w')
    for l in line:
        # scales
        if ('Delta_x = ' in l):
            if (Reso_proc=='0d25'):
                Out.write(l.replace('$Delta_x$', '0.25'))
            elif (Reso_proc=='0d05'):
                Out.write(l.replace('$Delta_x$', '0.05'))
            elif (Reso_proc=='0d02'):
                Out.write(l.replace('$Delta_x$', '0.02'))
            else:
                print ('No valid resolution ('+Reso_proc+')')
                sys.exit(1)

        elif ('x_min = ' in l):
            if (Reso_proc=='0d25'):
                Out.write(l.replace('$x_min$', '115.03'))
            elif (Reso_proc=='0d05'):
                Out.write(l.replace('$x_min$', '137.53'))
            elif (Reso_proc=='0d02'):
                Out.write(l.replace('$x_min$', '137.13'))
            else:
                print 'No valid resolution ('+Reso_proc+')'
                sys.exit(1)
                
        elif ('Nx = ' in l):
            if (Reso_proc=='0d25'):
                Out.write(l.replace('$Nx$', '200'))
            elif (Reso_proc=='0d05'):
                Out.write(l.replace('$Nx$', '120'))
            elif (Reso_proc=='0d02'):
                Out.write(l.replace('$Nx$', '328'))
            else:
                print 'No valid resolution ('+Reso_proc+')'
                sys.exit(1)
                
        elif ('Delta_y = ' in l):
            if (Reso_proc=='0d25'):
                Out.write(l.replace('$Delta_y$', '0.25'))
            elif (Reso_proc=='0d05'):
                Out.write(l.replace('$Delta_y$', '0.05'))
            elif (Reso_proc=='0d02'):
                Out.write(l.replace('$Delta_y$', '0.02'))
            else:
                print 'No valid resolution ('+Reso_proc+')'
                sys.exit(1)
                
        elif ('y_min = ' in l):
            if (Reso_proc=='0d25'):
                Out.write(l.replace('$y_min$', '25.02'))
            elif (Reso_proc=='0d05'):
                Out.write(l.replace('$y_min$', '34.72'))
            elif (Reso_proc=='0d02'):
                Out.write(l.replace('$y_min$', '33.72'))
            else:
                print 'No valid resolution ('+Reso_proc+')'
                sys.exit(1)

        elif ('Ny = ' in l):
            if (Reso_proc=='0d25'):
                Out.write(l.replace('$Ny$', '140'))
            elif (Reso_proc=='0d05'):
                Out.write(l.replace('$Ny$', '120'))
            elif (Reso_proc=='0d02'):
                Out.write(l.replace('$Ny$', '350'))
            else:
                print 'No valid resolution ('+Reso_proc+')'
                sys.exit(1)

        # config and path
        elif ('config_dir:' in l):
            Out.write(l.replace('config_dir:',
                                'config_dir: '
                                + work_dir
                                + relative_path))
        elif ('Data_description:' in l):
            Out.write(l.replace('Data_description:',
                                'Data_description: '
                                +'<config_dir>/'
                                +'data.cfg'))
        elif ('Configuration_file:' in l):
            Out.write(l.replace('Configuration_file:',
                                'Configuration_file: '
                                +'<config_dir>/'
                                +'saver.cfg'))
            
         # Species.dat
        elif ('Species:' in l):
            Out.write(l.replace('Species:',
                                'Species: <config_dir>/species.dat'))
        # BCS
        elif ('Scavenging_model_aer:' in l):
            Out.write(l.replace('Scavenging_model_aer:',
                                'Scavenging_model_aer: '
                                + BCS_proc ))
        # ICS
        elif ('Scavenging_model_incloud_aer:' in l):
            Out.write(l.replace('Scavenging_model_incloud_aer:',
                                'Scavenging_model_incloud_aer: '
                                + ICS_proc ))
        # Dry deposition
        elif ('Compute_deposition_aerosol:' in l):
            if DryDep_proc == 'Zhang':
                Out.write(l.replace('Compute_deposition_aerosol:',
                                    'Compute_deposition_aerosol: '
                                    + 'yes'))
            elif DryDep_proc == 'constant':
                Out.write(l.replace('Compute_deposition_aerosol:',
                                    'Compute_deposition_aerosol: '
                                    + 'no'))
        else:
            Out.write(l)

    Out.close()
    print FileName
    return

def write_config_data(config_dir, work_dir, relative_path, Met_proc, Source_proc, PSD_Source_proc, suffix_proc, Reso_proc, Kz_proc, Rain_proc, DryDep_proc):
    In = open(config_dir+'data.cfg','r')
    line = In.readlines()
    In.close()
    FileName = work_dir+relative_path+'/data.cfg'
    Out = open(FileName, 'w')
    
    for l in line:
        # meteo
        if ('Meteo_Data_path:' in l):
            if (Met_proc == 'WRF'):
                Out.write(l.replace('Meteo_Data_path:',
                                    'Meteo_Data_path: '
                                    +work_dir
                                    +'heavy_data/'
                                    +Reso_proc
                                    +'/meteo'))
            elif (Met_proc == 'ECMWF'):
                Out.write(l.replace('Meteo_Data_path:',
                                    'Meteo_Data_path: '
                                    +work_dir
                                    +'heavy_data/'
                                    +'coarse/meteo' ))

            else:
                print 'No valid meteo ('+Met_proc+')'
                sys.exit(1)
        elif ('Delta_t_meteo' in l):
            if (Met_proc == 'ECMWF'):
                Out.write(l.replace('Delta_t_meteo =',
                                    'Delta_t = 10800.'))
            elif (Met_proc == 'WRF'):
                Out.write(l.replace('Delta_t_meteo =',
                                    'Delta_t = 3600.'))
                                                                        
        # emissions
        elif os.path.isfile(work_dir+'heavy_data/source_shift/'+Source_proc+'_'+PSD_Source_proc+'_'+suffix_proc+'.dat') == False:
            print 'Source is not valid ('+Source_proc+'_'+PSD_Source_proc+'_'+suffix_proc+')'
            sys.exit(1)

        elif ('Emissions_Data_path:' in l):
            Out.write(l.replace('Emissions_Data_path:',
                                'Emissions_Data_path: '
                                +work_dir
                                +'heavy_data/source_shift' ))
            
        elif ('file: $point_source_aer$' in l):
            Out.write(l.replace('$point_source_aer$',
                                '<Emissions_Data_path>/'
                                +Source_proc+'_'+PSD_Source_proc+'_'+suffix_proc
                                +'.dat'))
                                                                                    
        # deposition
        elif ('Dep_Data_path:' in l):
            Out.write(l.replace('Dep_Data_path:',
                                'Dep_Data_path: '
                                +work_dir
                                +'heavy_data/'
                                +Reso_proc
                                +'/dep' ))
        elif ('Delta_t_dep' in l): 
            if (Met_proc == 'ECMWF'):
                Out.write(l.replace('Delta_t_dep =',
                                    'Delta_t = 10800.'))
            elif (Met_proc == 'WRF'):
                Out.write(l.replace('Delta_t_dep =',
                                    'Delta_t = 3600.'))
        elif ('Delta_t_meteo' in l):
            if (Met_proc == 'ECMWF'):
                Out.write(l.replace('Delta_t_meteo =',
                                    'Delta_t = 10800.'))
            elif (Met_proc == 'WRF'):
                Out.write(l.replace('Delta_t_meteo =',
                                    'Delta_t = 3600.'))
        elif (('#Filename_dep:' in l) and (DryDep_proc == 'constant')):
            Out.write(l.replace('#Filename_dep: 0.002',
                                'Filename: 0.002'))
        # Kz
        elif ('VerticalDiffusion:' in l):
            Out.write(l.replace('VerticalDiffusion: $Kz$',
                                'VerticalDiffusion: '
                                +'<Meteo_Data_path>/Kz_'
                                +Kz_proc
                                +'.bin' ))
            
        # Rain
        elif ('Rain: $Rain$' in l):
            if Rain_proc == 'Regular':
                Out.write(l.replace('Rain: $Rain$',
                                    'Rain: <Meteo_Data_path>/Rain.bin' ))
            elif Rain_proc == 'Factor_2d5':
                Out.write(l.replace('Rain: $Rain$',
                                    'Rain: <Meteo_Data_path>/Rain_factor2-5.bin' ))
            elif Rain_proc == 'Radar':
                Out.write(l.replace('Rain: $Rain$',
                                    'Rain: <Meteo_Data_path>/Rain_radar.bin' ))
            else:
                print 'No valid rain ('+Rain_proc+')'
                sys.exit(1)
                
        else:
            Out.write(l)

    Out.close()
    print FileName
    return 0

def write_config_saver(config_dir, work_dir, relative_path, Reso_proc):
    In = open(config_dir+'saver.cfg','r')
    line = In.readlines()
    In.close()
    FileName = work_dir+relative_path+'/saver.cfg'
    Out = open(FileName, 'w')
    for l in line :
        if ('Data_path:' in l):
            Out.write(l.replace('Data_path:',
                                'Data_path: '
                                +work_dir
                                +relative_path ))
        elif ('x_min = $x_min$' in l):
            if (Reso_proc == '0d25'):
                Out.write(l.replace('x_min = $x_min$ Delta_x = $Delta_x$ Nx = $Nx$',
                                    'x_min = 131.03 Delta_x = 0.05 Nx = 270'))
            elif (Reso_proc == '0d05'):
                l = l.replace('x_min = $x_min$',
                              'x_min = 137.13')
                l = l.replace('Delta_x = $Delta_x$',
                              'Delta_x = 0.02')
                Out.write(l.replace('Nx = $Nx$',
                                    'Nx = 328'))
            elif (Reso_proc == '0d02'):
                Out.write(l.replace('x_min = $x_min$',
                                    'x_min = 138.13'))
                Out.write(l.replace('Delta_x = $Delta_x$',
                                    'Delta_x = 0.01'))
                Out.write(l.replace('Nx = $Nx$',
                                    'Nx = 20'))
            elif ('y_min = $y_min$' in l):
                if (Reso_proc == '0d25'):
                    Out.write(l.replace('y_min = $y_min$ Delta_y = $Delta_y$ Ny = $Ny$',
                                        'y_min = 30.72 Delta_y = 0.05 Ny = 260'))
                elif (Reso_proc == '0d05'):
                    Out.write(l.replace('y_min = $y_min$',
                                        'y_min = 33.72'))
                    Out.write(l.replace('Delta_y = $Delta_y$',
                                        'Delta_y = 0.02'))
                    Out.write(l.replace('Ny = $Ny$',
                                        'Ny = 350'))
                elif (Reso_proc == '0d02'):
                    Out.write(l.replace('y_min = $y_min$',
                                        'y_min = 34.72'))
                    Out.write(l.replace('Delta_y = $Delta_y$',
                                        'Delta_y = 0.01'))
                    Out.write(l.replace('Ny = $Ny$',
                                        'Ny = 20'))
        else :
            Out.write(l)
    Out.close()
    print FileName
    return 0

def write_config_species(config_dir, work_dir, relative_path, BCS_proc, BCSunder_proc, ICS_proc, ICSunder_proc):
    In = open(config_dir+'species.dat','r')
    line = In.readlines()
    In.close()
    FileName = work_dir+relative_path+'/species.dat'
    Out = open(FileName, 'w')
    for l in line :
        # BCS
        if (('$'+BCS_proc+'$') in l):
            if (BCSunder_proc == 'IRSN'):
                Out.write(l.replace('$'+BCS_proc+'$',
                                    'User_defined      5.e-5     1.0'))
            elif (BCSunder_proc == 'BCS_zero'):
                Out.write(l.replace('$'+BCS_proc+'$',
                                    'User_defined      0.0     1.0'))
            elif (BCSunder_proc == 'Null'):
                Out.write(l.replace('$'+BCS_proc+'$',
                                    'User_defined      0.0     1.0'))
            elif (BCSunder_proc == 'BCS_one'):
                Out.write(l.replace('$'+BCS_proc+'$',
                                    'User_defined      1.0     1.0'))
            else:
                Out.write(l.replace('$'+BCS_proc+'$',
                                    BCSunder_proc))
        # ICS
        elif (('$'+ICS_proc+'$') in l):
            if (ICSunder_proc == 'IRSN'):
                Out.write(l.replace('$'+ICS_proc+'$',
                                    'User_defined      5.e-5     1.0'))
            elif (ICSunder_proc == 'ICS_zero'):
                Out.write(l.replace('$'+ICS_proc+'$',
                                    'User_defined      0.0     1.0'))
            elif (ICSunder_proc == 'Null'):
                Out.write(l.replace('$'+ICS_proc+'$',
                                    'User_defined      0.0     1.0'))
            elif (ICSunder_proc == 'ICS_one'):
                Out.write(l.replace('$'+ICS_proc+'$',
                                    'User_defined      1.0     1.0'))
            else:
                Out.write(l.replace('$'+ICS_proc+'$',
                                    ICSunder_proc))
        else :
            Out.write(l)
    Out.close()
    print FileName
    return 0

def write_config_land(config_dir, work_dir, relative_path, Reso_proc):
    In = open(config_dir+'land.dat','r')
    line = In.readlines()
    In.close()
    FileName = work_dir+relative_path+'/land.dat'
    Out = open(FileName, 'w')
    for l in line :
        if (('$RESOLUTION$') in l):
            Out.write(l.replace('$RESOLUTION$',
                                Reso_proc))
        else:
            Out.write(l)
    Out.close()
    print FileName                                    

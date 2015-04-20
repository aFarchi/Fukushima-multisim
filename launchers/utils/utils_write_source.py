from math import *
#from pylab import *
from numpy import *
from datetime import *

def shift_of_str(s):
	l = s.split('p')
	ipart = l[0]
	if (ipart[0] == 'm'):
		ipart = float(ipart[1:])
		factor = -1.
	else:
		ipart = float(ipart)
		factor = 1.
	fpart = l[1]
	n = len(fpart)
	fpart = float(fpart)*(10**(-n))
	return (ipart+fpart)*factor
	
def fn_of_shifts(dx,dy,dz,dt):
	s = 'shift_'
	s += dx + '_'
	s += dy + '_'
	s += dz + '_'
	s += dt
	return s

def f_log10_norm(n, log10sig, r, R):
	return n/(log10sig*sqrt(2.*pi))*exp(-(log10(r/R))**2.0 /2.0 /(log10sig)**2.0)

def write_source_term(SourceFile, work_dir, PSD_proc, dx_proc, dy_proc, dz_proc, dt_proc, DX_Unit=1., DY_Unit=1., DZ_Unit=1., DT_Unit=1.):	
	OutPath = work_dir + 'heavy_data/source_shift/'

	suffix_proc = fn_of_shifts(dx_proc,dy_proc,dz_proc,dt_proc)
	dx = shift_of_str(dx_proc)*DX_Unit
	dy = shift_of_str(dy_proc)*DY_Unit
	dz = shift_of_str(dz_proc)*DZ_Unit
	dt = shift_of_str(dt_proc)*DT_Unit

	# Definition of dap ranges studied
	# Continous range
	dap = logspace(-3,1,1000)
	# Polair range (bounds)
	dap_pol = [0.01,  0.0398,  0.1585,  0.6310, 2.5119,  10.]

	# Definition of the name of the PSD possiblity used
	PSD = {'Baklanov_Sorensen': {'': zeros(len(dap_pol)-1)},
	       'Jaenicke': {'Polar': zeros(len(dap_pol)-1),
			    'Background': zeros(len(dap_pol)-1),
			    'Maritime': zeros(len(dap_pol)-1),
			    'Remote_continental': zeros(len(dap_pol)-1),
			    'Desert_dust_storm': zeros(len(dap_pol)-1),
			    'Rural': zeros(len(dap_pol)-1),
			    'Urban': zeros(len(dap_pol)-1)}}

        ##############################################################
	# Baklanov & Sorensen distribution
	AMAD = 0.68 #um
	sigg = 1.15
	prob137 = []
	for i in range(len(dap)):
		prob137.append(exp(-0.5*(log(dap[i]/AMAD)/sigg)**2.)
			       /(dap[i]*sigg*sqrt(2.*pi)) )

	interv = ([10**(-1.4)-1e-3,
		   10**(-0.8)-10**(-1.4),
		   10**(-0.2)-10**(-0.8),
		   10**(0.4)-10**(-0.2),
		   10**(1.)-10**(0.4)])

	pro137 = zeros(len(dap_pol)-1)
	wg137 = zeros(len(dap_pol)-1)

	for i in range(5):
		pro137[i] = (exp(-0.5*((log(dap_pol[i]/AMAD)/sigg)**2))
			     /(dap_pol[i]*sigg*sqrt(2*pi)) )
		wg137[i] = interv[i]*pro137[i]

	# Weight computing
	sumprob = sum(wg137)
	for j in range(len(dap_pol)-1):
		PSD['Baklanov_Sorensen'][''][j] = wg137[j]/sumprob



	# Nombre de particules par classe de taille
	N = zeros(len(dap)-1)
	N_pol = zeros(len(dap_pol)-1)


	# Table des constantes
	# ni cm-3
	ni = {'Polar': [2.17e+1, 1.86e-1, 3.04e-4],
	      'Background': [1.29e+2, 5.97e+1, 6.35e+1],
	      'Maritime': [1.33e+2, 6.66e+1, 3.06e+0],
	      'Remote_continental': [3.20e+3, 2.90e+3, 3.00e-1],
	      'Desert_dust_storm': [7.26e+2, 1.14e+3, 1.78e-1],
	      'Rural': [6.65e+3, 1.47e+2, 1.99e+3],
	      'Urban': [9.93e+4, 1.11e+3, 3.64e+4]}

	# Ri mum
	Ri = {'Polar': [0.0689, 0.375, 4.290],
	      'Background': [0.0036, 0.127, 0.259],
	      'Maritime': [0.0039, 0.133, 0.290],
	      'Remote_continental': [0.0100, 0.058, 0.900],
	      'Desert_dust_storm': [0.0010, 0.019, 10.80],
	      'Rural': [0.0074, 0.027, 0.042],
	      'Urban': [0.0065, 0.00714, 0.0248]}

	# log10 sigi
	log10sigi = {'Polar': [0.245, 0.300, 0.294],
		     'Background': [0.645, 0.253, 0.425],
		     'Maritime': [0.657, 0.210, 0.396],
		     'Remote_continental': [0.161, 0.217, 0.380],
		     'Desert_dust_storm': [0.247, 0.770, 0.438],
		     'Rural': [0.225, 0.557, 0.266],
		     'Urban': [0.245, 0.666, 0.337]}

	# Calcul du nombre de particules par classe
	for name in ni.keys():
		N=zeros([len(dap)-1])
		N_pol=zeros([len(dap_pol)-1])
		for j in range(len(dap)-1):
			for i in range(3):
				dlog10r = log10(dap[j+1]/2.0)-log10(dap[j]/2.0)
				N[j] += (f_log10_norm(ni[name][i],
						      log10sigi[name][i],
						      dap[j]/2.0,
						      Ri[name][i])
					 *dlog10r)
		# Compute for the Polair3d bin
		for j in range(len(dap_pol)-1):
			for i in range(3):
				dlog10r = log10(dap_pol[j+1]/2.0)-log10(dap_pol[j]/2.0)
				N_pol[j] += (f_log10_norm(ni[name][i],
							  log10sigi[name][i],
							  dap_pol[j]/2.0,
							  Ri[name][i])
					     *dlog10r)
		# Width computing
		barwidth = zeros(len(dap_pol)-1)
		for i in range(len(dap_pol)-1):
			barwidth[i] = dap_pol[i+1]-dap_pol[i]

		# Weight calculus
		# Volumique distribution
		V_pol = N_pol*(dap_pol[0:5]+barwidth/2.0)**3.0
		sumV = sum(V_pol)
		Weight = V_pol/sumV
		PSD['Jaenicke'][name] = V_pol/sumV

        #############################################################################
	# Write the source from Victor Winiarek, from a bin file

	source = fromfile(SourceFile, dtype=float64, count=-1)
	Type = 'Winiarek_d22'
	nb_bin = 5

	# Loop on the differents PSD
	for author in PSD.keys():
		for name in PSD[author].keys():
			fileName  = OutPath + Type + '_' + author + '_' + name + '_AP_' + suffix_proc + '.dat'
			sourceout = open(fileName,'w')
			# read & write the source file				
			datestart = datetime(2011, 03, 11, 0)

			for time in range(len(source)):
				present_date = datestart + timedelta(hours=time) + timedelta(hours=dt)
				str_dat_bgn = (str(present_date.year) + '-'
					       + str('%02d' %present_date.month) + '-'
					       + str('%02d' %present_date.day) + '_'
					       + str('%02d' %present_date.hour) + 'h00')
				str_dat_end = (str(present_date.year) + '-'
					       + str('%02d' %present_date.month) + '-'
					       + str('%02d' %present_date.day) + '_'
					       + str('%02d' %present_date.hour) + 'h59')
				for i in range(nb_bin):
					sourceout.write('[source]\n\n')
					sourceout.write('Abscissa: '+str(141.03+dx)+'\n')
					sourceout.write('Ordinate: '+str(37.42+dy)+'\n')
					sourceout.write('Altitude: '+str(20.+dz)+'\n\n')
					sourceout.write('Species: Cs137_%i\n\n' %i)
					sourceout.write('Type: continuous\n')
					sourceout.write('Rate: %f\n' %(source[time]*PSD[author][name][i]))
					sourceout.write('Date_beg: '+str_dat_bgn+'\n')
					sourceout.write('Date_end: '+str_dat_end+'\n')
					sourceout.write('Velocity: 0.0\n')
					sourceout.write('Temperature = 0.\n')
					sourceout.write('Diameter = 100.\n\n')
					
			sourceout.close()
			print fileName
	return 0


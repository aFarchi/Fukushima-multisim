#####################
# mergeOTGSResults.py
#####################

import cPickle as pck
import numpy as np

from ..utils.io.saveSymMatrix import saveSymMatrixEig

def mergeOTGSResults(nbrProc, directory, algoName, printIO=False):
    results = np.zeros(shape = (nbrProc,nbrProc))
    for p1 in xrange(nbrProc):
        for p2 in xrange(p1):
            res = directory + str(p1) + '-' + str(p2) + '/output_'+algoName+'/result.bin'
            f = open(res, 'rb')
            p = pck.Unpickler(f)
            results[p1,p2] = p.load()
            results[p2,p1] = results[p1,p2]
            f.close()
    saveSymMatrixEig(directory+'/result_'+algoName, results)
    if printIO:
        print('Results merged in '+directory+' ...')

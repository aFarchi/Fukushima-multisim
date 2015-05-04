import pickle
import numpy as np

nbrProc = $nbrProc$
rep = $rep$

results = np.zeros(shape = (nbrProc,nbrProc))
for i1 in xrange(nbrProc):
    for i2 in xrange(i1):
        fn = rep + '/fields/' + str(i1) + '-' + str(i2) + '/result.bin'
        f = open(fn, 'rb')
        p = pickle.Unpickler(f)
        results[i1,i2] = p.dump()
        results[i2,i1] = results[i1,i2]
        f.close()

np.save(results, rep+'result.npy')

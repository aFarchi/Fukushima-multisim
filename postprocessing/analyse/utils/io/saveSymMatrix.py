##################
# saveSymMatrix.py
##################

import numpy as np

def saveSymMatrixEig(prefixFileName, matrix):
    n = matrix.shape[0]

    (eigVals,eigVects) = eigh(matrix)

    indexes            = np.argsort(abs(eigVals))
    i                  = np.arange(n)

    sortedEigVals      = eigVals[indexes[n-1-i]]
    sortedEigVects     = eigVects[:, indexes[n-1-i]]

    np.save(prefixFileName+'.npy', matrix)
    np.save(prefixFileName+'_eigVals.npy', sortedEigVals)
    np.save(prefixFileName+'_eigVects.npy', sortedEigVects)
                                    

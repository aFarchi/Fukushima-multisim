###################
# defaultTSelect.py
###################

def selectLastT(Nt):
    return Nt-1

def selectFirstT(Nt):
    return 0

def makeSelectXtimesNt(x):
    def selectXtimes(Nt):
        return min(int(Nt * x), Nt-1)
    return selectXtimes

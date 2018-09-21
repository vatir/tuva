"""
Imports that multiple files will be using that need to be imported before the normal imports packages are available.
"""

def AddSysPath(new_path):
    """
    Adds a path to the interpreter environment.
    """
    import sys, os
    # standardise
    new_path = os.path.abspath(new_path)

    # MS-Windows does not respect case
    if sys.platform == 'win32':
        new_path = new_path.lower()

    # disallow bad paths
    do = -1
    if os.path.exists(new_path):
        do = 1
        
        # check against all paths currently available
        for x in sys.path:
            x = os.path.abspath(x)
            if sys.platform == 'win32':
                x = x.lower()
            if new_path in (x, x + os.sep):
                do = 0

        # add path if we don't already have it
        if do:
            sys.path.append(new_path)
            pass

def uniquify(seq, idfun=None):
    """
    Looted from http://www.peterbe.com/plog/uniqifiers-benchmark
    
    Order Perserving
    
    Input: seq (to be searched for unique values)
    idfun: Function that can be applied to check for additional lack of uniqueness
        EX: a=list('ABeeE')
            uniqify(a)
            ['A','B','e','E']
            uniqify(a, lambda x: x.lower())
            ['A','B','e'] 
    """
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

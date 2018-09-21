"""
Role:
Initial setup of the DB.

Requirements:
DB Connection information is passed on the command line.

"""

from main import debug_level

from collections import OrderedDict


def import_args():
    """
    Imports the DB information from the command line.
    args.host : Hostname
    args.port : DB Server Port
    args.db   : DB Name
    args.user : DB Username
    args.file : Filename to import for original data
    args.runs : Number of runs to generate (0 for only import the original data)
    
    Defaults are mostly for testing ease.
    """
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-host',type=str, default="localhost")
    parser.add_argument('-port',type=int, default="9489")
    parser.add_argument('-db',type=str, default="MainData")
    parser.add_argument('-user',type=str, default="postgre")
    parser.add_argument('-file',type=str, default='data/ISWI DNA Binding 3 30 2012.dat')
    parser.add_argument('-runs',type=int, default=5000)
    parser.add_argument('-data_type',type=int, default=50)
    parser.add_argument('-schema',type=str, default='public')
    args = parser.parse_args()
    return args

import psycopg2
AsIs = psycopg2.extensions.AsIs

if __name__ == '__main__':

    if debug_level >= 2:
        import time
        start_time = time.time()
        total_time = time.time()

    cl_args=import_args()
    from CoreImports import AddSysPath
    AddSysPath('import')
    AddSysPath('model')
    from data import Import_Data_From_File
    try:
        data = Import_Data_From_File(cl_args.file)
    except:
        from sys import exit
        exit(1)
        
    dbconn = psycopg2.connect(database=cl_args.db, user=cl_args.user, host=cl_args.host, port=cl_args.port)
    dbconn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    dbcur = dbconn.cursor()
    dbcur.execute("SET search_path TO %s;", (AsIs(cl_args.schema),))
    """
    Add Generated Data
    """
    
    variables = OrderedDict()
    
    for key in data.traits().keys():
        try:
            float(data.traits()[key][1])
            variables[key] = "float8"
        except:
            variables[key] = "varchar"

    """
    Generate Random Data:
    
    Note: http://docs.scipy.org/doc/numpy/reference/routines.random.html
    
    numpy.random.normal(loc=0.0, scale=1.0, size=None)
        loc : Mean of the distribution.
        scale : Standard deviation of the distribution.
        size : tuple of ints
            Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples are drawn.
    """
    
    from numpy import random
    from numpy import zeros
    from numpy import ones
    
    num_runs = int(cl_args.runs)
    
    dbcur.execute("SELECT MAX(dataset) from entries;")
    hold_fetch = dbcur.fetchone()[0]
    if hold_fetch == None:
        current_max_dataset = 1
    else:
        current_max_dataset = hold_fetch + 1

    entries_columns = ()
    # Initialize column and value variables for the insert 
   
    # Add Dataset Number
    entries_columns += ("dataset", "type")

    for key in variables.keys():
        entries_columns += (str(key),)
    
    
    """
    Get Uncertainty
    
    Uncertainty values and types are held in the following ordered dictionaries. 
    uncertainty_types
    uncertainty_values
    
    """
    
    uncertainty_types = OrderedDict()
    uncertainty_values = OrderedDict()
    
    dbcur.execute("SELECT data_names, data_uncertainty_type from uncertainty_types;")
    
    for entry in dbcur.fetchall():
        uncertainty_types[entry[0]] = entry[1]
        uncertainty_values[entry[0]] = list()

    for key in uncertainty_values.keys():
        dbcur.execute("SELECT %s from uncertainty_values;", (AsIs(key),))
        for entry in dbcur.fetchall():
                uncertainty_values[key].append(entry[0])

    """
    End Get Uncertainty
    """

    """
    Create and Insert Data
    
    """
    import cStringIO
    
    for x in range(current_max_dataset, num_runs + current_max_dataset):
        
        Current_Run = x
        
        var_random_add = OrderedDict()
        
        for key in uncertainty_types.keys():
            if uncertainty_types[key] == "Normal":
                var_random_add[key] = list()
                for value in uncertainty_values[key]:
                    var_random_add[key].append(random.normal(scale=value))
            elif uncertainty_types[key] == "Uniform":
                var_random_add[key] = list()
                for value in uncertainty_values[key]:
                    var_random_add[key].append(random.uniform(low=(-1.0/2.0)*value, high=(1.0/2.0)*value))
            elif uncertainty_types[key] == "Normal_Once":
                var_random_add[key] = random.normal(scale=uncertainty_values[key][0]) * ones(data.GetNumberRows())
            elif uncertainty_types[key] == "Uniform_Once":
                var_random_add[key] = random.uniform(low=-uncertainty_values[key][0]*1.0/2.0, high=uncertainty_values[key][0]*1.0/2.0) * ones(data.GetNumberRows())
            else:
                var_random_add[key] = zeros(data.GetNumberRows())
                    
        entries_values = ""
        
        for i in range(data.GetNumberRows()):
            # Initialize column and value variables for the insert 
            
            
            # Add Dataset Number
            entries_values += str(Current_Run) + "\t" + str(cl_args.data_type) + "\t"
            
            for key in variables.keys():
                if variables[key] == "varchar":
                    entries_values += str(data.traits()[key][i]) + "\t"
                else:
                    entries_values += str(data.traits()[key][i] + var_random_add[key][i]) + "\t"
                    
            entries_values = entries_values[0:-1] + "\n"
        
        insert_file = cStringIO.StringIO(entries_values)
        dbcur.copy_from(insert_file, 'entries', columns=entries_columns)
        insert_file.close()
        
        if debug_level >= 2:
            print "Data Added:"
            print time.time() - start_time
            start_time = time.time()
    if debug_level >= 2:
        print "Total Time:"
        print time.time() - total_time
    
    """
    Close Connections
    """

    dbcur.close()
    dbconn.close()
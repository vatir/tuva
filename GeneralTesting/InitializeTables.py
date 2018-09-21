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
    parser.add_argument('-file',type=str, default='data\ISWI NCP Binding Double Label All 4 6 2012.dat')
    parser.add_argument('-schema',type=str, default='eclipse')
    args = parser.parse_args()
    return args

import psycopg2
AsIs = psycopg2.extensions.AsIs
def create_table(dbcur, table_name_str, columns):
    
    table_name = (AsIs(table_name_str),)
    columns = (AsIs(columns),)
    params =()
    params += table_name
    params += columns 
    table_creation = "CREATE TABLE %s (%s);"
    
    try:
        dbcur.execute(table_creation, params)
        
    except psycopg2.ProgrammingError:
        if debug_level >= 1:
            print "Error encountered: Table (" + table_name_str + ") Already Exists!"
        dbcur.execute("DROP TABLE %s;", table_name)
        dbcur.execute(table_creation, params)
    
    return True
    

if __name__ == '__main__':
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
    try:
        dbcur.execute("SET search_path TO %s;", (AsIs(cl_args.schema.upper()),))
    except psycopg2.DataError:
        if debug_level >= 1:
            print "Error encountered: Schema (" + str(cl_args.schema.upper()) + ") Does Not Exist!"
        dbcur.execute("CREATE SCHEMA %s;",(AsIs(cl_args.schema.upper()),))
        dbcur.execute("SET search_path TO %s;", (AsIs(cl_args.schema.upper()),))
        
    """
    Setup Columns:
    """
    
    variables = OrderedDict()
    
    for key in data.traits().keys():
        try:
            float(data.traits()[key][1])
            variables[key] = "float8"
        except:
            variables[key] = "varchar"
    
    if debug_level >= 2:
        import time
        start_time = time.time()
        total_time = time.time()
    
    
    """
    Main Table:
    id, dataset, type, analyzed, data_col_1, data_col_2, ..., data_col_n
    
    id:         Primary Key
    dataset:    A number that groups the dataset together
    type:   1 - Original Data
            2 - Generated Data
    
    data_cols
    
    REMOVED:
    analyzed:   (Defaults to False)
            True - Dataset has been analyzed
            False - Dataset has not been analyzed

    """
    
    table_name = "entries"
    columns_plus_type = "id serial PRIMARY KEY, dataset integer NOT NULL, type integer NOT NULL DEFAULT 2"
    for key in variables.keys():
        columns_plus_type += ","
        columns_plus_type += '"' + key.lower() + '"' + " " + variables[key] + " NOT NULL"
        
    create_table(dbcur, table_name, columns_plus_type)
    
    
    """
    Create and populate table for Data Titles
    """
    
    create_table(dbcur, "data_column_names", "id serial PRIMARY KEY, data_names varchar NOT NULL")
    
    """
    Create and populate table for Data Uncertainty Types
    """
    
    create_table(dbcur, "uncertainty_types", "id serial PRIMARY KEY, data_names varchar NOT NULL, data_uncertainty_type varchar NOT NULL")
    
    for key in data.uncertainty_types().keys():
        dbcur.execute("INSERT INTO uncertainty_types (data_names, data_uncertainty_type) VALUES (%s, %s);",(str(key), str(data.uncertainty_types()[key]), ))
        
    """
    Create table for Data Uncertainty Values
    """
    
    table_name = "uncertainty_values"
    columns_plus_type = "id serial PRIMARY KEY"
    for key in data.uncertainty_types().keys():
        columns_plus_type += ","
        columns_plus_type += '"' + key.lower() + '"' + " float8 NOT NULL"
        
    create_table(dbcur, table_name, columns_plus_type)
    
    """
    Create and Data Results Table
    dataset : Dataset that was analyzed
    analysis_type:
        1 - Assumes default analysis was performed
    """
    
    from CoreImports import uniquify
    uniquify(data.traits()["Run_Name"])
    group_names = uniquify(data.traits()["Run_Name"])
    from main import model_name
    model = __import__(model_name)
    
    results_columns = "id serial PRIMARY KEY, dataset integer, analysis_type integer DEFAULT 1, ssr float8, "
    x = 0
    for key in model.param.keys():
        if model.use_individual_params[key]:
            for i in range(len(group_names)):
                results_columns += "\"" + str(key) + "_" + str(group_names[x]) + "\" float8," 
                x += 1
        else:
            results_columns += "\"" + str(key) + "_global\" float8, "
            x += 1
    results_columns = results_columns[0:-2]
    
    table_name = "results"
    
    create_table(dbcur, table_name, results_columns)
    
    if debug_level >= 2:
        print "Tables Added:"
        print time.time() - start_time
        start_time = time.time()
    
    """
    Add original data
    """
    
    for key in variables:
        dbcur.execute("INSERT INTO data_column_names (data_names) VALUES (%s);",(str(key), ))

    
    """
    Insert Uncertainty Values
    """
    import cStringIO
    
    uncertainty_values = data.uncertainty_values()
    
    table_name = "uncertainty_values"
    entries_columns = ()
    # Initialize column and value variables for the insert 

    for key in uncertainty_values.keys():
        entries_columns += (str(key),)

    entries_values = ""
    for i in range(data.GetNumberRows()):
        # Initialize column and value variables for the insert 
        
        for key in uncertainty_values.keys():
            entries_values += str(uncertainty_values[key][i]) + "\t"
                
        entries_values = entries_values[0:-1] + "\n"
    
    insert_file = cStringIO.StringIO(entries_values)
    dbcur.copy_from(insert_file, table_name, columns=entries_columns)
    insert_file.close()

    """
    Insert Original Data
    """
    
    Current_Run = 1
    
    entries_columns = ()
    # Initialize column and value variables for the insert
    
    # Add Dataset Number
    entries_columns += ("dataset",)

    # Add type code (Only needed for Original Data)
    entries_columns += ("type",)

    for key in variables.keys():
        entries_columns += (str(key),)

    entries_values = ""
    for i in range(data.GetNumberRows()):
        # Initialize column and value variables for the insert 
        
        
        # Add Dataset Number
        entries_values += str(Current_Run) + "\t"
    
        # Add type code (Only needed for Original Data)
        entries_values += "1" + "\t"

        for key in variables.keys():
            entries_values += str(data.traits()[key][i]) + "\t"
                
        entries_values = entries_values[0:-1] + "\n"
    
    insert_file = cStringIO.StringIO(entries_values)
    dbcur.copy_from(insert_file, 'entries', columns=entries_columns)
    insert_file.close()
    
    """
    End Original Data Adding
    """
    
    if debug_level >= 2:
        print "Orig Data Added:"
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
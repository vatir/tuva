"""
Role:
Initial setup of the DB.

Requirements:
DB Connection information is passed on the command line.

"""

# Used for memory profiling
#from meliae import scanner

from main import debug_level
import gc
from collections import OrderedDict
from numpy import array
from numpy import ones

def import_args():
    """
    Imports the DB information from the command line.
    args.host       : Hostname
    args.port       : DB Server Port
    args.db         : DB Name
    args.user       : DB Username
    args.start_num  : Dataset Number to start with
    args.end_num    : Last dataset to process. (If this equals 0 then only run one.)
    
    Defaults are mostly for testing ease.
    """
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-host',type=str, default="localhost")
    parser.add_argument('-port',type=int, default="9489")
    parser.add_argument('-db',type=str, default="MainData")
    parser.add_argument('-user',type=str, default="postgre")
    parser.add_argument('-start_num',type=int, default=2)
    parser.add_argument('-end_num',type=int, default=2)
    parser.add_argument('-analysis_type',type=str, default=4)
    parser.add_argument('-schema',type=str, default='eclipse')
    args = parser.parse_args()
    return args

from functools import partial
from openopt import NLP

def fit(fitfunc, model, data_single, y, starting_values, param_upper_bounds, param_lower_bounds):
    print_level = -1
    if model.main_constrained:
        fitting = NLP(
                        partial (fitfunc,
                                 data = data_single,
                                 ind = y,
                                 return_residuals=False,
                                 return_SSR=True
                                 ),
                        starting_values,
                        ub=param_upper_bounds,
                        lb=param_lower_bounds,
                        ftol=model.tolerence
                        )
        #results = fitting.solve('nlp:ralg', iprint=print_level)
        #return fitting.solve('nssolve', iprint = print_level)
        return fitting.solve('ralg', iprint = print_level, maxIter = model.max_runs)
    else:
        fitting = NLP(
                        partial (fitfunc,
                                 data=data_single,
                                 ind = y,
                                 return_residuals=False,
                                 return_SSR=True
                                 ),
                        starting_values,
                        ftol=model.tolerence,
                        maxIter = model.max_runs,
                        )
        return fitting.solve('scipy_leastsq', iprint=print_level)

from CoreImports import uniquify
import psycopg2
AsIs = psycopg2.extensions.AsIs

if __name__ == '__main__':
    
    cl_args = import_args()
    
    from CoreImports import AddSysPath
    AddSysPath('import')
    AddSysPath('model')
    """
    Next statement is an alternate method of importing a module, but allows for using a variable to choose the module.
    """
    from main import model_name
    model = __import__(model_name)
    
    """
    Determine the Number of Runs
    """
    
    if cl_args.end_num <= cl_args.start_num:
        cl_args.end_num = cl_args.start_num
        
        
    if debug_level >= 2:
        import time
        total_time = time.time()
    
    
    for dataset_number in range(cl_args.start_num, cl_args.end_num+1):
        try:
            dbconn = psycopg2.connect(database=cl_args.db, user=cl_args.user, host=cl_args.host, port=cl_args.port)
            dbconn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            dbcur = dbconn.cursor()
            
            dbcur.execute("SET search_path TO %s;", (AsIs(cl_args.schema.upper()),))
            """
            Get the Data
            """
            if debug_level >= 2:
                start_time = time.time()
            
            
            data_grouped = OrderedDict() # Main Working Data Container (Grouped by run)
            data_single = OrderedDict() # Main Working Data Container (Ungrouped)
            
            
            dbcur.execute("SELECT data_names from data_column_names;")
            
            i = 0
            columns = ""
            
            for record in dbcur.fetchall():
                data_single[record[0]] = []
                columns += str(record[0].lower()) + ","
                if record[0] == "Run_Name":
                    run_name_col = i
                i += 1
            columns = columns[:-1]
        
            if debug_level >= 2:
                print "Get Data:"
                print time.time() - start_time
                start_time = time.time()
            
            dbcur.execute("SELECT %(col)s FROM entries WHERE dataset = %(dataset)s;", {'col':AsIs(columns), 'dataset':dataset_number})
    
            for record in dbcur.fetchall():
                for x in range(len(record)):
                    data_single[data_single.keys()[x]].append(record[x])
                                
            
            group_names = uniquify(data_single["Run_Name"])
            for name in group_names:
                data_grouped[name] = OrderedDict()
                for key in data_single.keys():
                    data_grouped[name][key] = []
            
            for i in range(len(data_single["Run_Name"])):
                for key in data_single.keys():
                    data_grouped[data_single["Run_Name"][i]][key].append(data_single[key][i])
        
            if debug_level >= 2:
                print "Parse Data:"
                print time.time() - start_time
                start_time = time.time()
            
            for key in data_single.keys():
                data_single[key] = array(data_single[key]) 
        
            for run in data_grouped.keys():
                for key in data_grouped[run].keys():
                    data_grouped[run][key] = array(data_grouped[run][key])
                
                data_single[key] = array(data_single[key]) 
            
            """
            Begin Data Analysis
            """
            
            y = data_single[model.output_param]
            
            starting_values = []
            for key in model.param.keys():
                if model.use_individual_params[key]:
                    for i in range(len(group_names)):
                        starting_values.append(model.param[key])
                else:
                    starting_values.append(model.param[key])
            
            param_upper_bounds = []
            for key in model.param_upper_bounds.keys():
                if model.use_individual_params[key]:
                    for i in range(len(group_names)):
                        param_upper_bounds.append(model.param_upper_bounds[key])
                else:
                    param_upper_bounds.append(model.param_upper_bounds[key])
                    
            param_lower_bounds = []
            for key in model.param_lower_bounds.keys():
                if model.use_individual_params[key]:
                    for i in range(len(group_names)):
                        param_lower_bounds.append(model.param_lower_bounds[key])
                else:
                    param_lower_bounds.append(model.param_lower_bounds[key])
            
            def fitfunc(fit_params, data, ind, return_residuals=False, return_SSR=True):
                i = 0
                for key in model.param.keys():
                    if model.use_individual_params[key]:
                        data[key] = []
                        for name in group_names:
                            data[key].append(fit_params[i]*ones(len(data_grouped[name]["Run_Name"])))
                            i += 1
                        data[key] = array(data[key]).ravel()
                    else:
                        data[key] = fit_params[i]*ones(len(ind))
                        data[key] = array(data[key])
                        i += 1
                if return_residuals:
                    return (model.func(data) - ind)
                elif return_SSR:
                    results = model.func(data)
                    return sum(map(lambda x: x**2, results - ind))
                else:
                    return model.func(data)
                
            if debug_level == 0:
                print_level = -1
            elif debug_level >= 1:
                print_level = -10
            
            
            results = fit(fitfunc, model, data_single, y, starting_values, param_upper_bounds, param_lower_bounds)
            y_fit = fitfunc(results.xf, data_single, y, return_residuals=False)
            SSR = sum(map(lambda x: x**2, y-y_fit))/len(y)
            
            """
            x = 0
            for key in model.param.keys():
                if model.use_individual_params[key]:
                    for i in range(len(group_names)):
                        print str(key) + " : " + str(group_names[x]) + " : " + str(results.xf[x])
                        x += 1
                else:
                    print str(key) + " : Global : " + str(results.xf[x])
                    x += 1
            
            #print '||residuals||^2 = ' + str(results.ff)
            SSR = SSR/len(y)
            print '||residuals||^2/N = ' + str(SSR)
            """
            
            results_columns = "dataset, ssr, analysis_type,"
            x = 0
            for key in model.param.keys():
                if model.use_individual_params[key]:
                    for i in range(len(group_names)):
                        results_columns += "\"" + str(key) + "_" + str(group_names[x]) + "\"," 
                        x += 1
                else:
                    results_columns += "\"" + str(key) + "_global\", "
                    x += 1
            results_columns = results_columns[0:-2]
            
            report_results = str(dataset_number) + ", " + str(SSR) + ", " + str(cl_args.analysis_type) + ", "
            
            x = 0
            for key in model.param.keys():
                if model.use_individual_params[key]:
                    for i in range(len(group_names)):
                        report_results += str(results.xf[x]) + ", "
                        x += 1
                else:
                    report_results += str(results.xf[x]) + ", "
                    x += 1
            report_results = report_results[0:-2]
            
            """
            if debug_level >= 2:
                print y_fit
                print report_results
                print '||residuals||^2/N = ' + str(SSR)
            """
            
            dbcur.execute("INSERT INTO results (%(columns)s) VALUES (%(values)s);",{"columns":AsIs(results_columns), "values":AsIs(report_results)})
        
            """
            Close Connections
            """
            dbcur.close()
            dbconn.close()
            
            """
            Cleanup
            
            Probably does not work.
            
            """
            del data_grouped
            del data_single
            del results
            del dbcur
            del dbconn
            del y_fit
            del SSR
            del report_results
            gc.collect()
        
        except MemoryError:
            print "Ran out of Memory in loop:" + str(dataset_number)
            """
            Attempt Cleanup due to Memory Error and fork the remainder. 
            
            Probably does not work.
            
            del data_grouped
            del data_single
            del results
            del dbcur
            del dbconn
            del y_fit
            del SSR
            del report_results
            """

        if debug_level >= 2:
            print "Analyze Complete:" + str(dataset_number)
            print time.time() - start_time
            start_time = time.time()
            
    if debug_level >= 2:
        print "DataAnalyzer(Runtime):"
        print time.time() - total_time
        
    # Used for memory profiling
    #scanner.dump_all_objects("memory_dump_big")

import numpy as np
from scipy import stats
from .analyze_data import analyze_data
from .plot_hypothesis import plot_hypothesis
from collections import namedtuple

def test_hypothesis(x, y, key, x_name = None, y_name = None, lam_c = None, 
                    n_cycles = None, repetitions = None, print_ = True,
                    plot = True):
    """Perform a bilateral Student T test using the model's mean."""
    out_data = namedtuple("test_hypothesis", [
        "var_ratio", "std_t_test", "welch_t_test", "x_stats", "y_stats"
        ])
    
    x_stats = analyze_data(x, key, print_ = False, plot = False)
    y_stats = analyze_data(y, key, print_ = False, plot = False)
    
    x_tau = [i["tau"] for i in np.array(x[key])]
    y_tau = [i["tau"] for i in np.array(y[key])]
    
    std_t_test = stats.ttest_ind(x_tau, y_tau, equal_var = True)
    welch_t_test = stats.ttest_ind(x_tau, y_tau, equal_var = False)
    
    if x_name == None: x_name = "X"
    if y_name == None: y_name = "Y"
    
    if print_ == True:
        line = "---------------------------------------------------------"
        
        title_x = ("[Group: {x_name} | Key: {key}]")\
                   .format(x_name = x_name, key = key.title())
        
        summary_x = ("Mean = {x_mean}\nVar. = {x_var}\nSD = {x_std}")\
                     .format(
                         x_mean = x_stats.mean, x_var = x_stats.var,
                         x_std = x_stats.std
                         )
        
        title_y = ("[Group: {y_name} | Key: {key}]")\
                   .format(y_name = y_name, key = key.title())
        
        summary_y = ("Mean = {y_mean}\nVar. = {y_var}\nSD = {y_std}")\
                     .format(
                         y_mean = y_stats.mean, y_var = y_stats.var,
                         y_std = y_stats.std
                         )
        
        title_x_y = ("[Groups: {x_name} & {y_name} | Key: {key}]")\
                     .format(
                         x_name = x_name, y_name = y_name, key = key.title()
                         )
        
        larger_var = np.max([x_stats.var, y_stats.var])
        smaller_var = np.min([x_stats.var, y_stats.var])
        var_ratio = larger_var / smaller_var
        ratio_test = var_ratio < 2
        
        summary_x_y = ("Variance ratio: {larger_var} / {smaller_var} = " +\
                       "{var_ratio}\n" +\
                       "Ratio test: {var_ratio} < 2: {ratio_test}\n\n" +\
                       "Standard t-test statistic = {std_t_test_stat}\n" +\
                       "Standard t-test p-value = {std_t_test_pvalue}\n" +\
                       "Welch’s t-test statistic = {welch_t_test_stat}\n" +\
                       "Welch’s t-test p-value = {welch_t_test_pvalue}")\
                       .format(
                           larger_var = larger_var, smaller_var = smaller_var,
                           var_ratio = var_ratio, 
                           ratio_test = str(ratio_test).upper(),
                           std_t_test_stat = std_t_test.statistic,
                           std_t_test_pvalue = std_t_test.pvalue,
                           welch_t_test_stat = welch_t_test.statistic,
                           welch_t_test_pvalue = welch_t_test.pvalue
                           )
        
        print(
            line, 
            title_x, summary_x, line, 
            title_y, summary_y, line, 
            title_x_y, summary_x_y, line,
            sep = "\n\n"
            )
    
    if ratio_test == True:
        p_value = round(std_t_test.pvalue, 5)
    else:
        p_value = round(welch_t_test.pvalue, 5)
    
    if plot == True:
        plot_hypothesis(
            x, y, key, p_value, x_name, y_name, lam_c, n_cycles,
            repetitions
            )
    
    return out_data(var_ratio, std_t_test, welch_t_test, x_stats, y_stats)

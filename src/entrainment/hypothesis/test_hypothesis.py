import numpy as np
from scipy import stats

def test_hypothesis(key, x = north, y = south, 
                    x_name = "Nascente do rio Ailã (Lat.: $5.272$)", 
                    y_name = "Arroio Chuí (Lat.: $- 33.752$)", 
                    lam_c = 4727.833, n_cycles = 3, repetitions = 100):
    x = [i["tau"] for i in np.array(x[key])]
    y = [i["tau"] for i in np.array(y[key])]
    
    line = "\n---------------------------------------------------------\n"
    print(line)
    
    title = ("\n[Groups: {x_name}/{y_name} | Key: {key}]\n")\
             .format(x_name = x_name, y_name = y_name, key = key.title())
             
    print(title)
    
    mean_x, var_x, std_x = np.mean(x), np.var(x), np.std(x) 
    min_x, max_x = np.min(x), np.max(x)
    
    summary_x = ("Mean = {mean_x}, SD = {std_x}\n")\
                 .format(mean_x = str(mean_x), std_x = str(std_x))
    
    print(summary_x)
    
    mean_y, var_y, std_y = np.mean(y), np.var(y), np.std(y) 
    min_y, may_y = np.min(y), np.max(y)
    
    summary_y = ("Mean = {mean_y}, SD = {std_y}\n")\
                 .format(mean_y = str(mean_y), std_y = str(std_y))
    
    print(summary_y)

    ttest = stats.ttest_ind(x, y)
    ttest_stats = round(ttest.pvalue, 5)
    
    print(stats.ttest_ind(x, y))
    print(line)
    
    plot_hypothesis(
        key, ttest_stats, x, y, x_name, y_name, lam_c, n_cycles,repetitions
        )
    
    return(ttest)

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from .analyze_data import analyze_data
from collections import namedtuple

def test_hypothesis(x, y, key, alternative = "less", x_name = None, 
                    y_name = None, lam_c = None, n_cycles = None, 
                    repetitions = None, print_ = True,
                    plot = True):
    """Compute a bilateral Student's t test for model's means.
    
    This function assumes that ``x`` and ``y`` have equal sizes and that
    all Student's t test assumptions are not violated.
    """
    out_data = namedtuple("test_hypothesis", [
        "var_ratio", "std_t_test", "welch_t_test", "cohens_d", "r_squared",
        "x_stats", "y_stats"
        ])
    
    x_stats = analyze_data(x, key, print_ = False, plot = False)
    y_stats = analyze_data(y, key, print_ = False, plot = False)
    
    x_tau = [i["tau"] for i in np.array(x[key])]
    y_tau = [i["tau"] for i in np.array(y[key])]
    
    std_t_test = stats.ttest_ind(
        x_tau, y_tau, equal_var = True, alternative = alternative
        )
    welch_t_test = stats.ttest_ind(
        x_tau, y_tau, equal_var = False, alternative = alternative
        )
    linear_reg = stats.linregress(x_tau, y_tau)
    r_squared = linear_reg.rvalue**2
    
    larger_var = np.max([x_stats.var, y_stats.var])
    smaller_var = np.min([x_stats.var, y_stats.var])
    var_ratio = larger_var / smaller_var
    ratio_test = var_ratio < 2
    
    if ratio_test == True:
        cohens_d_stat = cohens_d(x_tau, y_tau, t = std_t_test.statistic)
        p_value = round(std_t_test.pvalue, 5)
    else:
        cohens_d_stat = cohens_d(x_tau, y_tau, t = welch_t_test.statistic)
        p_value = round(welch_t_test.pvalue, 5)
    
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
        
        summary_x_y = ("Variance ratio: {larger_var} / {smaller_var} = " +\
                       "{var_ratio}\n" +\
                       "Ratio test: {var_ratio} < 2: {ratio_test}\n\n" +\
                       "Standard t-test statistic = {std_t_test_stat}\n" +\
                       "Standard t-test p-value = {std_t_test_pvalue}\n" +\
                       "Welch’s t-test statistic = {welch_t_test_stat}\n" +\
                       "Welch’s t-test p-value = {welch_t_test_pvalue}\n\n" +\
                       "Cohen's d = {cohens_d_stat}\n" +\
                       "Coefficient of determination (R squared) = " +\
                       "{r_squared}")\
                       .format(
                           larger_var = larger_var, smaller_var = smaller_var,
                           var_ratio = var_ratio, 
                           ratio_test = str(ratio_test).upper(),
                           std_t_test_stat = std_t_test.statistic,
                           std_t_test_pvalue = std_t_test.pvalue,
                           welch_t_test_stat = welch_t_test.statistic,
                           welch_t_test_pvalue = welch_t_test.pvalue,
                           cohens_d_stat = cohens_d_stat,
                           r_squared = r_squared
                           )
        
        print(
            line, 
            title_x, summary_x, line, 
            title_y, summary_y, line, 
            title_x_y, summary_x_y, line,
            sep = "\n\n"
            )
    
    if plot == True:
        plot_hypothesis(
            x, y, key, p_value, x_name, y_name, lam_c, n_cycles,
            repetitions
            )
    
    out = out_data(
        var_ratio, std_t_test, welch_t_test, cohens_d, r_squared, x_stats, 
        y_stats
        )
    
    return out

def cohens_d(x, y, t = None, abs = True):
    """Compute Cohen's :math:`d`.
    
    This function assumes that ``x`` and ``y`` have equal sizes.
    """
    x_n, y_n = len(x), len(y)
    # x_var, y_var = np.var(x, ddof = 0), np.var(y, ddof = 0)
    # x_std, y_std = np.std(x, ddof = 0), np.std(y, ddof = 0)
    
    df = x_n + y_n - 2
    
    # Salkind (2010) | Equation 9
    if not t == None:
        out = (t * (x_n + y_n)) / (np.sqrt(df) * np.sqrt(x_n * y_n))
    else:
        # Salkind (2010) | Equation 7
        # Only when sample sizes are equal.
        sd_pooled = np.sqrt((np.var(x) + np.var(y)) / 2)
        
        out = (np.mean(x) - np.mean(y)) / sd_pooled
    
    if abs == True: out = np.abs(out)
    
    return out

def plot_hypothesis(x, y, key, p_value, x_name = None, y_name = None, 
                    lam_c = None, n_cycles = None, repetitions = None):
    """Plot results of 'test_hypothesis()'."""
    x = [i["tau"] for i in np.array(x[key])]
    y = [i["tau"] for i in np.array(y[key])]
    n = len(x)

    if x_name == None: x_name = "None"
    if y_name == None: y_name = "None"

    title = ("Key = {key}, N = ${n}$, $\\lambda_c = {lam_c}$, " +\
             "Cycles = ${n_cycles}$, " +\
             "Repetitions = ${repetitions}$, p-value = {p_value}")\
             .format(key = key.title(), n = str(n), lam_c = str(lam_c), 
                     n_cycles = str(n_cycles), repetitions = str(repetitions), 
                     p_value = str(p_value))
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    sns.kdeplot(x, color = "red", label = x_name, linewidth = 1, 
            warn_singular = False)
    sns.kdeplot(y, color = "blue", label = y_name, linewidth = 1, 
                warn_singular = False)
    ax.set_xlabel("$\\tau$")
    ax.set_ylabel("Kernel Density Estimate (KDE)")
    ax.set_xlim(23.5, 24.6)
    ax.set_title(title, fontsize = 8)
    
    plt.legend(fontsize = 8)
    plt.show()
    
    return None

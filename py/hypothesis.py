import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# labren(72272)
north = run_model(
    n = 10 ** 3, labren_id = 72272, by = "season", n_cycles = 3, 
    repetitions = 100, plot = False
    )

# labren(1)
south = run_model(
    n = 10 ** 3, labren_id = 1, by = "season", n_cycles = 3, 
    repetitions = 100, plot = False
    )

def analyze_data(group, key, name):
    data = [i["tau"] for i in np.array(group[key])]
    
    kstest = stats.kstest(data, stats.norm.cdf)
    kstest_stats = round(kstest.statistic, 3)

    shapiro = stats.shapiro(data)
    shapiro_stats = round(shapiro.statistic, 3)
    
    # anderson = stats.anderson(data, dist = "norm")
    
    mean = round(np.mean(data), 3)
    
    title = ("Group = {name}, Key = {key}, Mean = ${mean}$, " +\
             "KS = ${kstest_stats}$, Shapiro-Wilk = ${shapiro_stats}$")\
             .format(name = name, key = key.title(), mean = str(mean),
              kstest_stats = str(kstest_stats),
              shapiro_stats = str(shapiro_stats))
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    ax.hist(data, density = True, edgecolor = "black", color = "red")
    ax.set_title(title, fontsize = 8)
    plt.show()

for i in list(north): analyze_data(north, i, "Nascente do rio Ailã")
for i in list(south): analyze_data(south, i, "Arroio Chuí")

def test_hypothesis(key, x = north, y = south, 
                    x_name = "Nascente do rio Ailã (Lat.: $5.272$)", 
                    y_name = "Arroio Chuí (Lat.: $- 33.752$)", 
                    lam_c = 4727.833, n_cycles = 3, repetitions = 100):
    x = [i["tau"] for i in np.array(x[key])]
    y = [i["tau"] for i in np.array(y[key])]
    
    print("\n---------------------------------------------------------\n")
    
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
    
    print("\n---------------------------------------------------------\n")
    
    plot_hypothesis(
        key, ttest_stats, x, y, x_name, y_name, lam_c, n_cycles,repetitions
        )
    
    return(ttest)

def plot_hypothesis(key, p_value, x = north, y = south, 
                    x_name = "Nascente do rio Ailã (Lat.: $5.272$)", 
                    y_name = "Arroio Chuí (Lat.: $- 33.752$)", 
                    lam_c = 4727.833, n_cycles = 3, repetitions = 100):
    n = len(x)

    title = ("Key = {key}, N = ${n}$, $\\lambda_c = {lam_c}$, " +\
             "Cycles = ${n_cycles}$, " +\
             "Repetitions = ${repetitions}$, P-value = {p_value}")\
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

for i in list(north): test_hypothesis(i, north, south)

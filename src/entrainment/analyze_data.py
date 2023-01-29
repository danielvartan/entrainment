import matplotlib.pyplot as plt
import numpy as np
import scipy
import seaborn as sns
import statsmodels.api as sm
from collections import namedtuple
from scipy import stats

def analyze_data(turtles, key, name = None, print_ = True, plot_hist_ = True,
                 plot_qq_ = True):
    """Compute and plot 'tau' statistics."""
    data = [i["tau"] for i in np.array(turtles[key])]
    
    out_data = namedtuple("analyze_data", [
        "mean", "var", "std", "min", "q_1", "median", "q_3", "max", "kurtosis",
        "skew", "kstest", "shapiro"
        ])
    
    out = out_data(
        np.mean(data), np.var(data), np.std(data), np.quantile(data, 0), 
        np.quantile(data, 0.25), np.quantile(data, 0.5), 
        np.quantile(data, 0.75), np.quantile(data, 1), stats.kurtosis(data),
        stats.skew(data), stats.kstest(data, stats.norm.cdf), 
        stats.shapiro(data)
        )
    
    if print_ == True:
        line = "---------------------------------------------------------"
        
        title = ("[Group: {name} | Key: {key}]")\
                 .format(name = name, key = key.title())
        
        summary = ("Mean = {mean}\nVar. = {var}\nSD = {std}\n\n" +\
                   "Min. = {min}\n1st Qu. = {q_1}\nMedian = {median}\n" +\
                   "3rd Qu. = {q_3}\nMax. = {max}\n\n" +\
                   "Kurtosis = {kurtosis}\nSkewness = {skew}\n\n" +\
                   "Kolmogorov-Smirnov test p-value = {kstest}\n" +\
                   "Shapiro-Wilks test p-value = {shapiro}")\
                   .format(
                       mean = out.mean, var = out.var, std = out.std,
                       min = out.min, q_1 = out.q_1, median = out.median,
                       q_3 = out.q_3, max = out.max, kurtosis = out.kurtosis,
                       skew = out.skew, kstest = out.kstest.pvalue,
                       shapiro = out.shapiro.pvalue
                       )

        print(line, title, summary, line, sep = "\n\n")
    
    title = ("Group = {name}, Key = {key}, Mean = ${mean}$, " +\
             "KS = ${kstest}$, Shapiro-Wilk = ${shapiro}$")\
             .format(
                 name = name, key = key.title(), mean = round(out.mean, 3),
                 kstest = round(out.kstest.pvalue, 3),
                 shapiro = round(out.shapiro.pvalue, 3)
                 )
    
    if plot_hist_ == True: plot_hist(turtles, key, name)
    if plot_qq_ == True: plot_qq(turtles, key, name)
    
    return out

def plot_hist(turtles, key, name = None):
    data = np.array([i["tau"] for i in np.array(turtles[key])])
    title = analyze_data_title(data, key, name)
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    ax.hist(data, density = True, edgecolor = "white", color = "#bcbcbc")
    sns.kdeplot(data, color = "red", linewidth = 1, warn_singular = False)
    
    ax.set_title(title, fontsize = 8)
    ax.set_xlabel("$\\tau$")
    ax.set_ylabel("Frequency")
    
    plt.show()
    
    return None

def plot_qq(turtles, key, name = None, dist = scipy.stats.distributions.norm):
    data = np.array([i["tau"] for i in np.array(turtles[key])])
    title = analyze_data_title(data, key, name)

    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    sm.qqplot(
        np.array(data), dist = dist, line = "s", marker = "o", 
        markerfacecolor = "None", markeredgecolor = "black",
        markeredgewidth = 0.5, ax = ax
        )
    
    ax.set_title(title, fontsize = 8)
    ax.set_xlabel("Theoretical quantiles (Standard normal)")
    ax.set_ylabel("Sample quantiles ($\\tau$)")
    
    plt.show()
    
    return None

def analyze_data_title(data, key, name = None):
    out = ("Group = {name}, Key = {key}, Mean = ${mean}$, " +\
           "KS = ${kstest}$, Shapiro-Wilk = ${shapiro}$")\
            .format(
                name = name, key = key.title(), mean = round(np.mean(data), 3),
                kstest = round(stats.kstest(data, stats.norm.cdf).pvalue, 3),
                shapiro = round(stats.shapiro(data).pvalue, 3)
                )
    
    return out

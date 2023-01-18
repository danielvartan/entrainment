import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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

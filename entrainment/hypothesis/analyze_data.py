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

# # labren(72272)
# north = run_model(
#     n = 10 ** 3, labren_id = 72272, by = "season", n_cycles = 3, 
#     repetitions = 100, plot = False
#     )

# # labren(1)
# south = run_model(
#     n = 10 ** 3, labren_id = 1, by = "season", n_cycles = 3, 
#     repetitions = 100, plot = False
#     )

# for i in list(north): analyze_data(north, i, "Nascente do rio Ailã")
# for i in list(south): analyze_data(south, i, "Arroio Chuí")

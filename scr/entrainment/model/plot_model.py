import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_model(turtles, lam_c, labren_id, n_cycles, repetitions):
    if len(turtles) == 13:
        colors = sns.color_palette("tab10", 12)
    else:
        colors = ["#f98e09", "#bc3754", "#57106e", "#5ec962"]
    
    n = len(turtles[list(turtles)[0]])
    lat = labren(labren_id)["lat"]
    start = list(turtles)[1].title()
    labels = [i.title() for i in list(turtles)]
    
    title = ("N = ${n}$, $\\lambda_c = {lam_c}$, Latitude = ${lat}$, " +\
             "Cycles = ${n_cycles}$, Start = {start}, " +\
             "Repetitions = ${repetitions}$")\
             .format(n = str(n), lam_c = str(lam_c), lat = str(lat), 
              n_cycles = str(n_cycles), start = start, 
              repetitions = str(repetitions))
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    
    for i, j in enumerate(turtles):
        tau_i = [i["tau"] for i in np.array(turtles[j])]
        n = len(tau_i)
        
        if (i == 0):
            color = "black"
            linewidth = 3
        else:
            color = colors[i - 1]
            linewidth = 1
        
        sns.kdeplot(tau_i, color = color, label = labels[i], 
                    linewidth = linewidth, warn_singular = False)

    ax.set_xlabel("$\\tau$")
    ax.set_ylabel("Kernel Density Estimate (KDE)")
    ax.set_xlim(23.5, 24.6)
    ax.set_title(title, fontsize = 8)
    
    plt.legend(fontsize = 8)
    plt.show()

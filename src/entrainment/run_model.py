import functools
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from .labren import labren
from .utils import reorder
from collections import namedtuple

# TODO: Change dict to namedtuple (change labren functions also)
# np.array(entrainment.labren.labren(72272)["ts"]).mean() ~ 4727.833
def run_model(
    n = 10**3, tau_range = (23.5, 24.6), tau_mean = 24.15, tau_sd = 0.2, 
    k_range = (0.001, 0.01), k_mean = 0.001, k_sd = 0.005, lam_c = 3750, 
    labren_id = 1, by = "season", n_cycles = 3, start_at = 0, 
    repetitions = 10**2, plot = True
    ):
    """Compute the entrainment model.
    
    This function has already a set of default values configured for testing
    purposes. To see it in action, just run ``run_model()``.
    
    :Example:
    
    >>> model = entrainment.run_model(
        n = 10**3, labren_id = 72272, by = "season", lam_c = 3750, 
        n_cycles = 3, repetitions = 10**2
        )
    
    >>> model = entrainment.run_model(
        n = 10**3, labren_id = 1, by = "season", lam_c = 3750, 
        n_cycles = 3, repetitions = 10**2
        )
    """
    turtles_0 = create_turtles(
        n, tau_range, tau_mean, tau_sd, k_range, k_mean, k_sd
        )
    
    if by == "month":
        labels = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", 
            "Oct", "Nov", "Dec"
            ]
        
        labren_data = labren(labren_id, by = "month")["ts"]
        cycle = 12
    elif by == "season":
        labels = ["Summer", "Autumn", "Winter", "Spring"]
        labren_data = labren(labren_id, by = "season")["ts"]
        cycle = 4
    else:
        labels = ["Annual"]
        labren_data = [labren(labren_id, by = "year")["ts"]]
        cycle = 1
    
    if by != "year":
        labels = reorder(labels, start_at)
        labren_data = reorder(labren_data, start_at)
    
    if not n_cycles == 1:
        labels_0, labren_data_0 = tuple(labels), tuple(labren_data)
        [labels.extend(labels_0) for i in range(n_cycles - 1)]
        [labren_data.extend(labren_data_0) for i in range(n_cycles - 1)]
    
    if repetitions == 0:
        turtles = {"unentrain": turtles_0}
        
        for i in range(cycle * n_cycles):
            key = list(turtles)[-1]
            lam = labren_data[i]
            turtles_i = entrain_turtles(
                turtles[key], turtles_0, lam, lam_c
                )
            turtles[labels[i].lower()] = turtles_i
    else:
        turtles_n = {}
        
        for i in range(repetitions + 1):
            turtles_i = {"unentrain": turtles_0}
            
            for j in range(cycle * n_cycles):
                key = list(turtles_i)[-1]
                lam = labren_data[j]
                turtles_j = entrain_turtles(
                    turtles_i[key], turtles_0, lam, lam_c,
                    )
                turtles_i[labels[j].lower()] = turtles_j
            
            turtles_n["r_" + str(i + 1)] = turtles_i
        
        turtles = average_turtles(turtles_n)

    if plot == True: 
        plot_model(turtles, lam_c, labren_id, n_cycles, repetitions)
    
    return turtles

def create_turtles(n = 10**2, tau_range = (23.5, 24.6), tau_mean = 24.15, 
                   tau_sd = 0.2, k_range = (0.001, 0.01), k_mean = 0.001, 
                   k_sd = 0.005):
    """Create turtles/subjects for the entrainment model.
    
    :Example:
    
    >>> create_turtles(1)
    """
    turtles = []
    
    for i in range(n):
        tau = np.random.normal(tau_mean, tau_sd)
        k = np.random.normal(k_mean, k_sd)
        
        if (tau < tau_range[0]): tau = tau_range[0]
        if (tau > tau_range[1]): tau = tau_range[1]
        if (k < k_range[0]): k = k_range[0]
        if (k > k_range[1]): k = k_range[1]
        
        turtles.append({"tau": tau, "k": k})
    
    return turtles

def entrain(lam, lam_c, k, tau, tau_ref = 24):
    """Compute the (un)entrainment function.
    
    :Example:
    
    >>> entrain(lam = 10, lam_c = 4, k = 10, tau = 19, tau_ref = 24)
    """
    logi_f = (tau_ref - tau) / (1 + np.exp(1) ** (- k * (lam - lam_c)))
    out = tau + logi_f
    error = np.random.uniform(low = 0, high = 1) * np.abs(out - tau)
    
    if out >= tau:
        out = out - error
    else:
        out = out + error
    
    return out

def entrain_turtles(turtles, turtles_0, lam, lam_c):
    """Entrain turtles/subjects.
    
    :Example:
    
    >>> entrain_turtles(
        turtles =create_turtles(5), turtles_0 = create_turtles(5),
        lam = 10, lam_c = 4
        )
    """
    n = len(turtles)
    out = []
    
    for i in range(n):
        tau_0 = turtles_0[i]["tau"]
        tau = turtles[i]["tau"]
        k = turtles[i]["k"]
        
        if (lam >= lam_c):
            tau_i = entrain(lam, lam_c, k, tau, tau_ref = 24)
        else:
            tau_i = entrain(lam, lam_c, k, tau, tau_ref = tau_0)
        
        out.append({"tau": tau_i, "k": k})
    
    return out

def average_turtles(turtles_n):
    """Average turtles/subjects values after n repetitions.
    
    :Example:
    
    >>> average_turtles(create_turtles(5))
    """
    n = len(turtles_n)
    keys = list(turtles_n[list(turtles_n)[0]])
    out = {}
    
    for i in keys: # i = 0 => "unentrain"
        turtles_i = []
        
        for a, b in enumerate(turtles_n): # a = 0 => b = "r_1"
            turtles_i.append(turtles_n[b][i])
        
        tau_i, k_i = [], []
        
        for a in range(len(turtles_i)):
            tau_i.append([b["tau"] for b in np.array(turtles_i[a])])
            k_i.append([b["k"] for b in np.array(turtles_i[a])])
        
        tau_i = functools.reduce(lambda x, y: np.array(x) + np.array(y), 
                                 tau_i) / n
        k_i = functools.reduce(lambda x, y: np.array(x) + np.array(y), 
                               k_i) / n
        
        turtles_i = []
        
        for a in range(len(tau_i)):
            turtles_i.append({"tau": tau_i[a], "k": k_i[a]})
        
        out[i] = turtles_i
        
    return out

def plot_model(turtles, lam_c, labren_id, n_cycles, repetitions):
    """Plot the entrainment model.
    
    :Example:
    
    >>> plot_model(
        turtles = entrainment.run_model(
            labren_id = 1000, plot = False, repetitions = 10
            ),
            lam_c = 3750, labren_id = 1000, n_cycles = 3, repetitions = 10
            )
    """
    if len(turtles) == 13:
        colors = sns.color_palette("tab10", 12)
    elif len(turtles) == 5:
        colors = ["#f98e09", "#bc3754", "#57106e", "#5ec962"]
    else:
        colors = ["red"]
    
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
    
    return None

## Source this file before using it.

import functools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def f_exact(lam, lam_c, k, tau, tau_ref = 24):
    logi_f = (tau_ref - tau) / (1 + np.exp(1) ** (- k * (lam - lam_c)))
    out = tau + logi_f

    return(out)

def exact(f, lam_c, k, tau, lam_0 = 0, lam_n = 10, h = 10 ** (- 3)):
    lam_list, y_list = [lam_0], [f(lam_0, lam_c, k, tau)]
    
    while lam_0 < lam_n:
        x_next = lam_0 + h
        y_next = f(x_next, lam_c, k, tau)
        lam_0 = x_next
        lam_list.append(x_next)
        y_list.append(y_next)
    
    return [lam_list, y_list]

def plot_exact(f, lam_c, k, tau, lam_0 = 0, lam_n = 10, 
               h = 10 ** (- 3)):
    data = exact(f, lam_c, k, tau, lam_0, lam_n)

    title = ("$\\lambda_c = {lam_c}$, $k = {k}$, $\\tau = {tau}$")\
         .format(lam_c = str(lam_c), k = str(k), tau = str(tau))

    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    ax.plot(data[0], data[1], "r-", linewidth = 1)
    ax.set_xlabel("$\\lambda$")
    ax.set_ylabel("$f(\\lambda, \\lambda_{c}, k, \\tau)$")
    ax.set_title(title, fontsize = 10)
    plt.show()

plot_exact(f_exact, lam_c = 5, k = 2, tau = 22, lam_0 = 0, lam_n = 10)
plot_exact(f_exact, lam_c = 5, k = 2, tau = 26, lam_0 = 0, lam_n = 10)

def labren(id, name = None, by = "month",
           file = "./data/labren/global_horizontal_means.csv"):
    data = (
        pd.read_csv(filepath_or_buffer  = file, sep = ";")
        .rename(str.lower, axis = "columns")
        .loc[[id - 1]]
    )
    
    out = {"name": name}
    for i in list(data): out[i] = data.loc[id - 1, i]
    
    data = (
        data.iloc[:, 5:17]
        .transpose()
    )

    data.reset_index(inplace = True)
    data.columns = ["month", "x"]
    
    out["ts"] = list(data["x"])
    
    if by == "season":
        seasons = [
            ["Dec", "Jan", "Feb"], ["Mar", "Apr", "May"], ["Jun", "Jul", "Aug"], 
            ["Sep", "Oct", "Nov"]
            ]
        
        keys = ["name", "id", "country", "lon", "lat", "annual"]
        labels = ["Summer", "Autumn", "Winter", "Spring"]
        data = out
        out = {}
    
        for i, j in enumerate(data):
            if j in keys: out[j] = data[j]
        
        for i in range(4):
            mean = np.mean([data[i.lower()] for i in seasons[i]])
            out[labels[i].lower()] = mean
        
        out["ts"] = [out[i.lower()] for i in labels]
    
    return(out)

def plot_labren(id_1_index = 72272, id_2_index = 1,
                label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
                label_2 = "Arroio Chuí (Lat.: $- 33.752$)",
                by = "month"):
    if (by == "month"):
        x = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
            "Oct", "Nov", "Dec"
            ]
        
        y_1 = labren(id_1_index)["ts"]
        y_2 = labren(id_2_index)["ts"]
        xlabel = "Month"
    else:
        x = ["Summer", "Autumn", "Winter", "Spring"]
        y_1 = labren(id_1_index, by = "season")["ts"]
        y_2 = labren(id_2_index, by = "season")["ts"]
        xlabel = "Season"
    
    title = "Global Horizontal Solar Irradiation (Source: LABREN/INPE, 2017)"
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    ax.plot(x, y_1, "r-", label = label_1, linewidth = 1)
    ax.plot(x, y_2, "b-", label = label_2,  linewidth = 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("$Wh / m^{2}.day$")
    ax.set_title(title, fontsize = 10)
    
    plt.legend(fontsize = 8)
    plt.show()

plot_labren(
    id_1_index = 72272, id_2_index = 1,
    label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
    label_2 = "Arroio Chuí (Lat.: $- 33.752$)",
    by = "month"
    )

plot_labren(
    id_1_index = 72272, id_2_index = 1,
    label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
    label_2 = "Arroio Chuí (Lat.: $- 33.752$)",
    by = "season"
    )

def entrain(lam, lam_c, k, tau, tau_ref = 24):
    logi_f = (tau_ref - tau) / (1 + np.exp(1) ** (- k * (lam - lam_c)))
    out = tau + logi_f
    error = np.random.uniform(low = 0, high = 1) * np.abs(out - tau)
    
    if out >= tau:
        out = out - error
    else:
        out = out + error
    
    return(out)

def entrain_turtles(turtles, turtles_0, lam, lam_c, lam_c_tol):
    n = len(turtles)
    out = []
    
    for i in range(n):
        tau_0 = turtles_0[i]["tau"]
        tau = turtles[i]["tau"]
        k = turtles[i]["k"]
        
        if (lam >= (lam_c - lam_c_tol)):
            tau_i = entrain(lam, lam_c, k, tau, tau_ref = 24)
        else:
            tau_i = entrain(lam, lam_c, k, tau, tau_ref = tau_0)
        
        out.append({"tau": tau_i, "k": k})
    
    return(out)

def create_turtles(n = 10 **2, tau_range = (23.5, 24.6), tau_mean = 24.15, 
                   tau_dp = 0.2, k_range = (0.001, 0.01), k_mean = 0.001, 
                   k_dp = 0.005):
    turtles = []
    
    for i in range(n):
        tau = np.random.normal(tau_mean, tau_dp)
        k = np.random.normal(k_mean, k_dp)
        
        if (tau < tau_range[0]): tau = tau_range[0]
        if (tau > tau_range[1]): tau = tau_range[1]
        if (k < k_range[0]): k = k_range[0]
        if (k > k_range[1]): k = k_range[1]
        
        turtles.append({"tau": tau, "k": k})
    
    return(turtles)

# np.array(labren(72272)["ts"]).mean() ~ 4727.833
def run_model(
    n = 10 ** 3, tau_range = (23.5, 24.6), tau_mean = 24.15, tau_dp = 0.2, 
    k_range = (0.001, 0.01), k_mean = 0.001, k_dp = 0.005, lam_c = 4727.833, 
    lam_c_tol = 1000, labren_id = 1, by = "month", n_cycles = 3, start_at = 0, 
    repetitions = 10 ** 2, plot = True
    ):
    turtles_0 = create_turtles(
        n, tau_range, tau_mean, tau_dp, k_range, k_mean, k_dp
        )
    
    if (by == "month"):
        labels = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", 
            "Oct", "Nov", "Dec"
            ]
        
        labren_data = labren(labren_id)["ts"]
        cycle = 12
    else:
        labels = ["Summer", "Autumn", "Winter", "Spring"]
        labren_data = labren(labren_id, by = "season")["ts"]
        cycle = 4
    
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
                turtles[key], turtles_0, lam, lam_c, lam_c_tol
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
                    turtles_i[key], turtles_0, lam, lam_c, lam_c_tol
                    )
                turtles_i[labels[j].lower()] = turtles_j
            
            turtles_n["r_" + str(i + 1)] = turtles_i
        
        turtles = average_turtles(turtles_n)

    if plot == True: plot_model_density(
        turtles, lam_c, labren_id, n_cycles, repetitions
        )
    
    return(turtles)

def plot_model_density(turtles, lam_c, labren_id, n_cycles, repetitions):
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

def average_turtles(turtles_n):
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
        
    return(out)

def reorder(x, start_at = 0):
    n = len(x)
    
    if (not start_at == 0):
        order = list(np.arange(start_at, n))
        order.extend(list(np.arange(0, start_at)))
        
        return([x[i] for i in order])
    else:
        return(x)

# labren(72272)
x = run_model(
    labren_id = 72272, by = "season", n_cycles = 2, repetitions = 100
    )

# labren(1)
x = run_model(labren_id = 1, by = "season", n_cycles = 2, repetitions = 100)

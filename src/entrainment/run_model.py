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
        turtles = {"unentrained": turtles_0}
        
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
            turtles_i = {"unentrained": turtles_0}
            
            for j in range(cycle * n_cycles):
                key = list(turtles_i)[-1]
                lam = labren_data[j]
                turtles_j = entrain_turtles(
                    turtles_i[key], turtles_0, lam, lam_c,
                    )
                turtles_i[labels[j].lower()] = turtles_j
            
            turtles_n["r_" + str(i + 1)] = turtles_i
        
        turtles = average_turtles(turtles_n)
    
    out_data = namedtuple("model_data", ["turtles", "settings"])
    
    settings_data = namedtuple("model_settings", [
        "n", "tau_range", "tau_mean", "tau_sd", "k_range", "k_mean", "k_sd",
        "lam_c", "labren_id", "by", "n_cycles", "start_at", "repetitions"
        ])
    
    settings = settings_data(
        n, tau_range, tau_mean, tau_sd, k_range, k_mean, k_sd, lam_c, labren_id,
        by, n_cycles, start_at, repetitions
    )
    
    out = out_data(turtles, settings)
    
    if plot == True: plot_model_line(out)
    
    return out

def create_turtles(n = 10**2, tau_range = (23.5, 24.6), tau_mean = 24.15, 
                   tau_sd = 0.2, k_range = (0.001, 0.01), k_mean = 0.001, 
                   k_sd = 0.005):
    """Create turtles/subjects for the entrainment model."""
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
    """Compute the (un)entrainment function."""
    logi_f = (tau_ref - tau) / (1 + np.exp(1) ** (- k * (lam - lam_c)))
    out = tau + logi_f
    error = np.random.uniform(low = 0, high = 1) * np.abs(out - tau)
    
    if out >= tau:
        out = out - error
    else:
        out = out + error
    
    return out

def entrain_turtles(turtles, turtles_0, lam, lam_c):
    """Entrain turtles/subjects."""
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
    """Average turtles/subjects values after n repetitions."""
    n = len(turtles_n)
    keys = list(turtles_n[list(turtles_n)[0]])
    out = {}
    
    for i in keys: # i = 0 => "unentrained"
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

def plot_model_line(model):
    """Plot the entrainment model."""
    settings = model.settings
    turtles = model.turtles
    
    if len(turtles) == 13:
        colors = sns.color_palette("tab10", 12)
    elif len(turtles) == 5:
        colors = ["#f98e09", "#bc3754", "#57106e", "#5ec962"]
    else:
        colors = ["red"]
    
    if not len(colors) == 1: colors = reorder(colors, settings.start_at)
    labels = [i.title() for i in list(turtles)]
    
    start = list(turtles)[1].title()
    labels = [i.title() for i in list(turtles)]
    lat = labren(settings.labren_id)["lat"]
    
    title = ("N = ${n}$, $\\lambda_c = {lam_c}$, Latitude = ${lat}$, " +\
             "Cycles = ${n_cycles}$, Start = {start}, " +\
             "Repetitions = ${repetitions}$")\
             .format(
                 n = settings.n, lam_c = settings.lam_c, lat = lat, 
                 n_cycles = settings.n_cycles, 
                 start = start, repetitions = settings.repetitions
                     )
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    
    for i, j in enumerate(turtles):
        tau_i = [k["tau"] for k in np.array(turtles[j])]

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

def plot_model_line_1_2(x, y, x_title = "(A)", y_title = "(B)", 
                        legend_plot = "y", legend_loc = "upper right", 
                        legend_fontsize = "small"):
    x_settings = x.settings
    y_settings = y.settings
    x_turtles = x.turtles
    y_turtles = y.turtles
    
    if len(x_turtles) == 13:
        colors = sns.color_palette("tab10", 12)
    elif len(x_turtles) == 5:
        colors = ["#f98e09", "#bc3754", "#57106e", "#5ec962"]
    else:
        colors = ["red"]
    
    if not len(colors) == 1:
        x_colors = reorder(colors, x_settings.start_at)
        y_colors = reorder(colors, y_settings.start_at)
    else:
        x_colors, y_colors = colors, colors
    
    x_labels = [i.title() for i in list(x_turtles)]
    y_labels = [i.title() for i in list(y_turtles)]
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, [ax_x, ax_y] = plt.subplots(nrows = 1, ncols = 2)
    
    for i, j in enumerate(x_turtles):
        tau_i = [k["tau"] for k in np.array(x_turtles[j])]

        if (i == 0):
            color_i = "black"
            linewidth = 3
        else:
            color_i = x_colors[i - 1]
            linewidth = 1
        
        sns.kdeplot(tau_i, ax = ax_x, color = color_i, label = x_labels[i], 
                    linewidth = linewidth, warn_singular = False)
    
    for i, j in enumerate(y_turtles):
        tau_i = [k["tau"] for k in np.array(y_turtles[j])]
        
        if (i == 0):
            color_i = "black"
            linewidth = 3
        else:
            color_i = y_colors[i - 1]
            linewidth = 1
        
        sns.kdeplot(tau_i, ax = ax_y, color = color_i, label = y_labels[i], 
                    linewidth = linewidth, warn_singular = False)
    
    y_max = np.max([ax_x.get_ylim()[1], ax_y.get_ylim()[1]])
    
    ax_x.set_xlabel("$\\tau$")
    ax_x.set_ylabel("Kernel Density Estimate (KDE)")
    ax_x.set_title(x_title, fontsize = 10)
    ax_x.set_xlim(23.5, 24.6)
    ax_x.set_ylim(0, y_max)

    ax_y.set_xlabel("$\\tau$")
    ax_y.set_ylabel("")
    ax_y.set_title(y_title, fontsize = 10)
    ax_y.set_xlim(23.5, 24.6)
    ax_y.set_ylim(0, y_max)
    ax_y.get_yaxis().set_visible(False)
    
    if legend_plot == "x":
        ax_x.legend(loc = legend_loc, fontsize = legend_fontsize)
    else:
        ax_y.legend(loc = legend_loc, fontsize = legend_fontsize)
    
    plt.show()
    
    return None

def plot_model_violin(model):
    """Plot the entrainment model."""
    settings = model.settings
    turtles = model.turtles
    
    if len(turtles) == 13:
        colors = sns.color_palette("tab10", 12)
    elif len(turtles) == 5:
        colors = ["#f98e09", "#bc3754", "#57106e", "#5ec962"]
    else:
        colors = ["red"]
    
    if not len(colors) == 1: colors = reorder(colors, settings.start_at)

    data = []
    means = []
    
    for i in list(turtles):
        data_i = [j["tau"] for j in np.array(turtles[i])]
        data.append(data_i)
        means.append(np.mean(data_i))

    title = ("N = ${n}$, $\\lambda_c = {lam_c}$, Latitude = ${lat}$, " +\
             "Cycles = ${n_cycles}$, Start = {start}, " +\
             "Repetitions = ${repetitions}$")\
             .format(
                 n = settings.n, lam_c = settings.lam_c, 
                 lat = labren(settings.labren_id)["lat"], 
                 n_cycles = settings.n_cycles, 
                 start = list(turtles)[1].title(), 
                 repetitions = settings.repetitions
                 )
    
    labels = list(map(str.title, list(turtles)))
    labels_pos = np.arange(1, len(data) + 1)
    colors.insert(0, "#000000")
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    plot = ax.violinplot(
        data, vert = True, showextrema = False, showmeans = False
        )
    ax.scatter(
        labels_pos, means, marker = "o", color = "red", s = 10, zorder = 3
        )
    
    for i, pc in enumerate(plot["bodies"]):
        pc.set_facecolor(colors[i])
        pc.set_edgecolor('black')
    
    ax.set_xticks(labels_pos, labels = labels)
    ax.set_title(title, fontsize = 8)
    ax.set_ylabel("$\\tau$")
    
    plt.show()
    
    return None

def plot_model_violin_1_2(x, y, x_title = "(A)", y_title = "(B)", 
                          legend_plot = "y", legend_loc = "upper right", 
                          legend_fontsize = "small"):
    x_settings = x.settings
    y_settings = y.settings
    x_turtles = x.turtles
    y_turtles = y.turtles
    
    if len(x_turtles) == 13:
        colors = sns.color_palette("tab10", 12)
    elif len(x_turtles) == 5:
        colors = ["#f98e09", "#bc3754", "#57106e", "#5ec962"]
    else:
        colors = ["red"]
    
    if not len(colors) == 1:
        x_colors = reorder(colors, x_settings.start_at)
        y_colors = reorder(colors, y_settings.start_at)
    else:
        x_colors, y_colors = colors, colors
    
    x_data = []
    x_means = []
    
    for i in list(x_turtles):
        data_i = [j["tau"] for j in np.array(x_turtles[i])]
        x_data.append(data_i)
        x_means.append(np.mean(data_i))
    
    y_data = []
    y_means = []
    
    for i in list(y_turtles):
        data_i = [j["tau"] for j in np.array(y_turtles[i])]
        y_data.append(data_i)
        y_means.append(np.mean(data_i))
    
    x_labels = list(map(str.title, list(x_turtles)))
    x_labels_pos = np.arange(1, len(x_turtles) + 1)
    x_labels_pos = x_labels_pos[::-1]
    
    y_labels = list(map(str.title, list(y_turtles)))
    y_labels_pos = np.arange(1, len(y_turtles) + 1)
    y_labels_pos = y_labels_pos[::-1]
    
    x_colors = ["#000000"] + x_colors
    x_colors.reverse()
    
    y_colors = ["#000000"] + y_colors
    y_colors.reverse()
    
    x_data.reverse()
    y_data.reverse()
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, [ax_x, ax_y] = plt.subplots(nrows = 1, ncols = 2)

    x_plot = ax_x.violinplot(
        x_data, vert = False, showextrema = False, showmeans = False
        )
    ax_x.scatter(
        x_means, x_labels_pos, marker = "o", color = "red", s = 10, 
        zorder = 3
        )
    
    for i, pc in enumerate(x_plot["bodies"]):
        pc.set_facecolor(x_colors[i])
        pc.set_edgecolor('black')
    
    y_plot = ax_y.violinplot(
        y_data, vert = False, showextrema = False, showmeans = False
        )
    ax_y.scatter(
        y_means, y_labels_pos, marker = "o", color = "red", s = 10, zorder = 3
        )
    
    for i, pc in enumerate(y_plot["bodies"]):
        pc.set_facecolor(y_colors[i])
        pc.set_edgecolor('black')
    
    ax_x.set_yticks(x_labels_pos, labels = x_labels)
    ax_x.set_ylabel("$\\tau$")
    ax_x.set_title(x_title, fontsize = 10)
    ax_x.set_xlim(23.5, 24.6)
    
    ax_y.set_yticks(y_labels_pos, labels = y_labels)
    ax_y.set_title(y_title, fontsize = 10)
    ax_y.set_xlim(23.5, 24.6)
    ax_y.get_yaxis().set_visible(False)
    
    plt.show()
    
    return None

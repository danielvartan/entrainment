import functools
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from .labren import labren
from .utils import reorder
from alive_progress import alive_bar
from box import Box

def run_model(
    n = 10**3, tau_range = (23.5, 24.6), tau_mean = 24.15, tau_sd = 0.2, 
    k_range = (0.001, 0.01), k_mean = 0.001, k_sd = 0.005, lam_c = 3750, 
    labren_id = 1, by = "season", n_cycles = 3, start_at = 0, 
    repetitions = 10**2, plot = True, show_progress = True
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
    cli_progress_step("! Creating turtles", show_progress)
    
    turtles_0 = create_turtles(
        n, tau_range, tau_mean, tau_sd, k_range, k_mean, k_sd
        )
    
    cli_progress_step("! Entraining turtles", show_progress)

    if repetitions == 0:
        turtles = cycle_turtles(
            turtles_0, lam_c, labren_id = labren_id, by = by, 
            n_cycles = n_cycles, start_at = start_at
            )
    else:
        turtles_n = Box()
        
        with alive_bar(
            repetitions, title = "- Repeating model", force_tty = True,
            length = 10, disable = not show_progress
            ) as bar:
            for i in range(repetitions):
                turtles_n["r_" + str(i + 1)] = cycle_turtles(
                    turtles_0, lam_c, labren_id = labren_id, by = by, 
                    n_cycles = n_cycles, start_at = start_at
                    )
                bar()
        
        turtles = average_turtles(turtles_n)
    
    out = Box(
        turtles = Box(turtles, frozen_box = True), 
        settings = Box(
            n = n, tau_range = tau_range, tau_mean = tau_mean, tau_sd = tau_sd,
            k_range = k_range, k_mean = k_mean, k_sd = k_sd, lam_c = lam_c,
            labren_id = labren_id, by = by, n_cycles = n_cycles,
            start_at = start_at, repetitions = repetitions, 
            frozen_box = True
            ),
            frozen_box = True
            )
    
    if plot == True:
        cli_progress_step("! Plotting turtles", show_progress)
        plot_model_line(out)
    
    return out

def create_turtles(
    n = 10, tau_range = (23.5, 24.6), tau_mean = 24.15, tau_sd = 0.2, 
    k_range = (0.001, 0.01), k_mean = 0.001, k_sd = 0.005
    ):
    """Create turtles/subjects for the entrainment model."""
    out = []
    
    for i in range(n):
        tau = np.random.normal(tau_mean, tau_sd)
        k = np.random.normal(k_mean, k_sd)
        
        if (tau < tau_range[0]): tau = tau_range[0]
        if (tau > tau_range[1]): tau = tau_range[1]
        if (k < k_range[0]): k = k_range[0]
        if (k > k_range[1]): k = k_range[1]
        
        out.append(Box(tau = tau, k = k, frozen_box = True))
    
    return tuple(out)

def entrain(tau, k, lam, lam_c, tau_ref = 24):
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
    out = []
    
    for i in range(len(turtles)):
        tau_0 = turtles_0[i].tau
        tau = turtles[i].tau
        k = turtles[i].k
        
        if (lam >= lam_c):
            tau_i = entrain(tau, k, lam, lam_c, tau_ref = 24)
        else:
            tau_i = entrain(tau, k, lam, lam_c, tau_ref = tau_0)
        
        out.append(Box(tau = tau_i, k = k, frozen_box = True))
    
    return tuple(out)

def cycle_turtles(
    turtles_0, lam_c, labren_id = 1, by = "season", n_cycles = 3, start_at = 0
    ):
    if by == "month":
        labels = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", 
            "Oct", "Nov", "Dec"
            ]
        labren_data = list(labren(labren_id, by = "month")["ts"])
        cycle = 12
    elif by == "season":
        labels = ["Summer", "Autumn", "Winter", "Spring"]
        labren_data = list(labren(labren_id, by = "season")["ts"])
        cycle = 4
    else:
        labels = ["Annual"]
        labren_data = [labren(labren_id, by = "year")["ts"]]
        cycle = 1
    
    if not by == "year":
        labels = reorder(labels, start_at)
        labren_data = reorder(labren_data, start_at)
    
    if not n_cycles == 1:
        labels_0, labren_data_0 = tuple(labels), tuple(labren_data)
        [labels.extend(labels_0) for i in range(n_cycles - 1)]
        [labren_data.extend(labren_data_0) for i in range(n_cycles - 1)]
    
    out = Box({"unentrained": turtles_0})
        
    for i in range(cycle * n_cycles):
        key = list(out)[-1]
        lam = labren_data[i]
        turtles_i = entrain_turtles(
            out[key], turtles_0, lam, lam_c
            )
        
        out[labels[i].lower()] = turtles_i
    
    return Box(out, frozen_box = True)

def average_turtles(turtles_n):
    """Average turtles/subjects values after n repetitions."""
    n = len(turtles_n)
    keys = list(turtles_n.r_1)[1::]
    out = Box({"unentrained": turtles_n.r_1.unentrained})
    
    for i in keys: # i = 0 => "unentrained"
        turtles_i = []
        
        ## Group all turtles from key 'i' in 'turtles_i' (each repetition)
        for a, b in enumerate(turtles_n): # a = 0 => b = "r_1"
            turtles_i.append(turtles_n[b][i])
        
        ## Separate 'tau' and 'k' value from each repetition
        tau_i, k_i = [], []
        
        for a in range(len(turtles_i)):
            tau_i.append([b["tau"] for b in np.array(turtles_i[a])])
            k_i.append([b["k"] for b in np.array(turtles_i[a])])
        
        ## Average 'tau' and 'k' values
        tau_i = functools.reduce(lambda x, y: np.array(x) + np.array(y), 
                                 tau_i) / n
        k_i = functools.reduce(lambda x, y: np.array(x) + np.array(y), 
                               k_i) / n
        
        ## Store the average turtles from key 'i' 'out'
        turtles_i = []
        
        for a in range(len(tau_i)):
            turtles_i.append(
                Box(tau = tau_i[a], k = k_i[a], frozen_box = True)
                )
        
        out[i] = tuple(turtles_i)
        
    return Box(out, frozen_box = True)

def cli_progress_step(msg, show_progress = True):
    if show_progress == True:
        print(msg)
    
    return None

def plot_model_colors(model):
    if model.settings.by == "month":
        out = sns.color_palette("tab10", 12)
    elif model.settings.by == "season":
        out = ["#f98e09", "#bc3754", "#57106e", "#5ec962"]
    else:
        out = ["red"]
    
    return out

def plot_model_line(model):
    """Plot the entrainment model."""
    settings = model.settings
    turtles = model.turtles
    
    colors = plot_model_colors(model)
    if not len(colors) == 1: colors = reorder(colors, settings.start_at)
    
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

def plot_model_line_1_2(
    x, y, x_title = "(A)", y_title = "(B)", legend_plot = "y", 
    legend_loc = "upper right", legend_fontsize = "small"
    ):
    colors = plot_model_colors(x)
    if not len(colors) == 1:
        x_colors = reorder(colors, x.settings.start_at)
        y_colors = reorder(colors, y.settings.start_at)
    else:
        x_colors, y_colors = colors, colors
    
    x_labels = [i.title() for i in list(x.turtles)]
    y_labels = [i.title() for i in list(y.turtles)]
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, [ax_x, ax_y] = plt.subplots(nrows = 1, ncols = 2)
    
    for i, j in enumerate(x.turtles):
        tau_i = [k["tau"] for k in np.array(x.turtles[j])]

        if (i == 0):
            color_i = "black"
            linewidth = 3
        else:
            color_i = x_colors[i - 1]
            linewidth = 1
        
        sns.kdeplot(tau_i, ax = ax_x, color = color_i, label = x_labels[i], 
                    linewidth = linewidth, warn_singular = False)
    
    for i, j in enumerate(y.turtles):
        tau_i = [k["tau"] for k in np.array(y.turtles[j])]
        
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
    
    colors = plot_model_colors(model)
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

def plot_model_violin_1_2(
    x, y, x_title = "(A)", y_title = "(B)", legend_plot = "y", 
    legend_loc = "upper right", legend_fontsize = "small"
    ):
    colors = plot_model_colors(x)
    if not len(colors) == 1:
        x_colors = reorder(colors, x.settings.start_at)
        y_colors = reorder(colors, y.settings.start_at)
    else:
        x_colors, y_colors = colors, colors
    
    x_data = []
    x_means = []
    
    for i in list(x.turtles):
        data_i = [j["tau"] for j in np.array(x.turtles[i])]
        x_data.append(data_i)
        x_means.append(np.mean(data_i))
    
    y_data = []
    y_means = []
    
    for i in list(y.turtles):
        data_i = [j["tau"] for j in np.array(y.turtles[i])]
        y_data.append(data_i)
        y_means.append(np.mean(data_i))
    
    x_labels = list(map(str.title, list(x.turtles)))
    x_labels_pos = np.arange(1, len(x.turtles) + 1)
    x_labels_pos = x_labels_pos[::-1]
    
    y_labels = list(map(str.title, list(y.turtles)))
    y_labels_pos = np.arange(1, len(y.turtles) + 1)
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

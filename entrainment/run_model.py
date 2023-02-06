import functools
import matplotlib.pyplot as plt
import numpy as np
from .get_labren_data import get_labren_data
from .plot_model import plot_model_line
from .utils import cli_progress_step, reorder
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
        labren_data = list(get_labren_data(labren_id, by = "month")["ts"])
        cycle = 12
    elif by == "season":
        labels = ["Summer", "Autumn", "Winter", "Spring"]
        labren_data = list(get_labren_data(labren_id, by = "season")["ts"])
        cycle = 4
    else:
        labels = ["Annual"]
        labren_data = [get_labren_data(labren_id, by = "year")["ts"]]
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
        exposure = list(out)[-1]
        lam = labren_data[i]
        turtles_i = entrain_turtles(
            out[exposure], turtles_0, lam, lam_c
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
        
        ## Group all turtles from exposure 'i' in 'turtles_i' (each repetition)
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
        
        ## Store the average turtles from exposure 'i' in 'out'
        turtles_i = []
        
        for a in range(len(tau_i)):
            turtles_i.append(
                Box(tau = tau_i[a], k = k_i[a], frozen_box = True)
                )
        
        out[i] = tuple(turtles_i)
        
    return Box(out, frozen_box = True)

import numpy as np
from .average_turtles import average_turtles
from .create_turtles import create_turtles
from .entrain import entrain_turtles
from .plot_model import plot_model
from ..labren import labren
from ..utils import reorder

# np.array(entrainment.labren.labren(72272)["ts"]).mean() ~ 4727.833
def run(
    n = 10**3, tau_range = (23.5, 24.6), tau_mean = 24.15, tau_sd = 0.2, 
    k_range = (0.001, 0.01), k_mean = 0.001, k_sd = 0.005, lam_c = 4727.833, 
    lam_c_tol = 1000, labren_id = 1, by = "season", n_cycles = 3, start_at = 0, 
    repetitions = 10 ** 2, plot = True
    ):
    turtles_0 = create_turtles(
        n, tau_range, tau_mean, tau_sd, k_range, k_mean, k_sd
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

    if plot == True: 
        plot_model(
            turtles, lam_c, labren_id, n_cycles, repetitions
            )
    
    return(turtles)

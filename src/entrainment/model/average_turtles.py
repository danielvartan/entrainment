import functools
import numpy as np

def average_turtles(turtles_n):
    """Average turtles/subjects values after n repetitions"""
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

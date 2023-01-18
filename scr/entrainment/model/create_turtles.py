import numpy as np

def create_turtles(n = 10 **2, tau_range = (23.5, 24.6), tau_mean = 24.15, 
                   tau_sd = 0.2, k_range = (0.001, 0.01), k_mean = 0.001, 
                   k_sd = 0.005):
    turtles = []
    
    for i in range(n):
        tau = np.random.normal(tau_mean, tau_sd)
        k = np.random.normal(k_mean, k_sd)
        
        if (tau < tau_range[0]): tau = tau_range[0]
        if (tau > tau_range[1]): tau = tau_range[1]
        if (k < k_range[0]): k = k_range[0]
        if (k > k_range[1]): k = k_range[1]
        
        turtles.append({"tau": tau, "k": k})
    
    return(turtles)

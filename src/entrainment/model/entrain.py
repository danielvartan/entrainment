import numpy as np

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

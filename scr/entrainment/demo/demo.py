import matplotlib.pyplot as plt
import numpy as np

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

# plot_exact(f_exact, lam_c = 5, k = 2, tau = 22, lam_0 = 0, lam_n = 10)
# plot_exact(f_exact, lam_c = 5, k = 2, tau = 26, lam_0 = 0, lam_n = 10)

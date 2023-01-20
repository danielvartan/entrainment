import matplotlib.pyplot as plt
import seaborn as sns

def plot_hypothesis(key, p_value, x, y, 
                    x_name = "Nascente do rio Ailã (Lat.: $5.272$)", 
                    y_name = "Arroio Chuí (Lat.: $- 33.752$)", 
                    lam_c = 4727.833, n_cycles = 3, repetitions = 100):
    n = len(x)

    title = ("Key = {key}, N = ${n}$, $\\lambda_c = {lam_c}$, " +\
             "Cycles = ${n_cycles}$, " +\
             "Repetitions = ${repetitions}$, p-value = {p_value}")\
             .format(key = key.title(), n = str(n), lam_c = str(lam_c), 
                     n_cycles = str(n_cycles), repetitions = str(repetitions), 
                     p_value = str(p_value))
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    sns.kdeplot(x, color = "red", label = x_name, linewidth = 1, 
            warn_singular = False)
    sns.kdeplot(y, color = "blue", label = y_name, linewidth = 1, 
                warn_singular = False)
    ax.set_xlabel("$\\tau$")
    ax.set_ylabel("Kernel Density Estimate (KDE)")
    ax.set_xlim(23.5, 24.6)
    ax.set_title(title, fontsize = 8)
    
    plt.legend(fontsize = 8)
    plt.show()
    
    return None

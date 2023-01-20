import matplotlib.pyplot as plt
import numpy as np

def f_exact(lam, lam_c, k, tau, tau_ref = 24):
    """Compute the (un)entrainment function.
    
    ``f_exact()`` computes the entrainment or unentrainment function of the
    ``entrainment`` model, but without its random error (:math:`E`) term
    (that's why it's called "exact").
    
    **Guidelines**
    
    The (un)entrainment function computation without its error (:math:`E`) term
    is given as  follows. Note that the (un)entrainment function is a logistic 
    function.
    
    .. math::
        \\text{f}(\\lambda, \\lambda_{c}, k, \\tau, \\tau_{\\text{ref}}) = 
        \\tau +  \\cfrac{\\tau_{\\text{ref}} - \\tau}{1 + e^{-k (\\lambda - 
        \\lambda_{c})}}
    
    Where:
    
    * :math:`\\lambda` = Global horizontal irradiation mean value present in the
      environment.
    * :math:`\\lambda_{c}` = Threshold/critial value of the global horizontal 
      irradiation, indicating the onset of the entrainment phenomenon.
    * :math:`k` = Exposure factor, indicating the subject's sensibility to
      entrainment. It gives the slope of the sigmoid.
    * :math:`\\tau` = The actual subject's circadian phenotype (period) given 
      in decimal hours.
    * :math:`\\tau_{\\text{ref}}` = Reference period to which the subject must
      entrain. This can be 24 hour light/dark period or the subject's own 
      endogenous period.
    
    .. note::
        You can see the complete entrainment funtion in 
        :func:`entrainment.model.entrain`.
    
    :param lam: Global horizontal irradiation mean value present in the 
        environment. See :func:`entrainment.labrem.labrem` to learn more.
    :type lam: int, float
    :param lam_c: Tthreshold/critial value of the global horizontal 
        irradiation, indicating the onset of the entrainment phenomenon.
    :type lam_c: int, float
    :param k: Exposure factor, indicating the subject's sensibility to
      entrainment.
    :type k: int, float
    :param tau: The actual subject's circadian phenotype (period) given in 
        decimal hours.
    :type tau: int, float
    :param tau_ref: (optional) reference period to which the subject must 
        entrain. This can be 24 hour light/dark period or the subject's own 
        endogenous period (default: ``24``).
    :type tau: int, float
    
    :return: The new period (:math:`\\tau`) value after the entrainment 
        dynamics.
    :rtype: float
    
    :Example:
    
    >>> lam = 1
    >>> lam_c = 5
    >>> k = 2
    >>> tau = 22
    >>> tau_ref = 24
    >>> entrainment.demo.f_exact(lam, lam_c, k, tau, tau_ref)
    22.000670700260933
    
    >>> lam = 1
    >>> lam_c = 5
    >>> k = 2
    >>> tau = 26
    >>> tau_ref = 24
    >>> entrainment.demo.f_exact(lam, lam_c, k, tau, tau_ref)
    25.99932929973906
    
    >>> lam = 1
    >>> lam_c = 5
    >>> k = 0.1
    >>> tau = 26
    >>> tau_ref = 10
    >>> entrainment.demo.f_exact(lam, lam_c, k, tau, tau_ref)
    19.579002561799232
    
    >>> lam = 1
    >>> lam_c = 5
    >>> k = 0.1
    >>> tau = 26
    >>> tau_ref = 35
    >>> entrainment.demo.f_exact(lam, lam_c, k, tau, tau_ref)
    29.611811058987932
    """
    logi_f = (tau_ref - tau) / (1 + np.exp(1) ** (- k * (lam - lam_c)))
    out = tau + logi_f

    return(out)

def exact(lam_c, k, tau, lam_0 = 0, lam_n = 10, h = 10 ** (- 3)):
    """Compute points in an interval of the (un)entrainment function."""
    lam_list, y_list = [lam_0], [f_exact(lam_0, lam_c, k, tau)]
    
    while lam_0 < lam_n:
        x_next = lam_0 + h
        y_next = f_exact(x_next, lam_c, k, tau)
        lam_0 = x_next
        lam_list.append(x_next)
        y_list.append(y_next)
    
    return [lam_list, y_list]

def plot_exact(lam_c, k, tau, lam_0 = 0, lam_n = 10, 
               h = 10 ** (- 3)):
    """Plot the (un)entrainment function in a given interval."""
    data = exact(lam_c, k, tau, lam_0, lam_n)

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

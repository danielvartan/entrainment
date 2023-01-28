import matplotlib.pyplot as plt
import numpy as np

def plot_dynamics(lam_c = 5, k = 2, tau = 26, tau_ref = 24, lam_0 = 0, 
                  lam_n = 10, h = 10**(- 3)):
    """Plot the (un)entrainment dynamic in a given interval.
    
    ``plot_dynamics()`` computes the entrainment or unentrainment function of 
    the ``entrainment`` model without its random error (:math:`E`) term.
    
    This function has already a set of default values configured for testing
    purposes. To see it in action, just run ``plot_dynamics()``.
    
    **Guidelines**
    
    The (un)entrainment function computation without its error (:math:`E`) term
    is given as  follows. Note that the (un)entrainment function is a logistic 
    function.
    
    .. math::
        \\text{f}(\\lambda, \\lambda_{c}, k, \\tau, \\tau_{\\text{ref}}) = 
        \\tau +  \\cfrac{\\tau_{\\text{ref}} - \\tau}{1 + e^{-k (\\lambda - 
        \\lambda_{c})}}
    
    Where:
    
    * :math:`\\lambda` = Global horizontal solar irradiation mean value present
      in the environment.
    * :math:`\\lambda_{c}` = Threshold/critial value of the global horizontal 
      solar irradiation, indicating the onset of the entrainment phenomenon.
    * :math:`k` = Exposure factor, indicating the subject's sensibility to
      entrainment. It gives the slope of the sigmoid.
    * :math:`\\tau` = The actual subject's circadian phenotype (period) given 
      in decimal hours.
    * :math:`\\tau_{\\text{ref}}` = Reference period to which the subject must
      entrain. This can be 24 hour light/dark period or the subject's own 
      endogenous period.
    
    :param lam_c: (optional) Threshold/critial value of the global horizontal 
        solar irradiation, indicating the onset of the entrainment phenomenon
        (default: ``5``).
    :type lam_c: int, float
    :param k: (optional) Exposure factor, indicating the subject's sensibility 
        to entrainment (default: ``2``).
    :type k: int, float
    :param tau: (optional) The actual subject's circadian phenotype (period) 
        given in decimal hours (default: ``26``).
    :type tau: int, float
    :param tau_ref: (optional) reference period to which the subject must 
        entrain. This can be 24 hour light/dark period or the subject's own 
        endogenous period (default: ``24``).
    :type tau: int, float
    :param lam_0: (optional) The start of the plot interval (default: ``0``).
    :type lam_0: int, float
    :param lam_n: (optional) The end of the plot interval (default: ``10``).
    :type lam_n: int, float
    :param h: (optional) The resolution of the function line. This value 
        indicates the interval between each data point 
        (default: ``10**(- 3))``).
    :type h: int, float
    
    :return: A ``None`` value. This function don't aim to return values.
    :rtype: None
    
    :Example:
    
    >>> entrainment.plot_dynamics(
        lam_c = 5, k = 2, tau = 22, tau_ref = 24, lam_0 = 0, lam_n = 10,
        h = 10**(- 3)
        )
    """
    data = exact(lam_c, k, tau, tau_ref, lam_0, lam_n)

    title = ("$\\lambda_c = {lam_c}$, $k = {k}$, $\\tau = {tau}$, " +\
             "$\\tau_{ref_latex} = {tau_ref}$")\
            .format(
                lam_c = lam_c, k = k, tau = tau, tau_ref = tau_ref,
                ref_latex = "{ref}"
                )

    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    ax.plot(data[0], data[1], "r-", linewidth = 1)
    ax.set_xlabel("$\\lambda$")
    ax.set_ylabel("$f(\\lambda, \\lambda_{c}, k, \\tau)$")
    ax.set_title(title, fontsize = 10)
    plt.show()
    
    return None

def f_exact(lam, lam_c, k, tau, tau_ref = 24):
    """Compute the exact (un)entrainment function."""
    logi_f = (tau_ref - tau) / (1 + np.exp(1) ** (- k * (lam - lam_c)))
    out = tau + logi_f

    return out

def exact(lam_c, k, tau, tau_ref = 24, lam_0 = 0, lam_n = 10, h = 10 ** (- 3)):
    """Compute the exact (un)entrainment function data points in a interval."""
    lam_list, y_list = [lam_0], [f_exact(lam_0, lam_c, k, tau, tau_ref)]
    
    while lam_0 < lam_n:
        x_next = lam_0 + h
        y_next = f_exact(x_next, lam_c, k, tau)
        lam_0 = x_next
        lam_list.append(x_next)
        y_list.append(y_next)
    
    return [lam_list, y_list]

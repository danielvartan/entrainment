import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from .get_labren_data import get_labren_data
from .utils import reorder

def plot_model_line(model):
    """Plot the entrainment model."""
    settings = model.settings
    turtles = model.turtles
    
    colors = plot_model_colors(model)
    if not len(colors) == 1: colors = reorder(colors, settings.start_at)
    labels = [i.title() for i in list(turtles)]
    
    title = ("N = ${n}$, $\\lambda_c = {lam_c}$, Latitude = ${lat}$, " +\
             "Cycles = ${n_cycles}$, Start = {start}, " +\
             "Repetitions = ${repetitions}$")\
             .format(
                 n = settings.n, lam_c = settings.lam_c, 
                 lat = get_labren_data(settings.labren_id)["lat"], 
                 n_cycles = settings.n_cycles, 
                 start = list(turtles)[1].title(), 
                 repetitions = settings.repetitions
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
    # 0.0625 | 0.125 | 0.25 | 0.5 | 1
    plt.subplots_adjust(
        left = 0.1375, bottom = 0.1625, right = 0.925, top = 0.88125, 
        wspace = None, hspace = None
        )
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
    
    title = ("N = ${n}$, $\\lambda_c = {lam_c}$, Cycles = ${n_cycles}$, " +\
             "Start = {start}, Repetitions = ${repetitions}$")\
             .format(
                 n = x.settings.n, lam_c = x.settings.lam_c,
                 n_cycles = x.settings.n_cycles, 
                 start = list(x.turtles)[1].title(), 
                 repetitions = x.settings.repetitions
                 )
    
    plt.rcParams.update({'font.size': 8})
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
    ax_x.set_title(x_title)
    ax_x.set_xlim(23.5, 24.6)
    ax_x.set_ylim(0, y_max)

    ax_y.set_xlabel("$\\tau$")
    ax_y.set_ylabel("")
    ax_y.set_title(y_title)
    ax_y.set_xlim(23.5, 24.6)
    ax_y.set_ylim(0, y_max)
    ax_y.get_yaxis().set_visible(False)
    
    if legend_plot == "x":
        ax_x.legend(loc = legend_loc, fontsize = legend_fontsize)
    else:
        ax_y.legend(loc = legend_loc, fontsize = legend_fontsize)
    
    plt.suptitle(title, fontsize = 8, y = 0.9375)
    # 0.0625 | 0.125 | 0.25 | 0.5 | 1
    plt.subplots_adjust(
        left = 0.125, bottom = 0.15, right = 0.9375, top = 0.83125, 
        wspace = None, hspace = None
        )
    plt.show()
    
    return None

def plot_model_violin(model):
    """Plot the entrainment model."""
    settings = model.settings
    turtles = model.turtles
    
    colors = plot_model_colors(model)
    colors = reorder_plot_model_colors(colors, settings.start_at)

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
                 lat = get_labren_data(settings.labren_id)["lat"], 
                 n_cycles = settings.n_cycles, 
                 start = list(turtles)[1].title(), 
                 repetitions = settings.repetitions
                 )
    
    labels_pos = np.arange(1, len(data) + 1)
    colors.insert(0, "#000000")

    ax_1_labels = list(map(str.title, list(turtles)))
    
    if model.settings.by == "year":
        ax_2_labels = [0] + [get_labren_data(
            model.settings.labren_id,
            by = model.settings.by)["ts"]
        ]
    else:
        ax_2_labels = [0] + list(get_labren_data(
            model.settings.labren_id, 
            by = model.settings.by)["ts"]
            )
    
    ax_2_labels = [int(i) for i in ax_2_labels]
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax_1 = plt.subplots()
    ax_2 = ax_1.twiny()
    
    ax_1_plot = ax_1.violinplot(
        data, vert = True, showextrema = False, showmeans = False
        )
    ax_1.scatter(
        labels_pos, means, marker = "o", color = "red", s = 10, zorder = 3
        )
    ax_2_plot = ax_2.violinplot(
        data, vert = True, showextrema = False, showmeans = False
        )
    
    for i, pc in enumerate(ax_1_plot["bodies"]):
        pc.set_facecolor(colors[i])
        pc.set_edgecolor('black')
    
    for i, pc in enumerate(ax_2_plot["bodies"]):
        pc.set_alpha(0)
    
    ax_1.set_xticks(labels_pos, labels = ax_1_labels)
    ax_1.set_title(title, fontsize = 8, y = 1.1875)
    ax_1.set_xlabel("Exposure")
    ax_1.set_ylabel("$\\tau$")
    ax_2.set_xticks(labels_pos, labels = ax_2_labels)
    ax_2.set_xlabel("$Wh / m^{2}.day$")
    
    # 0.0625 | 0.125 | 0.25 | 0.5 | 1
    plt.subplots_adjust(
        left = 0.1375, bottom = 0.16875, right = 0.95, top = 0.775, 
        wspace = None, hspace = None
        )
    plt.show()
    
    return None

def plot_model_violin_1_2(
    x, y, x_title = "(A)", y_title = "(B)", legend_plot = "y", 
    legend_loc = "upper right", legend_fontsize = "small"
    ):
    x_colors = plot_model_colors(x)
    x_colors = reorder_plot_model_colors(x_colors, x.settings.start_at)
    y_colors = plot_model_colors(y)
    y_colors = reorder_plot_model_colors(y_colors, y.settings.start_at)
    
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
    
    title = ("N = ${n}$, $\\lambda_c = {lam_c}$, Cycles = ${n_cycles}$, " +\
             "Start = {start}, Repetitions = ${repetitions}$")\
             .format(
                 n = x.settings.n, lam_c = x.settings.lam_c,
                 n_cycles = x.settings.n_cycles, 
                 start = list(x.turtles)[1].title(), 
                 repetitions = x.settings.repetitions
                 )
    
    x_labels_pos = np.arange(1, len(x.turtles) + 1)[::-1]
    ax_x_1_labels = list(map(str.title, list(x.turtles)))
    
    if x.settings.by == "year":
        ax_x_2_labels = [0] + [get_labren_data(
            x.settings.labren_id, 
            by = x.settings.by)["ts"]
            ]
    else:
        ax_x_2_labels = [0] + list(get_labren_data(
            x.settings.labren_id, 
            by = x.settings.by)["ts"]
            )
    
    ax_x_2_labels = [int(i) for i in ax_x_2_labels]
    
    y_labels_pos = np.arange(1, len(y.turtles) + 1)[::-1]
    ax_y_1_labels = list(map(str.title, list(y.turtles)))
    
    if y.settings.by == "year":
        ax_y_2_labels = [0] + [get_labren_data(
            y.settings.labren_id, 
            by = y.settings.by)["ts"]
            ]
    else:
        ax_y_2_labels = [0] + list(get_labren_data(
            y.settings.labren_id, 
            by = y.settings.by)["ts"]
            )
    
    ax_y_2_labels = [int(i) for i in ax_y_2_labels]
    
    x_colors = (["#000000"] + x_colors)[::-1]
    y_colors = (["#000000"] + y_colors)[::-1]
    
    x_data.reverse()
    y_data.reverse()
    
    plt.rcParams.update({'font.size': 8})
    plt.clf()
    
    fig, [ax_x_1, ax_y_1] = plt.subplots(nrows = 1, ncols = 2)
    ax_x_2, ax_y_2 = ax_x_1.twinx(), ax_y_1.twinx()

    ax_x_1_plot = ax_x_1.violinplot(
        x_data, vert = False, showextrema = False, showmeans = False
        )
    ax_x_1.scatter(
        x_means, x_labels_pos, marker = "o", color = "red", s = 10, 
        zorder = 3
        )
    ax_x_2_plot = ax_x_2.violinplot(
        x_data, vert = False, showextrema = False, showmeans = False
        )
    
    for i, pc in enumerate(ax_x_1_plot["bodies"]):
        pc.set_facecolor(x_colors[i])
        pc.set_edgecolor('black')
    
    for i, pc in enumerate(ax_x_2_plot["bodies"]):
        pc.set_alpha(0)
    
    ax_y_1_plot = ax_y_1.violinplot(
        y_data, vert = False, showextrema = False, showmeans = False
        )
    ax_y_1.scatter(
        y_means, y_labels_pos, marker = "o", color = "red", s = 10, zorder = 3
        )
    ax_y_2_plot = ax_y_2.violinplot(
        y_data, vert = False, showextrema = False, showmeans = False
        )
    
    for i, pc in enumerate(ax_y_1_plot["bodies"]):
        pc.set_facecolor(y_colors[i])
        pc.set_edgecolor('black')
    
    for i, pc in enumerate(ax_y_2_plot["bodies"]):
        pc.set_alpha(0)
    
    ax_x_1.set_yticks(x_labels_pos, labels = ax_x_1_labels)
    ax_x_1.set_ylabel("Exposure")
    ax_x_1.set_xlabel("$\\tau$")
    ax_x_1.set_title(x_title)
    ax_x_1.set_xlim(23.5, 24.6)
    ax_x_2.set_yticks(x_labels_pos, labels = ax_x_2_labels)
    
    ax_y_1.set_yticks(y_labels_pos, labels = ax_y_1_labels)
    ax_y_1.set_xlabel("$\\tau$")
    ax_y_1.set_title(y_title)
    ax_y_1.set_xlim(23.5, 24.6)
    ax_y_1.get_yaxis().set_visible(False)
    ax_y_2.set_yticks(y_labels_pos, labels = ax_y_2_labels)
    ax_y_2.set_ylabel("$Wh / m^{2}.day$", labelpad = 5)
    
    plt.suptitle(title, fontsize = 8, y = 0.9375)
    # 0.0625 | 0.125 | 0.25 | 0.5 | 1
    plt.subplots_adjust(
        left = 0.19375, bottom = 0.15625, right = 0.8625, top = 0.8375,
        wspace = 0.4, hspace = None
        )
    plt.show()
    
    return None

def plot_model_dynamics(
    tau = 26, k = 2, lam_c = 5, tau_ref = 24, lam_0 = 0, lam_n = 10, 
    h = 10**(- 3)
    ):
    """Plot the (un)entrainment dynamic in a given interval.
    
    ``plot_model_dynamics()`` computes the entrainment or unentrainment 
    function of the ``entrainment`` model without its random error (:math:`E`) 
    term.
    
    This function has already a set of default values configured for testing
    purposes. To see it in action, just run ``plot_model_dynamics()``.
    
    **Guidelines**
    
    The (un)entrainment function computation without its error (:math:`E`) term
    is given as  follows. Note that the (un)entrainment function is a logistic 
    function.
    
    .. math::
        \\text{f}(\\tau, k, \\lambda, \\lambda_{c}, \\tau_{\\text{ref}}) = 
        \\tau +  \\cfrac{\\tau_{\\text{ref}} - \\tau}{1 + e^{-k (\\lambda - 
        \\lambda_{c})}}
    
    Where:
    
    * :math:`\\tau` = The actual subject's circadian phenotype (period) given 
      in decimal hours.
    * :math:`k` = Exposure factor, indicating the subject's sensibility to
      entrainment. It gives the slope of the sigmoid.
    * :math:`\\lambda` = Global horizontal solar irradiation mean value present
      in the environment.
    * :math:`\\lambda_{c}` = Threshold/critial value of the global horizontal 
      solar irradiation, indicating the onset of the entrainment phenomenon.
    * :math:`\\tau_{\\text{ref}}` = Reference period to which the subject must
      entrain. This can be 24 hour light/dark period or the subject's own 
      endogenous period.
    
    :param tau: (optional) The actual subject's circadian phenotype (period) 
        given in decimal hours (default: ``26``).
    :type tau: int, float
    :param k: (optional) Exposure factor, indicating the subject's sensibility 
        to entrainment (default: ``2``).
    :type k: int, float
    :param lam_c: (optional) Threshold/critial value of the global horizontal 
        solar irradiation, indicating the onset of the entrainment phenomenon
        (default: ``5``).
    :type lam_c: int, float
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
    
    >>> entrainment.plot_model_dynamics(
        tau = 22, k = 2, lam_c = 5, tau_ref = 24, lam_0 = 0, lam_n = 10,
        h = 10**(- 3)
        )
    """
    data = get_exact_entrain(tau, k, lam_c, tau_ref, lam_0, lam_n)

    title = ("$\\tau = {tau}$, $k = {k}$, $\\lambda_c = {lam_c}$, " +\
             "$\\tau_{ref_latex} = {tau_ref}$")\
            .format(
                tau = tau, k = k, lam_c = lam_c, tau_ref = tau_ref,
                ref_latex = "{ref}"
                )

    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    ax.plot(data[0], data[1], "r-", linewidth = 1)
    ax.set_xlabel("$\\lambda$")
    ax.set_ylabel(
        "$f(\\tau, k, \\lambda, \\lambda_c, \\tau_{ref_latex}$)"\
        .format(ref_latex = "{ref}")
        )
    ax.set_title(title, fontsize = 10)
    
    # 0.0625 | 0.125 | 0.25 | 0.5 | 1
    plt.subplots_adjust(
        left = 0.15625, bottom = 0.16875, right = 0.95, top = 0.8875,
        wspace = None, hspace = None
        )
    plt.show()
    
    return None

def exact_entrain(tau, k, lam, lam_c, tau_ref = 24):
    """Compute the exact (un)entrainment function."""
    logi_f = (tau_ref - tau) / (1 + np.exp(1) ** (- k * (lam - lam_c)))
    out = tau + logi_f

    return out

def get_exact_entrain(
    tau, k, lam_c, tau_ref = 24, lam_0 = 0, lam_n = 10, h = 10 ** (- 3)
    ):
    """Compute the exact (un)entrainment function data points in a interval."""
    lam_list, y_list = [lam_0], [exact_entrain(tau, k, lam_0, lam_c, tau_ref)]
    
    while lam_0 < lam_n:
        x_next = lam_0 + h
        y_next = exact_entrain(tau, k, x_next, lam_c)
        lam_0 = x_next
        lam_list.append(x_next)
        y_list.append(y_next)
    
    return lam_list, y_list

def plot_model_colors(model):
    if model.settings.by == "month":
        out = sns.color_palette("tab10", 12)
    elif model.settings.by == "season":
        out = ["#f98e09", "#bc3754", "#57106e", "#5ec962"]
    else:
        out = ["red"]
    
    return out

def reorder_plot_model_colors(colors, start_at = 0):
    if not len(colors) == 1:
        colors = reorder(colors, start_at)
    
    return colors

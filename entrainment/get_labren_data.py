import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .utils import reorder
from box import Box
from importlib.resources import files
from scipy.interpolate import make_interp_spline

global_horizontal_means = (
    files("entrainment.data")
    .joinpath("global_horizontal_means.csv")
    )

def get_labren_data(id, by = "month", name = None):
    """Retrieve LABREN's global horizontal solar irradiation.
    
    :Example:
    
    >>> entrainment.get_labren_data(
        id = 1, by = "month", name = "Arroio Chuí (Lat.: - 33.752)"
        )
    
    >>> entrainment.get_labren_data(
        id = 1, by = "season", name = "Arroio Chuí (Lat.: - 33.752)"
        )
    
    >>> entrainment.get_labren_data(
        id = 1, by = "year", name = "Arroio Chuí (Lat.: - 33.752)"
        )
    """
    data = (
        pd.read_csv(filepath_or_buffer = global_horizontal_means, sep = ";")
        .rename(str.lower, axis = "columns")
        .loc[[id - 1]]
    )
    
    out = Box({"name": name})
    for i in list(data): out[i] = data.loc[id - 1, i]
    
    data = (
        data.iloc[:, 5:17]
        .transpose()
    )

    data.reset_index(inplace = True)
    data.columns = ["month", "x"]
    
    out["ts"] = list(data["x"])
    
    if by == "season":
        seasons = [
            ["Dec", "Jan", "Feb"], ["Mar", "Apr", "May"], ["Jun", "Jul", "Aug"], 
            ["Sep", "Oct", "Nov"]
            ]
        
        keys = ["name", "id", "country", "lon", "lat", "annual"]
        labels = ["Summer", "Autumn", "Winter", "Spring"]
        data = out
        out = {}
    
        for i, j in enumerate(data):
            if j in keys: out[j] = data[j]
        
        for i in range(4):
            mean = np.mean([data[i.lower()] for i in seasons[i]])
            out[labels[i].lower()] = mean
        
        out["ts"] = [out[i.lower()] for i in labels]
    
    if by == "year":
        keys = ["name", "id", "country", "lon", "lat", "annual"]
        data = out
        out = {}
        
        for i, j in enumerate(data):
            if j in keys: out[j] = data[j]
        
        out["ts"] = out["annual"]
    
    return Box(out, frozen_box = True)

def plot_labren_data(
    id_1 = 72272, id_2 = 1, by = "month", start_at = 0, label_1 = None, 
    label_2 = None
    ):
    """Plot and compare LABREN's global horizontal solar irradiation.
    
    :Example:
    
    >>> entrainment.plot_labren_data(
        id_1 = 72272, id_2 = 1, 
        label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
        label_2 = "Arroio Chuí (Lat.: $33.752$)",
        by = "month"
        )
    
    >>> entrainment.plot_labren_data(
        id_1 = 72272, id_2 = 1, 
        label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
        label_2 = "Arroio Chuí (Lat.: $33.752$)",
        by = "season"
        )
    """
    if by == "month":
        labels = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
            "Oct", "Nov", "Dec"
            ]
        x_label = "Month"
    elif by == "season":
        labels = ["Summer", "Autumn", "Winter", "Spring"]
        x_label = "Season"
    
    y_1 = list(get_labren_data(id_1, by = by)["ts"])
    y_2 = list(get_labren_data(id_2, by = by)["ts"])
    labels = reorder(labels, start_at)
    y_1, y_2 = reorder(y_1, start_at), reorder(y_2, start_at)
    fmt_1, fmt_2 = "r-", "b-"
    
    if label_1 == None: label_1 = "ID " + str(id_1)
    if label_2 == None: label_2 = "ID " + str(id_2)
    
    title = "Global Horizontal Solar Irradiation (Source: LABREN/INPE, 2017)"
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    fig, ax = plt.subplots()
    
    labels_0, y_1_0, y_2_0 = tuple(labels), tuple(y_1), tuple(y_2)
    labels.extend(labels_0)
    y_1.extend(y_1_0)
    y_2.extend(y_2_0)
    
    x = np.arange(0, len(labels))
    x_y_1_spline = make_interp_spline(x, y_1)
    x_y_2_spline = make_interp_spline(x, y_2)
    
    x = np.linspace(x.min(), x.max(), 500)
    y_1 = x_y_1_spline(x)
    y_2 = x_y_2_spline(x)
    
    ax.plot(x, y_1, fmt_1, label = label_1, linewidth = 1)
    ax.plot(x, y_2, fmt_2, label = label_2,  linewidth = 1)
    
    x_ticks_loc = ax.get_xticks().tolist()
    x_ticks_loc = [int(i) for i in x_ticks_loc]
    x_ticks_labels = [""] + [labels[i] for i in x_ticks_loc[1:-1]] + [""]
    ax.xaxis.set_major_locator(ticker.FixedLocator(x_ticks_loc))
    ax.set_xticklabels(x_ticks_labels)
    
    ax.set_xlabel(x_label)
    ax.set_ylabel("$Wh / m^{2}.day$")
    ax.set_title(title, fontsize = 10)
    
    plt.legend(fontsize = 8)
    # 0.0625 | 0.125 | 0.25 | 0.5 | 1
    plt.subplots_adjust(
        left = 0.15, bottom = 0.16875, right = 0.95, top = 0.8875, 
        wspace = None, hspace = None
        )
    plt.show()
    
    return None

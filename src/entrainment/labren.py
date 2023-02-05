import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from box import Box
from importlib.resources import files

global_horizontal_means = (
    files("entrainment.data")
    .joinpath("global_horizontal_means.csv")
    )

def labren(id, name = None, by = "month"):
    """Retrieve LABREN's global horizontal solar irradiation.
    
    :Example:
    
    >>> entrainment.labren(
        id = 1, name = "Arroio Chuí (Lat.: - 33.752)", by = "month"
        )
    
    >>> entrainment.labren(
        id = 1, name = "Arroio Chuí (Lat.: - 33.752)", by = "season"
        )
    
    >>> entrainment.labren(
        id = 1, name = "Arroio Chuí (Lat.: - 33.752)", by = "year"
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

def plot_labren(
    id_1 = 72272, id_2 = 1, label_1 = None, label_2 = None, by = "month"
    ):
    """Plot and compare LABREN's global horizontal solar irradiation.
    
    :Example:
    
    >>> entrainment.plot_labren(
        id_1 = 72272, id_2 = 1, 
        label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
        label_2 = "Arroio Chuí (Lat.: $33.752$)",
        by = "month"
        )
    
    >>> entrainment.plot_labren(
        id_1 = 72272, id_2 = 1, 
        label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
        label_2 = "Arroio Chuí (Lat.: $33.752$)",
        by = "season"
        )
    """
    if by == "month":
        x = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
            "Oct", "Nov", "Dec"
            ]
        
        y_1 = labren(id_1)["ts"]
        y_2 = labren(id_2)["ts"]
        fmt_1 = "r-"
        fmt_2 = "b-"
        x_label = "Month"
    elif by == "season":
        x = ["Summer", "Autumn", "Winter", "Spring"]
        y_1 = labren(id_1, by = "season")["ts"]
        y_2 = labren(id_2, by = "season")["ts"]
        fmt_1 = "r-"
        fmt_2 = "b-"
        x_label = "Season"
    else:
        x = ["Annual"]
        y_1 = labren(id_1, by = "year")["ts"]
        y_2 = labren(id_2, by = "year")["ts"]
        fmt_1 = "ro"
        fmt_2 = "bo"
        x_label = "Year"
    
    if label_1 == None: label_1 = "ID " + str(id_1)
    if label_2 == None: label_2 = "ID " + str(id_2)
    
    title = "Global Horizontal Solar Irradiation (Source: LABREN/INPE, 2017)"
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    ax.plot(x, y_1, fmt_1, label = label_1, linewidth = 1)
    ax.plot(x, y_2, fmt_2, label = label_2,  linewidth = 1)
    ax.set_xlabel(x_label)
    ax.set_ylabel("$Wh / m^{2}.day$")
    ax.set_title(title, fontsize = 10)
    
    plt.legend(fontsize = 8)
    plt.show()
    
    return None

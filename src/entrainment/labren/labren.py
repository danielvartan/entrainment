import numpy as np
import pandas as pd
from importlib.resources import files

global_horizontal_means = (
    files("entrainment.data")
    .joinpath("global_horizontal_means.csv")
    )

def labren(id, name = None, by = "month"):
    """Retrieve LABREN's global horizontal solar irradiation"""
    data = (
        pd.read_csv(filepath_or_buffer = global_horizontal_means, sep = ";")
        .rename(str.lower, axis = "columns")
        .loc[[id - 1]]
    )
    
    out = {"name": name}
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
    
    return out

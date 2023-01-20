import matplotlib.pyplot as plt
from .labren import labren

def plot_labren(id_1_index = 72272, id_2_index = 1,
                label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
                label_2 = "Arroio Chuí (Lat.: $- 33.752$)",
                by = "month"):
    """Plot LABREN's global horizontal solar irradiation"""
    if by == "month":
        x = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
            "Oct", "Nov", "Dec"
            ]
        
        y_1 = labren(id_1_index)["ts"]
        y_2 = labren(id_2_index)["ts"]
        fmt_1 = "r-"
        fmt_2 = "b-"
        xlabel = "Month"
    elif by == "season":
        x = ["Summer", "Autumn", "Winter", "Spring"]
        y_1 = labren(id_1_index, by = "season")["ts"]
        y_2 = labren(id_2_index, by = "season")["ts"]
        fmt_1 = "r-"
        fmt_2 = "b-"
        xlabel = "Season"
    else:
        x = ["Annual"]
        y_1 = labren(id_1_index, by = "year")["ts"]
        y_2 = labren(id_2_index, by = "year")["ts"]
        fmt_1 = "ro"
        fmt_2 = "bo"
        xlabel = "Year"
    
    title = "Global Horizontal Solar Irradiation (Source: LABREN/INPE, 2017)"
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    ax.plot(x, y_1, fmt_1, label = label_1, linewidth = 1)
    ax.plot(x, y_2, fmt_2, label = label_2,  linewidth = 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("$Wh / m^{2}.day$")
    ax.set_title(title, fontsize = 10)
    
    plt.legend(fontsize = 8)
    plt.show()
    
    return None

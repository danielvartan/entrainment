import matplotlib.pyplot as plt

def plot_labren(id_1_index = 72272, id_2_index = 1,
                label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
                label_2 = "Arroio Chuí (Lat.: $- 33.752$)",
                by = "month"):
    if (by == "month"):
        x = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
            "Oct", "Nov", "Dec"
            ]
        
        y_1 = labren(id_1_index)["ts"]
        y_2 = labren(id_2_index)["ts"]
        xlabel = "Month"
    else:
        x = ["Summer", "Autumn", "Winter", "Spring"]
        y_1 = labren(id_1_index, by = "season")["ts"]
        y_2 = labren(id_2_index, by = "season")["ts"]
        xlabel = "Season"
    
    title = "Global Horizontal Solar Irradiation (Source: LABREN/INPE, 2017)"
    
    plt.rcParams.update({'font.size': 10})
    plt.clf()
    
    fig, ax = plt.subplots()
    ax.plot(x, y_1, "r-", label = label_1, linewidth = 1)
    ax.plot(x, y_2, "b-", label = label_2,  linewidth = 1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("$Wh / m^{2}.day$")
    ax.set_title(title, fontsize = 10)
    
    plt.legend(fontsize = 8)
    plt.show()

# plot_labren(
#     id_1_index = 72272, id_2_index = 1,
#     label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
#     label_2 = "Arroio Chuí (Lat.: $- 33.752$)",
#     by = "month"
#     )

# plot_labren(
#     id_1_index = 72272, id_2_index = 1,
#     label_1 = "Nascente do rio Ailã (Lat.: $5.272$)",
#     label_2 = "Arroio Chuí (Lat.: $- 33.752$)",
#     by = "season"
#     )

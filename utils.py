import matplotlib.pyplot as plt

def bar_graph(df, column_names, title="Bar Graph", xlabel="Index", ylabel="Values"):
    df[column_names].plot(kind='bar')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
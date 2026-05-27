import matplotlib.pyplot as plt

def make_graph(data):
    plt.figure()
    plt.plot(data)
    plt.title("Crash History")
    path = "graph.png"
    plt.savefig(path)
    plt.close()
    return path

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def init_graph():
    G = nx.read_edgelist('/Users/reece/Documents/MTHE493/MTHE-493-Stochastic-Control/app/utils/hospital_graph.txt', nodetype=int, data=(('weight',float),), create_using=nx.Graph())

    return G

def draw_graph(G):

    labels = nx.get_edge_attributes(G,'weight')

    pos = nx.spring_layout(G, k=2)

    nx.draw(G, pos, with_labels=True)

    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

    plt.show()

def main():
    G = init_graph()

    #nx.draw(G, with_labels=True)
    labels = nx.get_edge_attributes(G,'weight')

    pos = nx.spring_layout(G, k=2)

    nx.draw(G, pos, with_labels=True)

    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

    plt.show()

if __name__ == "__main__":
    main()
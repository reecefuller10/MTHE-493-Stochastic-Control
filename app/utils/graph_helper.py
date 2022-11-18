import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#returns a list of all the nodes adjacent to the input node
def get_neighbours(G,node):

    #initialize list to store neighbours
    neighbours_list = []

    #iterate through neighbours and add them to the list (this is necessary because the G.neighbors() object is weird)
    for n in G.neighbors(node):
        neighbours_list.append(n)
    
    #print(neighbours_list)

    return neighbours_list

#read graph from text file
def init_graph():

    #change to /your/path/here/MTHE-493-Stochastic-Control/app/utils/hospital_graph.txt
    #G = nx.read_edgelist('C:\Users\Gmack\MTHE-493-Stochastic-Control\app\utils\hospital_graph.txt', nodetype=int, data=(('weight',float),), create_using=nx.Graph())
    G = nx.read_edgelist('/Users/reece/Documents/MTHE493/MTHE-493-Stochastic-Control/app/utils/hospital_graph.txt', nodetype=int, data=(('weight',float),), create_using=nx.Graph())
    return G

#Pretty picture
def draw_graph(G):

    labels = nx.get_edge_attributes(G,'weight')

    pos = nx.spring_layout(G, k=2)

    nx.draw(G, pos, with_labels=True)

    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

    plt.show()

#for testing
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
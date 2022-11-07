import networkx as nx
import numpy as np
import pandas as pd
import random
from enviroment_helper import *
from graph_helper import *



def move_nurse(G, hospital_dict, from_node, to_node):

    if (G.has_node(from_node) == 0):
        print("ERROR a Hospital with ID " + str(from_node) + " does not exist.")
        return 0

    if (G.has_node(to_node) == 0):
        print("ERROR a Hospital with ID " + str(to_node) + " does not exist.")
        return 0

    from_hospital = hospital_dict[from_node]
    to_hospital = hospital_dict[to_node]

    if(from_hospital.num_nurses == 0):
        print("ERROR no nurses available to transfer from hospital with ID " + str(from_hospital))
        return 0
    
    if(to_hospital.num_nurses == to_hospital.nurse_capacity):
        print("ERROR hospital with ID" + str(to_node) + "is already at full capacity (" + str(to_hospital.nurse_capacity) + ")")
        return 0

    num_from_0 = from_hospital.num_nurses
    num_to_0 = to_hospital.num_nurses

    (hospital_dict[from_node]).num_nurses = num_from_0 - 1
    (hospital_dict[to_node]).num_nurses = num_to_0 + 1    

    return hospital_dict

def get_min_distance(G, from_node, to_node):

    distance = nx.dijkstra_path_length(G,from_node,to_node)

    return distance

if __name__ == "__main__":
    main()
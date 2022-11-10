import networkx as nx
import numpy as np
import pandas as pd
import random
from enviroment_helper import *
from graph_helper import *

#Function to transfer nurse to another hospital (Will transfer even if hospitals are not connected)
def move_nurse(G, hospital_dict, from_node, to_node):

    #--------------------------------------Fail cases--------------------------------------
    if (G.has_node(from_node) == 0):
        print("ERROR a Hospital with ID " + str(from_node) + " does not exist.")
        return 0

    if (G.has_node(to_node) == 0):
        print("ERROR a Hospital with ID " + str(to_node) + " does not exist.")
        return 0
    #--------------------------------------Fail cases--------------------------------------

    #Isolate hospital objects from dictionary
    from_hospital = hospital_dict[from_node]
    to_hospital = hospital_dict[to_node]

    #--------------------------------------Fail cases--------------------------------------
    if(from_hospital.num_nurses == 0):
        print("ERROR no nurses available to transfer from hospital with ID " + str(from_hospital))
        return hospital_dict
    
    if(to_hospital.num_nurses == to_hospital.nurse_capacity):
        print("ERROR hospital with ID" + str(to_node) + "is already at full capacity (" + str(to_hospital.nurse_capacity) + ")")
        return hospital_dict
    #--------------------------------------Fail cases--------------------------------------

    #Isolate hospital attributes
    num_from_0 = from_hospital.num_nurses
    num_to_0 = to_hospital.num_nurses

    #Update values by removing 1 and adding 1
    (hospital_dict[from_node]).num_nurses = num_from_0 - 1
    (hospital_dict[to_node]).num_nurses = num_to_0 + 1    

    #Return updated dictionary
    return hospital_dict

#Uses Dijkstra's algorithm (shortest path algorithm) to find the minimum distance between 2 hospitals
def get_min_distance(G, from_node, to_node):

    #compute distance
    distance = nx.dijkstra_path_length(G,from_node,to_node)

    #return distane value
    return distance

def get_neighbours_nurses(G,node,hospital_dict):

    #Get list of neighbours
    neighbours = list(G.neighbors(node))
    neighbours_dict = {}

    for i in neighbours:
        neighbours_dict[i] = hospital_dict[i].num_nurses
        print(neighbours_dict[i])


    #Return list of nurses
    return neighbours_dict


if __name__ == "__main__":
    main()
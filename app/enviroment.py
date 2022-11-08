import networkx as nx
import numpy as np
import pandas as pd
import random
import sys

#Update with the path to utils folder on your computer
sys.path.append('/Users/reece/Documents/MTHE493/MTHE-493-Stochastic-Control/app/utils')

#debug system path
#print(sys.path)

#Import functions from helper files
from utils.enviroment_helper import *
from utils.transmission_helper import *
from utils.graph_helper import *

def evolve(hospital_dict,pop_dict):

    for ID in hospital_dict.keys():
        hospital_dict = drift_patients(ID,hospital_dict,pop_dict[ID],0.25,0.02)


    return hospital_dict


def main():

    #create a dictionary storing objects that represent each hospital, indexed by ID
    hospital_dict = create_data_dict(num= 5) 

    pop_dict = create_population_dict(hospital_dict.keys())

    print(pop_dict)

    end_time = 5

    #Initialize graph structure
    G = init_graph()

    #loop for the system to evolve
    #demo code: prints the evolution of hospital with ID = 3 over 5 time steps
    t = 0
    while(1):
        print("-------------------time = " + str(t) + "-------------------")
        hospital_dict = evolve(hospital_dict= hospital_dict, pop_dict= pop_dict)
        print_single_hospital_data(ID= 3, hospital_dict= hospital_dict)

        t += 1
        if t == end_time : break

    draw_graph(G)


    #print_hospital_data(hospital_dict)


if __name__ == "__main__":
    main()




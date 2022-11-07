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


def main():

    #create a dictionary storing objects that represent each hospital, indexed by ID
    hospital_dict = create_data_dict(5) 

    #Initialize graph structure
    G = init_graph()

    print_hospital_data(hospital_dict)

    set_hospital_attribute(hospital_dict = hospital_dict, ID = 1, attribute = 'num_patients', new_val = 30)

    hospital_dict = move_nurse(G, hospital_dict, 2, 3)

    distance = get_min_distance(G, 2, 3)

    get_neighbours(G,2)

    drift_patients(2, hospital_dict,100,0.5,0.02)

    print_hospital_data(hospital_dict)

    print('d = ' + str(distance))

    draw_graph(G)



if __name__ == "__main__":
    main()




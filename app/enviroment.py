import networkx as nx
import numpy as np
import pandas as pd
import random
import sys

sys.path.append('/Users/reece/Documents/MTHE493/MTHE-493-Stochastic-Control/app/utils')
print(sys.path)
from utils.enviroment_helper import *
from utils.transmission_helper import *
from utils.graph_helper import *


#ID, nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio

def main():
    print(sys.path)
    
    hospital_dict = create_data_dict(5)
    G = init_graph()
    print_hospital_data(hospital_dict)

    update_hospital_attribute(hospital_dict = hospital_dict, ID = 1, attribute = 'num_patients', new_val = 30)

    hospital_dict = move_nurse(G, hospital_dict, 2, 3)

    distance = get_min_distance(G, 2, 3)

    update_patients(2, hospital_dict,100,0.5,0.02)

    print_hospital_data(hospital_dict)

    print('d = ' + str(distance))

    draw_graph(G)



if __name__ == "__main__":
    main()




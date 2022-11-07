import networkx as nx
import numpy as np
import pandas as pd
import random
from utils.enviroment_helper import *
from utils.transmission_helper import *
from utils.graph_helper import *

#ID, nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio

def main():
    hospital_dict = create_data_dict(5)
    G = init_graph()
    print_hospital_data(hospital_dict)

    update_hospital_attribute(hospital_dict = hospital_dict, ID = 1, attribute = 'num_patients', new_val = 30)

    move_nurse(G, hospital_dict, 0, 1)

    draw_graph(G)



if __name__ == "__main__":
    main()




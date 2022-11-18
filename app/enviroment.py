import networkx as nx
import numpy as np
import pandas as pd
import random
import sys

#Change this path to /you/path/here/MTHE-493-Stochastic-Control/app/utils
sys.path.append(r'C:\Users\Gmack\MTHE-493-Stochastic-Control\app\utils')

#print(sys.path)

#Import functions from helper files
from utils.enviroment_helper import *
from utils.transmission_helper import *
from utils.graph_helper import *
from utils.control_system_helper import *

def evolve(hospital_dict,time_step):

    #call drift patients on every hospital
    for ID in hospital_dict.keys():
        hospital_dict = drift_patients(ID,hospital_dict,hospital_dict[ID].pop_susceptible,hospital_dict[ID].pop_infected,hospital_dict[ID].num_patients,hospital_dict[ID].pop_recovered,time_step)

    #def drift_patients(ID, hospital_dict, pop_susceptible, pop_infected, pop_hospitalized, pop_recovered, time_step):
    

    return hospital_dict


def main():

    #create a dictionary storing objects that represent each hospital, indexed by ID
    hospital_dict = create_data_dict(num= 5) 

    #create a dictionary storing the populations for each hospital, indexed by ID
    pop_dict = create_population_dict(hospital_dict.keys())

    #initialize a dictionary to represent the action space, indexed by time step
    action_dict = create_action_dict(hospital_dict)

    #Initialize graph structure
    G = init_graph()
    

    #loop for the system to evolve
    #demo code: prints the evolution of hospital with ID = 3 over 5 time steps
    #           2 actions are taken at time 2 and time 4 as a demonstration

    end_time = 5

    t = 0
    while(1):

        #Dynamically add empty control values for each hospital, at time step
        action_dict = increment_action_dict(hospital_dict, action_dict, t)

        print("-------------------State data at time = " + str(t) + "-------------------")

        #demo code to post actions at time 2 and time 4
        if t == 2:
            action_dict = post_action(3, 2, 5, G, hospital_dict, action_dict, t)

        if t == 4:
            action_dict = post_action(2, 3, 4, G, hospital_dict, action_dict, t)

        #resolve actions taken at the previous time step
        hospital_dict = resolve_action(hospital_dict, action_dict, t)

        #print data
        print_single_hospital_data(ID= 3, hospital_dict= hospital_dict)

        #print posted actions
        print('actions posted' + str(t), action_dict[t])

        #transition the sytstem to the next state
        hospital_dict = evolve(hospital_dict= hospital_dict, time_step= t)

        t += 1

        #+1 since time is incrememented after state transition
        if t == end_time + 1 : break

    #draw_graph(G)


    #print_hospital_data(hospital_dict)


if __name__ == "__main__":
    main()




import networkx as nx
import numpy as np
import pandas as pd
import random
import sys

#Change this path to /you/path/here/MTHE-493-Stochastic-Control/app/utils
#sys.path.append(r'C:\Users\Gmack\MTHE-493-Stochastic-Control\app\utils')
sys.path.append('/Users/reece/Documents/MTHE493/MTHE-493-Stochastic-Control/app/utils')

#print(sys.path)

#Import functions from helper files
from utils.enviroment_helper import *
from utils.transmission_helper import *
from utils.graph_helper import *
from utils.control_system_helper import *
from Q_learning import *

def evolve(hospital_dict,time_step):

    #call drift patients on every hospital
    for ID in hospital_dict.keys():
        hospital_dict = drift_patients(ID,hospital_dict,hospital_dict[ID].pop_susceptible,hospital_dict[ID].pop_infected,hospital_dict[ID].num_patients,hospital_dict[ID].pop_recovered,time_step)

    #get all care ratios
    care_array = []
    for keys in hospital_dict.keys():
        care_array.append(hospital_dict[keys].care_ratio)
    
    #test stuff for reward
    num_bad = 0
    for val in care_array:
        if val <= 0.5:
            num_bad += 1


    reward = 0

    #a poorly implemented way to stop divide by 0 errors
    for ID in hospital_dict.keys():
        if (hospital_dict[ID].care_ratio == 'inf'):
            hospital_dict[ID].care_ratio = 0 
        
        if (hospital_dict[ID].care_ratio == 'nan'):
            hospital_dict[ID].care_ratio = -1
        
        #temporary reward function
        reward += hospital_dict[ID].care_ratio
    
    
    

    return hospital_dict, reward

def main():

    #create a dictionary storing objects that represent each hospital, indexed by ID
    hospital_dict = create_data_dict(num= 5) 

    #create a dictionary storing the populations for each hospital, indexed by ID
    pop_dict = create_population_dict(hospital_dict.keys())

    #initialize a dictionary to represent the action space, indexed by time step
    action_dict = create_action_dict(hospital_dict)

    create_state_space(hospital_dict)

    #create_action_space(hospital_dict)

    #create_action_space(hospital_dict)


    
    #Initialize graph structure
    G = init_graph()
    
    #initialize Q stuff
    Q = Q_table(learning_rate=0.1, discount_factor=0.9, gamma=0.9)
    Q.initalize_actions(hospital_dict)
    Q.initialize_states(hospital_dict)
    Q.initialize_table()


    #number of episodes
    end_time = 1000
    
    #evolution loop
    t = 0

    picture = []
    while(1):

        #Dynamically add empty control values for each hospital, at time step
        action_dict = increment_action_dict(hospital_dict, action_dict, t+1)

        print("-------------------State data at time = " + str(t) + "-------------------")

        #demo code to post actions at time 2 and time 4

        #get initial state
        state = get_state(hospital_dict)
        print('initial state = ',state)

        #get ID of initial state
        state_ID = get_state_ID(state,Q)
        print('initial state id = ',state_ID)
        
        #debugging check
        print('state from ID = ',Q.states[state_ID])

        #have the agent choose an action
        action, action_ID = Q.choose_action(state_ID, hospital_dict)
        print('action = ',action)
        print('found action id = ',action_ID)

        #debugging check
        print('action from ID = ',Q.actions[action_ID])

        #post the action to the action dict
        action_dict[t] = post_action(action, action_dict, t)

        #resolve actions taken at the previous time step
        hospital_dict = resolve_action(hospital_dict, action_dict, t)

        #print posted actions
        print('action posted to dict = ', action_dict[t])

        #transition the sytstem to the next state and get the reward
        hospital_dict,reward = evolve(hospital_dict= hospital_dict, time_step= t)

        #get the new state
        next_state = get_state(hospital_dict)

        #get the new state ID
        next_state_ID = get_state_ID(next_state,Q)

        #debugging check
        print('next state ID = ',next_state_ID)
        print('next state = ',next_state)

        print('Reward = ', reward)
        print_care_ratios(hospital_dict)

        #update the Q table
        Q.learn(state_ID, action_ID, reward, next_state_ID)

        #this is to graph the average care ratio over time after episodes are finished. I named it picture because I'm lazy (Copilot wrote this line lol)
        picture.append(get_average_care_ratio(hospital_dict))
        

        t += 1

        #+1 since time is incrememented after state transition
        if t == end_time + 1 : break

    graph_care_ratio(picture)

    #draw_graph(G)

    #print_hospital_data(hospital_dict)
    

if __name__ == "__main__":
    main()


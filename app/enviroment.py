import networkx as nx
import numpy as np
import pandas as pd
import random
import sys
import time

#Change this path to /you/path/here/MTHE-493-Stochastic-Control/app/utils
#sys.path.append(r'C:\Users\Gmack\MTHE-493-Stochastic-Control\app\utils')
sys.path.append('/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/app/utils')

#print(sys.path)

#Import functions from helper files
from utils.enviroment_helper import *
from utils.transmission_helper import *
from utils.graph_helper import *
from utils.control_system_helper import *
from Q_learning import *
import pickle

def evolve(hospital_dict,time_step, action):

    #call drift patients on every hospital
    
    for ID in hospital_dict.keys():
        
        hospital_dict = drift_patients(ID,hospital_dict,hospital_dict[ID].pop_susceptible,hospital_dict[ID].pop_infected,hospital_dict[ID].num_patients,hospital_dict[ID].pop_recovered,time_step)
    '''
    for i in hospital_dict.keys():
        print(f"pop_infected = {hospital_dict[i].pop_infected}")
        print(f"pop_recovered = {hospital_dict[i].pop_recovered}")
        print(f"pop_susceptible = {hospital_dict[i].pop_susceptible}")
        print(f"num_patients = {hospital_dict[i].num_patients}")
    '''

    #get all care ratios
    care_array = []
    for keys in hospital_dict.keys():
        care_array.append(hospital_dict[keys].care_ratio)
    
    #depricate
    num_bad = 0
    for val in care_array:
        if val <= 0.5:
            num_bad += 1
            

    cost = 0

    #a poorly implemented way to stop divide by 0 errors (might not be needed anymore)
    for ID in hospital_dict.keys():
        if hospital_dict[ID].num_nurses != 0:
        #temporary reward function
            care_r = hospital_dict[ID].num_patients/hospital_dict[ID].num_nurses_unquantized
            if care_r <=4 :
                cost += (1/16)*np.exp(care_r)
            elif care_r > 4 and care_r < 8:
                cost += 100
            if action[ID - 1] < 0 :
                cost += action[ID-1]
            
        else:
            cost += 100
    
    #print(f"cost = {cost}")
    
    return hospital_dict, cost

    
def main():

    #create a dictionary storing objects that represent each hospital, indexed by ID
    hospital_dict = create_data_dict(num= 2) 

    #initialize a dictionary to represent the action space, indexed by time step
    #action_dict = create_action_dict(hospital_dict)

    #Initialize graph structure
    G = init_graph()
    
    tik = time.time()

    #initialize Q stuff
    Q = Q_table(learning_rate=0.1, discount_factor=0.9, gamma=0.9)

    Q.initalize_actions(hospital_dict)
    Q.initialize_states(hospital_dict)
    Q.initialize_table()
    
    

    print(f"table dimensions = {np.shape(Q.table)}")
    
    print()

    tok = time.time()
    #print(f"Q init time = {tok-tik}")


    #print(f"Q.states = {Q.states}")

    #print(f"partitioned states = {Q.partitioned_states[22][0].state_values}")

    #test_state_id = get_state_ID([4,0,0,4,6],Q)

    #print(f"state from id = {Q.states[test_state_id]}")

    #print(f"Q.table.shape() = {np.shape(Q.table)}")


    #number of epis
    # odes
    end_time = 2500
    
    #evolution loop
    t = 0

    picture = []
    t1 = time.time()

    quantized = True
    optimal = False
    no_Control = True

    saved_states = []

    care_ar = []

    reset_mod = [0,0]
    modulo_vals = [300 + random.randint(-50,50),300 + random.randint(-50,50)]

    initial_total_pop = hospital_dict[1].total_population() + hospital_dict[2].total_population()


    if optimal == True:
        Q.table = np.load('/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/Q_table.npy')
        Q.remove_bad_actions()
    while(1):

        #Dynamically add empty control values for each hospital, at time step
        #action_dict = increment_action_dict(hospital_dict, action_dict, t+1)

        #print("-------------------State data at time = " + str(t) + "-------------------")
        if t%10000 == 0:
            print('time = ',t)
        T1 = time.time()


        tic = time.time()
        #get initial state
        if (quantized == False):
            state = get_state(hospital_dict)
        if (quantized == True):
            state = get_state(hospital_dict)
            saved_states.append(get_state(hospital_dict))
            #print(f"state = {state}")
            state = quantize_state(hospital_dict,state, Q)
            #print(f"quantized state = {state}")

        care_ar.append(hospital_dict[1].num_patients/hospital_dict[1].num_nurses_unquantized)
        care_ar.append(hospital_dict[2].num_patients/hospital_dict[2].num_nurses_unquantized)

        #print('initial state = ',state)
        tok = time.time()
        #print('time to get state = ',tok-tic)

        #get ID of initial state
        tik = time.time()
        state_ID = get_state_ID(state,Q)

        #print(f'found state from id = {Q.states[state_ID]}')
        #print(f"state ID = {state_ID}")
        #print('initial state id = ',state_ID)
        tok = time.time()
        #print('time to get state id = ',tok-tic)
        
        tik = time.time()
        #have the agent choose an action
        if optimal == False:
            action, action_ID = Q.choose_action(state_ID, hospital_dict,t)
        if optimal == True:
            action, action_ID = Q.choose_optimal_action(state_ID, hospital_dict,t)
            #print(f"Q-value = {Q.table[state_ID,action_ID]}")
        if no_Control == True:
            action,action_ID = [0,0],0


        #print('action = ',action)
        #print('found action id = ',action_ID)
        #debugging check
        tok = time.time()
        #print('time to choose action = ',tok-tik)
        
        tik = time.time()
        #post the action to the action dict
        hospital_dict = take_action(action, hospital_dict, t)
        tok = time.time()
        #print('time to take action = ',tok-tik)

        #print_hospital_data(hospital_dict)

        #transition the sytstem to the next state and get the reward
        tik = time.time()
        hospital_dict,reward = evolve(hospital_dict= hospital_dict, time_step= t, action = action)
        tok = time.time()
        #print('time to evolve = ',tok-tik)

        #get the new state
        tik = time.time()
        if(quantized == False):
            next_state = get_state(hospital_dict)
        if(quantized == True):
            next_state = get_state(hospital_dict)
            next_state = quantize_state(hospital_dict,next_state, Q)
        tok = time.time()
        #print('time to get next state = ',tok-tik)

        #get the new state ID
        tik = time.time()
        next_state_ID = get_state_ID(next_state,Q)
        tok = time.time()
        #print('time to get next state id = ',tok-tik)

        #debugging check
        #print('next state ID = ',next_state_ID)
        #print('next state = ',next_state)

        #print('Reward = ', reward)
        #print_care_ratios(hospital_dict)

        #update the Q table
        tik = time.time()
        if optimal == False:
            pass
            #Q.learn(state_ID, action_ID, reward, next_state_ID)
        tok = time.time()
        #print('time to learn = ',tok-tik)
        T2 = time.time()
        #print("total time = ",T2 - T1)

        #this is to graph the average care ratio over time after episodes are finished. I named it picture because I'm lazy (Copilot wrote this line lol)
        #picture.append(get_average_care_ratio(hospital_dict))
        
        if t % 10000 == 0:
            np.save("/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/Q_table.npy",Q.table)
            np.save("/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/actions.npy",Q.actions)
            np.save("/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/states.npy",Q.states)

        t += 1

        #+1 since time is incrememented after state transition
        if t == end_time + 1 : break

    t2 = time.time()
    print('time = ',t2-t1)

    total_Q_entries = Q.table.shape[0]*Q.table.shape[1]
    print(f"total_Q_entries = {total_Q_entries}")
    print(f"num_Q_entries_filled = {Q.num_Q_values_updated}")
    print(f"percent Q entries filled = {Q.num_Q_values_updated/total_Q_entries * 100} %")

    print("saving Q table...")
    Q.save_table()
    print("Q table saved")

    print(f"min care ratio = {np.min(care_ar)}")
    print(f"max care ratio = {np.max(care_ar)}")
    print(f'average care ratio = {np.mean(care_ar)}')
    print(f"standard deviation of care ratio = {np.std(care_ar)}")

    print(f'initial_total_pop = {initial_total_pop}')
    print(f'final_total_pop = {hospital_dict[1].total_population() + hospital_dict[2].total_population()}')

    plot_results(saved_states)

    np.save("/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/saved_states.npy",np.asarray(saved_states))

    #graph_care_ratio(picture)

    #draw_graph(G)

    #print_hospital_data(hospital_dict)
    

if __name__ == "__main__":
    main()


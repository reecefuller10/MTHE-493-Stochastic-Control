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




def generate_losses(hospital_dict,ID):
    '''
    randomly generate the number of deaths that occur in the overflow queue based on n independent binomial trials with parameter p
    where n is the number of patients in the overflow queue for 14 or more days, and p is the probability of death.
    '''
    
    p = 0.1
    '''#print(f'array before deaths = {hospital_dict[ID].overflow_array}')
    count = np.random.binomial(hospital_dict[ID].overflow_array[0],p)
    #print(f'num dead = {count}')
    hospital_dict[ID].overflow_array[0] -= count
    #print(f'array after deaths = {hospital_dict[ID].overflow_array}')
    hospital_dict[ID].num_deaths += count
    hospital_dict[ID].deaths_delta = count'''
    count = np.random.binomial(hospital_dict[ID].total_overflow,p)
    #print(f'num dead = {count}')
    hospital_dict[ID].total_overflow -= count
    #print(f'array after deaths = {hospital_dict[ID].overflow_array}')
    hospital_dict[ID].num_deaths += count
    hospital_dict[ID].deaths_delta = count
    print(f'new deaths = {hospital_dict[ID].deaths_delta}')

    return hospital_dict

def queue_evolve_v2(ID, hospital_dict,time_step, lam, mewGood, mewBad, mewMid):
    '''
    2nd version of the queuing evolution. This version has a queue to track the number of patients who were not admitted to the hospital.
    Each time step, if there are people who were waiting for 14 or more days, they have a probability of dying given by n independent binomial distributions
    with paramter p (see generate_losses()). This version prioritizes those in the overflow queue over those who arrived during the current time step.
    '''

    hospital_dict = generate_losses(hospital_dict, ID)
    

    QoC = hospital_dict[ID].num_patients/(hospital_dict[ID].num_nurses * 6)
    
    #calculate departures
    '''
    if QoC < 2:
        departures = np.random.poisson(mewGood)
    elif QoC >= 2 and QoC <= 4:
        departures = np.random.poisson(mewMid)
    else:
        departures = np.random.poisson(mewBad)
    '''

    if QoC < 6:
        departures = np.random.poisson(6.25-((0.35)/6)*QoC)
    else:
        departures = np.random.poisson(mewBad)

    #if ID == 1: print(f'departures = {departures}')

    #update number of patients in hospital based on departures
    hospital_dict[ID].num_patients = max(0, hospital_dict[ID].num_patients - departures)

    #bring in patients from overflow queue
    #if ID == 1: print(f'number of patients before adding from overflow = {hospital_dict[ID].num_patients}')
    '''for i in range(0,len(hospital_dict[ID].overflow_array)-1):

        
        if sum(hospital_dict[ID].overflow_array) == 0:
            break

        temp = hospital_dict[ID].overflow_array[i] + hospital_dict[ID].num_patients

        if temp >= hospital_dict[ID].patient_capacity:
            hospital_dict[ID].num_patients = hospital_dict[ID].patient_capacity
            hospital_dict[ID].overflow_array[i] = temp - hospital_dict[ID].patient_capacity
            break

        else:
            hospital_dict[ID].num_patients += hospital_dict[ID].overflow_array[i]
            hospital_dict[ID].overflow_array[i] = 0
        
    #if ID == 1: print(f'number of patients after adding from overflow = {hospital_dict[ID].num_patients}')
    #if ID == 1: print(f'new overflow queue = {hospital_dict[ID].overflow_array}')
        
  
    #update overflow queue if there are still patients after filling the hospital
    hospital_dict[ID].overflow_array[0] += hospital_dict[ID].overflow_array[1]

    for i in range(1,len(hospital_dict[ID].overflow_array)-1):
        hospital_dict[ID].overflow_array[i] = hospital_dict[ID].overflow_array[i+1]
    
    hospital_dict[ID].overflow_array[-1] = 0
    
    #if ID == 1: print(f'queue after shift = {hospital_dict[ID].overflow_array}')

    #calculate arrivals
    arrivals = np.random.poisson(lam)

    #if ID == 1: print(f'arrivals = {arrivals}')

    #update number of patients and overflow queue based on arrivals
    new_total = hospital_dict[ID].num_patients + arrivals

    #if ID == 1: print(f'num patients (w/ overflow) + arrivals = {new_total}')

    if new_total < hospital_dict[ID].patient_capacity:
        hospital_dict[ID].num_patients = max(0,new_total)
        
    else:
        hospital_dict[ID].num_patients = hospital_dict[ID].patient_capacity
        hospital_dict[ID].overflow_array[-1] = new_total - hospital_dict[ID].patient_capacity'''
    
    
    temp = hospital_dict[ID].total_overflow + hospital_dict[ID].num_patients

    if temp >= hospital_dict[ID].patient_capacity:
        hospital_dict[ID].num_patients = hospital_dict[ID].patient_capacity
        hospital_dict[ID].total_overflow = temp - hospital_dict[ID].patient_capacity

    else:
        hospital_dict[ID].num_patients += hospital_dict[ID].total_overflow
        hospital_dict[ID].total_overflow = 0
    
    #if ID == 1: print(f'number of patients after adding from overflow = {hospital_dict[ID].num_patients}')
    #if ID == 1: print(f'new overflow queue = {hospital_dict[ID].overflow_array}')
        
  
    #update overflow queue if there are still patients after filling the hospital
    
    #if ID == 1: print(f'queue after shift = {hospital_dict[ID].overflow_array}')

    #calculate arrivals
    arrivals = np.random.poisson(lam)

    #if ID == 1: print(f'arrivals = {arrivals}')

    #update number of patients and overflow queue based on arrivals
    new_total = hospital_dict[ID].num_patients + arrivals

    #if ID == 1: print(f'num patients (w/ overflow) + arrivals = {new_total}')

    if new_total < hospital_dict[ID].patient_capacity:
        hospital_dict[ID].num_patients = max(0,new_total)
        
    else:
        hospital_dict[ID].num_patients = hospital_dict[ID].patient_capacity
        hospital_dict[ID].total_overflow += new_total - hospital_dict[ID].patient_capacity
    
    if(ID == 1):
        print(f'arrivals = {arrivals}')
        print(f'departures = {departures}')
        print(f'num patients = {hospital_dict[ID].num_patients}')
        print(f'final overflow = {hospital_dict[ID].total_overflow}')

    #if ID == 1: print(f'final overflow queue = {hospital_dict[ID].overflow_array}')
    #if ID == 1: print(f'final number of patients = {hospital_dict[ID].num_patients}')
    

    return hospital_dict

def queue_evolve(ID, hospital_dict,time_step, lam, mewGood, mewBad, mewMid):
    '''
    1st implementation of the queuing implentation. This version has a queue to track the number of patients who were not admitted to the hospital,
    but does not differentiate between those who arrived during the current time step and those who have been waiting for multiple days. There is also
    no chance of those in the overflow queue dying.
    '''

    QoC = hospital_dict[ID].num_patients/(hospital_dict[ID].num_nurses * 6)

    arrivals = np.random.poisson(lam)

    if QoC < 2:
        departures = np.random.poisson(mewGood)
    elif QoC >= 2 and QoC <= 4:
        departures = np.random.poisson(mewMid)
    else:
        departures = np.random.poisson(mewBad)

    delta = arrivals - departures

    total_change = hospital_dict[ID].num_patients + delta + hospital_dict[ID].overflow

    if total_change < hospital_dict[ID].patient_capacity:
        hospital_dict[ID].num_patients = max(0,total_change)
    elif total_change >= hospital_dict[ID].patient_capacity:
        hospital_dict[ID].num_patients = hospital_dict[ID].patient_capacity
        hospital_dict[ID].overflow = total_change - hospital_dict[ID].patient_capacity
        

    #L = max(0, hospital_dict[ID].num_patients + arrivals - departures)

    #hospital_dict[ID].num_patients = L

    return hospital_dict


def evolve(hospital_dict,time_step, action):

    #call drift patients on every hospital
    
    for ID in hospital_dict.keys():
        
        #hospital_dict = drift_patients(ID,hospital_dict,hospital_dict[ID].pop_susceptible,hospital_dict[ID].pop_infected,hospital_dict[ID].num_patients,hospital_dict[ID].pop_recovered,time_step)
        #hospital_dict = queue_evolve(ID,hospital_dict,time_step, lam = 6.0, mewGood = 6.4, mewBad = 5.9, mewMid = 6.01)
        hospital_dict = queue_evolve_v2(ID,hospital_dict,time_step, lam = 6.0, mewGood = 6.25, mewBad = 5.9, mewMid = 6.01)
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
    '''
    for ID in hospital_dict.keys():
        new_deaths = hospital_dict[ID].deaths_delta
        cost += new_deaths*2
        hospital_dict[ID].deaths_delta = 0
        if hospital_dict[ID].num_nurses != 0:
        #temporary reward function

            care_r = hospital_dict[ID].num_patients/hospital_dict[ID].num_nurses_unquantized
            if care_r >= 0 and care_r < 4:
                cost += (20/3)*care_r - 10
            else:
                cost += (140/3)*care_r - 130
            
            if action[ID - 1] < 0: #ID -1 because ID starts at 1 but action starts at 0
                cost += action[ID-1] * 5
            
        else:
            cost += 300*2
    '''
    for ID in hospital_dict.keys():
        #print(time_step)
        #print(f'prev_nurses = {hospital_dict[ID].prev_nurses}')
        #print(f'action = {action[ID-1]}')
        if action[ID - 1] < hospital_dict[ID].prev_nurses: #ID -1 because ID starts at 1 but action starts at 0
                cost += -1*(action[ID-1] - hospital_dict[ID].prev_nurses)*6
                #print(f'cost = {cost}')
                #print(f'cost = {cost}')
                #print(action[ID-1])
                #print(hospital_dict[ID].prev_nurses)
                #print(f'cost = {-1*(action[ID-1] - hospital_dict[ID].prev_nurses)*5}')

        cost += sum(hospital_dict[ID].overflow_array) *4
        cost += hospital_dict[ID].deaths_delta * 40

        #print(f'cost = {cost}')

    
  

    
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
    end_time = 100000
    
    #evolution loop
    t = 0

    picture = []
    t1 = time.time()

    quantized = True
    optimal = False
    no_Control = False

    saved_states = []

    care_ar = []

    running_cost = 0




    

    initial_total_pop = hospital_dict[1].total_population() + hospital_dict[2].total_population()


    if optimal == True:
        Q.table = np.load('/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/Q_table.npy')
        #Q.remove_bad_actions()
        for i in range(Q.table.shape[0]):
            for j in range(Q.table.shape[1]):
                if Q.table[i][j] == 0:
                    Q.table[i][j] = 10**10
    while(1):

        #Dynamically add empty control values for each hospital, at time step
        #action_dict = increment_action_dict(hospital_dict, action_dict, t+1)

        #print("-------------------State data at time = " + str(t) + "-------------------")
        if t%10000 == 0:
            print('time step = ',t)

        #get initial state
        if (quantized == False):
            state = get_state(hospital_dict)
        if (quantized == True):
            state = get_state(hospital_dict)
            saved_states.append(get_state(hospital_dict))
            #print(f"state = {state}")
            state = quantize_state(hospital_dict,state, Q)
            #print(f"quantized state = {state}")

        care_ar.append(hospital_dict[1].num_patients/hospital_dict[1].num_nurses * 6)
        care_ar.append(hospital_dict[2].num_patients/(hospital_dict[2].num_nurses*6))

        #print('initial state = ',state)

        #print('time to get state = ',tok-tic)

        #get ID of initial state
        tic = time.time()
        state_ID = get_state_ID(state,Q)
        tok = time.time()
        #print(f'found state from id = {Q.states[state_ID]}')
        #print(f"state ID = {state_ID}")
        #print('initial state id = ',state_ID)

        print('time to get state id = ',tok-tic)
        

        #have the agent choose an action
        if optimal == False:
            action, action_ID = Q.choose_action(state_ID, hospital_dict,t)
        if optimal == True:
            action, action_ID = Q.choose_optimal_action(state_ID, hospital_dict,t)
            print(f'optimal action = {action}')
            print(f'state id = {state_ID}')
            print(f'state = {Q.states[state_ID]}')
            #print(f"Q-value = {Q.table[state_ID,action_ID]}")
        if no_Control == True:
            action,action_ID = [0,0],0

        #print(f"action = {action}")


        #print('action = ',action)
        #print('found action id = ',action_ID)
        #debugging check
        #print('time to choose action = ',tok-tik)
        #print(f'num_patients = {hospital_dict[1].num_patients,hospital_dict[2].num_patients}')
        #post the action to the action dict
        hospital_dict = take_action(action, hospital_dict, t)

        #print(f'num_nurses = {hospital_dict[1].num_nurses,hospital_dict[2].num_nurses}')
        #print('time to take action = ',tok-tik)
        #print('all nurses = ',hospital_dict[1].num_nurses + hospital_dict[2].num_nurses)

        #print_hospital_data(hospital_dict)

        #transition the sytstem to the next state and get the reward

        hospital_dict,reward = evolve(hospital_dict= hospital_dict, time_step= t, action = action)

        #print('time to evolve = ',tok-tik)

        for i in hospital_dict.keys():
            hospital_dict[i].prev_nurses = action[i-1]

        running_cost += reward

        #get the new state
        tik = time.time()
        if(quantized == False):
            next_state = get_state(hospital_dict)
        if(quantized == True):
            next_state = get_state(hospital_dict)
            next_state = quantize_state(hospital_dict,next_state, Q)
        #print('time to get next state = ',tok-tik)

        #get the new state ID
        next_state_ID = get_state_ID(next_state,Q)
        #print('time to get next state id = ',tok-tik)

        #debugging check
        #print('next state ID = ',next_state_ID)
        #print('next state = ',next_state)

        #print('Reward = ', reward)
        #print_care_ratios(hospital_dict)

        #update the Q table
        if optimal == False:
            Q.learn(state_ID, action_ID, reward, next_state_ID)
        #print('time to learn = ',tok-tik)
        #print("total time = ",T2 - T1)

        #this is to graph the average care ratio over time after episodes are finished. I named it picture because I'm lazy (Copilot wrote this line lol)
        #picture.append(get_average_care_ratio(hospital_dict))
        
        if t % 10000 == 0 and optimal == False and no_Control == False:
            np.save("/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/Q_table.npy",Q.table)
            np.save("/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/actions.npy",Q.actions)
            np.save("/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/states.npy",Q.states)

        t += 1

        #+1 since time is incrememented after state transition
        if t == end_time + 1 : break

    t2 = time.time()
    print(f'time = {t2-t1} s')

    for i in hospital_dict.keys():
        print(f'number of deaths in hospital {i} = {hospital_dict[i].num_deaths}')

    total_Q_entries = Q.table.shape[0]*Q.table.shape[1]
    print(f"total_Q_entries = {total_Q_entries}")
    print(f"num_Q_entries_filled = {Q.num_Q_values_updated}")
    print(f"percent Q entries filled = {Q.num_Q_values_updated/total_Q_entries * 100} %")

    print("saving Q table...")
    if optimal == False and no_Control == False:
        
        Q.save_table()
    print("Q table saved")

    print(f"min care ratio = {np.min(care_ar)}")
    print(f"max care ratio = {np.max(care_ar)}")
    print(f'average care ratio = {np.mean(care_ar)}')
    print(f"standard deviation of care ratio = {np.std(care_ar)}")

    print(f'initial_total_pop = {initial_total_pop}')
    print(f'final_total_pop = {hospital_dict[1].total_population() + hospital_dict[2].total_population()}')

    print(f'running cost = {running_cost}')

    plot_results(saved_states)

    np.save("/Users/reecefuller/Documents/MTHE493/MTHE-493-Stochastic-Control/saved_states.npy",np.asarray(saved_states))

    #graph_care_ratio(picture)

    #draw_graph(G)

    #print_hospital_data(hospital_dict)
    

if __name__ == "__main__":
    main()


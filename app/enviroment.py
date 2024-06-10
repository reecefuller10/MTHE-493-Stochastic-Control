import random
import sys
import time

import networkx as nx
import numpy as np
import pandas as pd

# Change this path to /you/path/here/MTHE-493-Stochastic-Control/app/utils
# sys.path.append(r'C:\Users\Gmack\MTHE-493-Stochastic-Control\app\utils')
sys.path.append('/Users/reecefuller/Documents/MTHE-493-Stochastic-Control/app/utils')

# print(sys.path)

import pickle

from Q_learning import *
from utils.control_system_helper import *

# Import functions from helper files
from utils.enviroment_helper import *
from utils.graph_helper import *
from utils.transmission_helper import *



def generate_losses(hospital_dict, ID):


    '''
    randomly generate the number of deaths that occur in the overflow queue based on n independent binomial trials with parameter p
    where n is the number of patients in the overflow queue for 14 or more days, and p is the probability of death.
    '''


    p = 0.5

    count = np.random.binomial(hospital_dict[ID].overflow_array[0], p)
    hospital_dict[ID].overflow_array[0] -= count
    hospital_dict[ID].num_deaths += count
    hospital_dict[ID].deaths_delta = count


    return hospital_dict


def queue_evolve_v2(ID, hospital_dict, lam, mewBad):
    '''
    2nd version of the queuing evolution. This version has a queue to track the number of patients who were not admitted to the hospital.
    Each time step, if there are people who were waiting for 14 or more days, they have a probability of dying given by n independent binomial distributions
    with paramter p (see generate_losses()). This version prioritizes those in the overflow queue over those who arrived during the current time step.
    '''

    hospital_dict = generate_losses(hospital_dict, ID)


    QoC = hospital_dict[ID].num_patients / (hospital_dict[ID].num_nurses * 6)

    if QoC < 6:
        departures = np.random.poisson(6.25 - ((0.36) / 6) * QoC)

    else:
        departures = np.random.poisson(mewBad)
    '''

    if QoC < 6:
        departures = np.random.poisson(6.25-((0.35)/6)*QoC)
    else:
        departures = np.random.poisson(mewBad)


    # update number of patients in hospital based on departures
    hospital_dict[ID].num_patients = max(0, hospital_dict[ID].num_patients - departures)

    # bring in patients from overflow queue
    for i in range(0, len(hospital_dict[ID].overflow_array) - 1):


        if sum(hospital_dict[ID].overflow_array) == 0:
            break

        temp = hospital_dict[ID].overflow_array[i] + hospital_dict[ID].num_patients

        if temp >= hospital_dict[ID].patient_capacity:
            hospital_dict[ID].num_patients = hospital_dict[ID].patient_capacity
            hospital_dict[ID].overflow_array[i] = (
                temp - hospital_dict[ID].patient_capacity
            )
            break

        else:
            hospital_dict[ID].num_patients += hospital_dict[ID].overflow_array[i]
            hospital_dict[ID].overflow_array[i] = 0


    # update overflow queue if there are still patients after filling the hospital
    hospital_dict[ID].overflow_array[0] += hospital_dict[ID].overflow_array[1]

    for i in range(1, len(hospital_dict[ID].overflow_array) - 1):
        hospital_dict[ID].overflow_array[i] = hospital_dict[ID].overflow_array[i + 1]


    hospital_dict[ID].overflow_array[-1] = 0


    # calculate arrivals
    arrivals = np.random.poisson(lam)


    # update number of patients and overflow queue based on arrivals
    new_total = hospital_dict[ID].num_patients + arrivals


    if new_total < hospital_dict[ID].patient_capacity:
        hospital_dict[ID].num_patients = max(0, new_total)

    else:
        hospital_dict[ID].num_patients = hospital_dict[ID].patient_capacity
        hospital_dict[ID].overflow_array[-1] = (
            new_total - hospital_dict[ID].patient_capacity
        )


    return hospital_dict


def queue_evolve(ID, hospital_dict, lam, mewGood, mewBad, mewMid):
    '''
    1st implementation of the queuing implentation. This version has a queue to track the number of patients who were not admitted to the hospital,
    but does not differentiate between those who arrived during the current time step and those who have been waiting for multiple days. There is also
    no chance of those in the overflow queue dying.
    '''


    QoC = hospital_dict[ID].num_patients / (hospital_dict[ID].num_nurses * 6)


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
        hospital_dict[ID].num_patients = max(0, total_change)
    elif total_change >= hospital_dict[ID].patient_capacity:
        hospital_dict[ID].num_patients = hospital_dict[ID].patient_capacity
        hospital_dict[ID].overflow = total_change - hospital_dict[ID].patient_capacity

    return hospital_dict


def evolve(hospital_dict, time_step, action):


    # call drift patients on every hospital


    for ID in hospital_dict.keys():

        hospital_dict = queue_evolve_v2(
            ID, hospital_dict, time_step, lam=6.0, mewGood=6.25, mewBad=5.9, mewMid=6.01
        )

    # get all care ratios
    care_array = []
    for keys in hospital_dict.keys():
        care_array.append(hospital_dict[keys].care_ratio)

    cost = 0
            


    for ID in hospital_dict.keys():

        if action[ID - 1] < hospital_dict[ID].prev_nurses:
            cost_nurses = (hospital_dict[ID].prev_nurses - action[ID - 1]) * 6
            print(f'nurse cost = {cost_nurses}')
            cost += cost_nurses

            hospital_dict[ID].total_transfers += -1 * (
                action[ID - 1] - hospital_dict[ID].prev_nurses
            )

        if hospital_dict[ID].num_patients >= 0.75 * hospital_dict[ID].patient_capacity:
            pass

        cost += hospital_dict[ID].deaths_delta * 40

    return hospital_dict, cost


def main():

    # create a dictionary storing objects that represent each hospital, indexed by ID
    hospital_dict = create_data_dict(num=2)

    # Initialize graph structure
    G = init_graph()

    # initialize Q stuff
    Q = Q_table(learning_rate=0.1, discount_factor=0.7, gamma=0.9)

    Q.initalize_actions(hospital_dict)
    Q.initialize_states(hospital_dict)
    Q.initialize_table()

    print(f"table dimensions = {np.shape(Q.table)}")

    print()

    # number of episodes
    end_time = 5000000


    t = 0

    quantized = True
    optimal = False
    no_Control = False

    saved_states = []
    saved_nurses = []

    care_ar = []

    running_cost = 0


    initial_total_pop = (
        hospital_dict[1].total_population() + hospital_dict[2].total_population()
    )

    if optimal == True:

        Q.table = np.load(
            '/Users/reecefuller/Documents/MTHE-493-Stochastic-Control/Q_table.npy'
        )


    while 1:


        # Dynamically add empty control values for each hospital, at time step

        if t % 10000 == 0:
            print('time step = ', t)

        # get initial state
        if quantized == False:

            state = get_state(hospital_dict)
        if quantized == True:
            state = get_state(hospital_dict)
            saved_states.append(get_state(hospital_dict))
            saved_nurses.append(
                [hospital_dict[1].num_nurses * 6, hospital_dict[2].num_nurses * 6]
            )
            state = quantize_state(hospital_dict, state, Q)


        care_ar.append(
            hospital_dict[1].num_patients / (hospital_dict[1].num_nurses * 6)
        )
        care_ar.append(
            hospital_dict[2].num_patients / (hospital_dict[2].num_nurses * 6)
        )

        state_ID = get_state_ID(state, Q)

        # have the agent choose an action

        if optimal == False:
            action, action_ID = Q.choose_action(state_ID, hospital_dict, t)
        if optimal == True:

            action, action_ID = Q.choose_optimal_action(state_ID, hospital_dict, t)


        if no_Control == True:
            action, action_ID = [5, 5], 4


        print('action = ', action)
        print('state = ', state)

        hospital_dict = take_action(action, hospital_dict, t)
        print(f'time = {t}')
        print(f'num_nurses = {hospital_dict[1].num_nurses,hospital_dict[2].num_nurses}')


        # transition the sytstem to the next state and get the reward
        hospital_dict, reward = evolve(
            hospital_dict=hospital_dict, time_step=t, action=action
        )


        for i in hospital_dict.keys():
            hospital_dict[i].prev_nurses = action[i - 1]

        running_cost += reward

        # get the new state

        tik = time.time()
        if quantized == False:
            next_state = get_state(hospital_dict)
        if quantized == True:
            next_state = get_state(hospital_dict)

            next_state = quantize_state(hospital_dict, next_state, Q)

        # get the new state ID
        next_state_ID = get_state_ID(next_state, Q)

        # update the Q table
        if optimal == False:
            Q.learn(state_ID, action_ID, reward, next_state_ID)
        #

        if t % 10000 == 0 and optimal == False and no_Control == False:
            np.save(
                "/Users/reecefuller/Documents/MTHE-493-Stochastic-Control/Q_table.npy",
                Q.table,
            )
            np.save(
                "/Users/reecefuller/Documents/MTHE-493-Stochastic-Control/actions.npy",
                Q.actions,
            )
            np.save(
                "/Users/reecefuller/Documents/MTHE-493-Stochastic-Control/states.npy",
                Q.states,
            )

        t += 1

        if t == end_time + 1:
            break

    print(
        f'total transfered = {hospital_dict[1].total_transfers + hospital_dict[2].total_transfers}'
    )

    t2 = time.time()
    print(f'time = {t2-t1} s')

    for i in hospital_dict.keys():
        print(f'number of deaths in hospital {i} = {hospital_dict[i].num_deaths}')

    total_Q_entries = Q.table.shape[0] * Q.table.shape[1]
    print(f"total_Q_entries = {total_Q_entries}")
    print(f"num_Q_entries_filled = {Q.num_Q_values_updated}")
    print(
        f"percent Q entries filled = {Q.num_Q_values_updated/total_Q_entries * 100} %"
    )

    print("saving Q table...")
    if optimal == False and no_Control == False:

        Q.save_table()
    print("Q table saved")

    print(f"min care ratio = {np.min(care_ar)}")
    print(f"max care ratio = {np.max(care_ar)}")
    print(f'average care ratio = {np.mean(care_ar)}')
    print(f"standard deviation of care ratio = {np.std(care_ar)}")

    print(f'initial_total_pop = {initial_total_pop}')
    print(
        f'final_total_pop = {hospital_dict[1].total_population() + hospital_dict[2].total_population()}'
    )

    print(f'running cost = {running_cost}')


    plot_results(saved_states, saved_nurses)

    np.save(
        "/Users/reecefuller/Documents/MTHE-493-Stochastic-Control/saved_states.npy",
        np.asarray(saved_states),
    )


if __name__ == "__main__":
    main()

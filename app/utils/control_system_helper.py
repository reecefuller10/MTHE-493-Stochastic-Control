import numpy as np
from transmission_helper import *

#todo (maybe)
def create_state_space_representation(ID, hospital_dict):

    
    state_matrix = np.array([0,0])

#create the dictionary used to represent actions taken at each time step
def create_action_dict(hospital_dict):

    #inner dictionary is ID, outer is time step

    action_dict = {}

    time_dict = {}

    #initialize action space for time 0 (all 0 since no actions can be taken before t = 0)
    for id in hospital_dict.keys():

        action_dict[id] = 0

    time_dict[0] = action_dict


    return time_dict

#dynamically add empty control values for each hospital and time step (eliminates need for a lot of fail cases)
def increment_action_dict(hospital_dict, action_dict, t):

    actions = {}

    for id in hospital_dict.keys():

        actions[id] = 0

    action_dict[t+1] = actions

    return action_dict

#update action_dict to reflect actions that will be implemented at the next time step
def post_action(from_id, to_id, num_nurses, G, hospital_dict, action_dict, time_step):

    action_dict[time_step][from_id] -= num_nurses
    action_dict[time_step][to_id] += num_nurses

    return action_dict

#apply the posted actions to the hospital_dict
def resolve_action(hospital_dict, action_dict, time_step):

    #loop through hospitals and update their nurse counts
    for id in hospital_dict.keys():
            if(time_step != 0):
                '''
                print('\n')
                print('action dict = ', action_dict[time_step-1])
                print('\n')
                '''
                hospital_dict[id].num_nurses += action_dict[time_step-1][id]
                


    

    return hospital_dict
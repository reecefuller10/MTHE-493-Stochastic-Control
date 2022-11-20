import numpy as np
from transmission_helper import *

#Depreciated
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

    action_dict[t] = actions

    return action_dict

#update action_dict to reflect actions that will be implemented at the next time step
def post_action(action, action_dict, time_step):
    
    actions = {}
    
    #loop through hospitals and update the actions dict based on actions taken
    for key in list(action_dict[time_step].keys()):
        idx = int(key)
        actions[key] = action[idx -1 ]

    return actions

#apply the posted actions to the hospital_dict
def resolve_action(hospital_dict, action_dict, time_step):

    #loop through hospitals and update their nurse counts
    for id in hospital_dict.keys():
            if(time_step != 0):
                
                hospital_dict[id].num_nurses += action_dict[time_step][id]
                
    return hospital_dict
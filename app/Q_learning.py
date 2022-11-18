import numpy as np
import pandas as pd

def create_state_space(hospital_dict, population_dict):
    


    return 0

def create_action_space(hospital_dict):

    hospital_IDs = hospital_dict.keys()

    action_space = {}
    sample_dict = {}

    #create an empty dictionary with keys for each hospital
    for keys in hospital_dict.keys():
        sample_dict[keys] = 0

    action_space[0] = sample_dict.copy()

    i = 1
    #create a dictionary of dictionaries, where each inner dictionary is a possible action
    #this is necessary for the Q-learning algorithm to have actions indexed by a number

    #Might be a better way to do this, but this works for now
    #Loop through each hospital and transfer all possible number of patients to all possible hospitals
    for ID in hospital_IDs:
        num_nurses = hospital_dict[ID].num_nurses
        
        for to_ID in hospital_IDs :

            if ID != to_ID:
                for nurse in range(1,num_nurses+1):
                    action_space[i] = sample_dict.copy()
                    action_space[i][ID] = -1*nurse
                    action_space[i][to_ID] = nurse
                    i += 1
    print(action_space)
    return action_space

class Q_table:
    def __init__(self,states,actions,learning_rate,discount_factor,gamma):
        self.states = states
        self.actions = actions
        self.table = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.gamma = gamma

    def initialize_table(self):
        for state in self.states:
            self.table = self.table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.table.columns,
                    name=state,
                )
            )


def main():
    q_table = Q_table(states = [1,2,3,4,5], actions = [1,2,3,4,5], learning_rate = 0.1, discount_factor = 0.9, gamma = 0.9)
    q_table.initialize_table()
    print(q_table.table)

if __name__ == "__main__":
    main()


import numpy as np
import pandas as pd
import random as rand
import time

class state:
    def __init__(self, ID, state_values):
        self.ID = ID
        self.state_values = state_values
        self.sum = np.sum(state_values)

    def __lt__(self, other): #less than method for sorting
        return self.sum < other.sum
    def __eq__(self, other): #equal method for sorting
        return self.sum == other.sum
    def __gt__(self, other): #greater than method for sorting
        return self.sum > other.sum

#create an array with all possible states
def create_state_space(hospital_dict):
    
    N = 10 #number of partitions of the state space (for easier lookups later)

    #going to index each possible state by a number

    #dict indexed by hospital ID representing the max number of patients at the hospital
    patients_dict = {}
    object_array = []
    
    #array of arrays where the inner index is all possible values for that hospital
    for ID in hospital_dict.keys():
        array = np.linspace(0,hospital_dict[ID].patient_capacity,hospital_dict[ID].patient_capacity +1 ,True, dtype = int)
        print(f"linspace array = {array}")
        patients_dict[ID] = array

    #array where each entry is a possible state
    #No idea how this line works
    comb_array = np.array(np.meshgrid(patients_dict[1],patients_dict[2],patients_dict[3],patients_dict[4],patients_dict[5])).T.reshape(-1,5)
    print(comb_array)
    print(comb_array[0])
    print(comb_array)
    for i in range(len(comb_array)):
        value = state(i,comb_array[i])
        object_array.append(value)
        
    sorted_array = sorted(object_array)
    '''
    for i in range(len(sorted_array)):
        print(f"sorted_array[{i}] = {sorted_array[i].state_values}, sum = {sorted_array[i].sum} id = {sorted_array[i].ID}")
    '''
    partition_dict = {}
    min = sorted_array[0].sum
    max = sorted_array[-1].sum
    buckets = np.linspace(min,max,N,True, dtype = int)
    buckets = np.delete(buckets,0)
    print(f"buckets = {buckets}")

    for i in buckets:
        partition_dict[i] = []
    
    print(partition_dict)
    
    for object in sorted_array:
        for i in buckets:
            if object.sum <= i:
                print(f"bucket chose = {i} for a sum of {object.sum}")
                partition_dict[i].append(object)
                break
    
    
    #return all states
    return comb_array

#create an array with all possible actions
def create_action_space(hospital_dict):

    nurses_dict = {}

    #creates an array of arrays where the inside arrays varries over al possible nurse transfers
    for ID in hospital_dict.keys():
        array = np.linspace(-1*hospital_dict[ID].nurse_capacity, hospital_dict[ID].nurse_capacity,2*hospital_dict[ID].nurse_capacity +1 , True, dtype = int)
        nurses_dict[ID] = array
    
    #some wacky code that creates all possible action spaces (idfk how this works but it's exactly what we need)
    comb_array = np.array(np.meshgrid(nurses_dict[1],nurses_dict[2],nurses_dict[3],nurses_dict[4],nurses_dict[5])).T.reshape(-1,5)
    
    #get the indices of all actions that sum to 0 (cant recieve more nurses than were transfered)
    keep_array = []
    for i in range(len(comb_array)):
        if np.sum(comb_array[i]) == 0:
            keep_array.append(i)
    
    #only keep valid actions
    comb_array = comb_array[keep_array]

    #returns all possible actions
    return comb_array

#get current state as an array
def get_state(hospital_dict):
    state = []
    
    #loop through all states and append
    for ID in hospital_dict.keys():
        state.append(hospital_dict[ID].num_patients)

    return state

#get ID of a state in the Q table
def get_state_ID(state,Q):

    state_sum = np.sum(state)

    buckets = Q.partitioned_states.keys()

    for i in buckets:
        if state_sum <= i:
            search_supremum = i
            break

    search_array = Q.partitioned_states[search_supremum]

    #loop through all states until the state is found and return its ID
    for i in range(0,len(search_array)):

            if np.array_equal(state,search_array[i].state_values):
                idx = search_array[i].ID
                break

    return idx

#get ID of an action in the (maybe depreciated)
def get_action_ID(action,Q_table):

    idx = np.where(Q_table.actions == action)

    return idx

class Q_table:
    def __init__(self,learning_rate,discount_factor,gamma):

        #Hyperparamters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.gamma = gamma

        #epsilon controlls how often the agent explores vs exploits
        self.epsilon = 1
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

        self.table = 0
        self.actions = 0
        self.states = 0
        self.num_Q_values_updated = 0

    def initalize_actions(self,hospital_dict):
        self.actions = create_action_space(hospital_dict)
    
    def initialize_states(self,hospital_dict):
        #self.states = create_state_space(hospital_dict)

        N = 100 #number of partitions of the state space (for easier lookups later)

        #going to index each possible state by a number

        #dict indexed by hospital ID representing the max number of patients at the hospital
        patients_dict = {}
        object_array = []
        
        #array of arrays where the inner index is all possible values for that hospital
        for ID in hospital_dict.keys():
            array = np.linspace(0,hospital_dict[ID].patient_capacity,hospital_dict[ID].patient_capacity +1 ,True, dtype = int)
            #print(f"linspace array = {array}")
            patients_dict[ID] = array

        #array where each entry is a possible state
        #No idea how this line works

        comb_array = np.array(np.meshgrid(patients_dict[1],patients_dict[2],patients_dict[3],patients_dict[4],patients_dict[5])).T.reshape(-1,5)
        
        self.states = comb_array

        #print(comb_array)
        #print(comb_array[0])
        #print(comb_array)
        tik = time.time()
        for i in range(len(comb_array)):
            value = state(i,comb_array[i])
            object_array.append(value)
        tok = time.time()
        print(f"creating state objects took {tok-tik} seconds")

        tik = time.time()
        #dont need to sort, jsut get the the max # of patients in each hospital and add them (TODO)
        sorted_array = sorted(object_array)
        tok = time.time()
        print(f"sorting took {tok-tik} seconds")

        '''
        for i in range(len(sorted_array)):
            print(f"sorted_array[{i}] = {sorted_array[i].state_values}, sum = {sorted_array[i].sum} id = {sorted_array[i].ID}")
        '''
        partition_dict = {}
        min = sorted_array[0].sum
        max = sorted_array[-1].sum
        buckets = np.linspace(min,max,N,True, dtype = int)
        buckets = np.delete(buckets,0)
        #print(f"buckets = {buckets}")

        for i in buckets:
            partition_dict[i] = []
        
        #print(partition_dict)
        tik = time.time()
        for object in sorted_array:
            for i in buckets:
                if object.sum <= i:
                    #print(f"bucket chose = {i} for a sum of {object.sum}")
                    partition_dict[i].append(object)
                    break
        tok = time.time()
        print(f"partitioning took {tok-tik} seconds")
        
        self.partitioned_states = partition_dict
        
    def initialize_table(self):
        #initialize table with zeros (table is represented by a 2d array indexed as table[state][action] = Q_value)
        self.table = np.zeros(((self.states.shape)[0],(self.actions.shape)[0]))
        
    def choose_action(self,state_ID,hospital_dict):

        #Agent keeps picking unvalid actions not in the actions table (this is a temp fix) (TODO: figure out why this happens)
        non_valid = True
        while(non_valid == True):

            #explore
            if rand.random() < self.epsilon:
                action = rand.choice(self.actions)
                
            #exploit
            else:
                #action = self.table[state_ID].argmax()
                action_idx = np.argmax(self.table[state_ID])
                action = self.actions[action_idx]
                #print("exploited action = ", action)
            
            #used range function because of error when converting iterator to scalar (h-1 is the problem) (TODO: Optimize this)
            for h in range(1,5):

                #fail case to handle if it picks an integer instead of a 5-tuple (TODO: stop this from happening)
                try: 
                    if action.type() == int.type(): break
                except: 0
               
                #If we are removing nurses from a hospital, insure we are not removing more than there are at the hopsital.
            
                
                if(action[h-1] < 0):
                    if(hospital_dict[h].num_nurses + action[h-1] < 0):
                        non_valid = True
                        break
                
                #If we are adding nurses to a hospital, insure we are not adding more than the capacity
                if(action[h-1] >= 0):
                    if(hospital_dict[h].num_nurses + action[h-1] > hospital_dict[h].nurse_capacity):
                        non_valid = True
                        break

                #if no fail cases are tripped, the action is valid
                non_valid = False

        #decay epsilonto bias exploitation over time
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        #Get action ID
        for i in range(0,self.actions.shape[0]):

            if np.array_equal(action,self.actions[i]):

                idx = i
                break

        #return chosen action and its index
        return action, idx

    def learn(self,state,action,reward,next_state):

        print("old Q Value = ", self.table[state][action])
        if self.table[state][action] == 0:
            self.num_Q_values_updated += 1
        #update Q value based on the Bellman equation (this is the ML component)
        self.table[state][action] += self.learning_rate * (reward + self.discount_factor * self.table[next_state].max() - self.table[state][action])
        
        print("New Q_val = ", self.table[state][action])

def main():
    q_table = Q_table(states = [1,2,3,4,5], actions = [1,2,3,4,5], learning_rate = 0.1, discount_factor = 0.9, gamma = 0.9)
    q_table.initialize_table()
    print(q_table.table)

if __name__ == "__main__":
    main()


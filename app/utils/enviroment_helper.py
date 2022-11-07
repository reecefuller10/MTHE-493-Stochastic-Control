import networkx as nx
import numpy as np
import pandas as pd
import random

class Hospital:
    def __init__(self, ID, nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio):
        self.ID = ID
        self.nurse_capacity = nurse_capacity
        self.num_nurses = num_nurses
        self.patient_capacity = patient_capacity
        self.num_patients = num_patients
        self.care_ratio = care_ratio
        self.care_ratio_delta = num_nurses/num_patients - care_ratio

    def _update(self):
        self.care_ratio_delta = self.num_nurses/self.num_patients - self.care_ratio

    def echo_care_ratio(self):
        print(self.num_nurses + "/" + self.num_patients)

#Creates a hospital object
def create_hospital(ID,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio):
    
    #Initialize object
    h = Hospital(ID,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio)

    return h

#Updates any attribute of a hospital object
def set_hospital_attribute(hospital_dict, ID, attribute, new_val):
    
    #Get the value of the attribute were looking for
    prev_val = getattr(hospital_dict[ID], attribute)
    print('prev val = ' + str(prev_val))

    setattr(hospital_dict[ID], attribute, new_val)
    new_val = getattr(hospital_dict[ID], attribute)
    print('new val = ' + str(new_val))

#create a dictionary to store hospital attributes (indexed by ID)
def create_data_dict(num):

    #initialize dictionary
    data_dict = {}

    #generate (pseudo)random values for each attribute for each hospital (todo: Find actual values)
    for i in range(1,num+1):
        nurse_capacity = random.randint(10,20)
        num_nurses = random.randint(5,20)
        patient_capacity = random.randint(50,100)
        num_patients = random.randint(10,70)
        care_ratio = random.randint(1,4)

        #creates a hospital object with the given attributes for each hospital and stores it in the dictionary (indexed by i)
        data_dict[i] = create_hospital(i,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio)

    #return hospital dictionary
    return data_dict

#simple function to print all attributes for each hospital
def print_hospital_data(hospital_dict):

    for i in hospital_dict.keys():
        print("Data for Hospital " + str(i) + ":")
        print('nurse capacity =', hospital_dict[i].nurse_capacity)
        print('num nurses = ', hospital_dict[i].num_nurses)
        print('patient capacity = ', hospital_dict[i].patient_capacity)
        print('num patients', hospital_dict[i].num_patients)
        print('care ratio', hospital_dict[i].care_ratio)
        print("-----------------------")

#Calling this function advances the state for the hospital, absent of control.
def drift_patients(ID, hospital_dict,population, p_better,p_sick):

    #isolate hospital object from dictionary
    hospital = hospital_dict[ID]
    num_patients = hospital.num_patients

    #number of people who get better
    X = np.random.binomial(num_patients,p_better)

    print('X = ' + str(X))

    #number of new people who get sick
    Y = np.random.binomial(population, p_sick)

    print("Y = " + str(Y))

    delta = Y - X

    hospital_dict[ID].num_patients = num_patients + delta
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

def create_hospital(ID,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio):
    
    h = Hospital(ID,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio)

    return h

def update_hospital_attribute(hospital_dict, ID, attribute, new_val):
    
    prev_val = getattr(hospital_dict[ID], attribute)
    print('prev val = ' + str(prev_val))

    setattr(hospital_dict[ID], attribute, new_val)
    new_val = getattr(hospital_dict[ID], attribute)
    print('new val = ' + str(new_val))

def create_data_dict(num):

    data_dict = {}

    for i in range(1,num+1):
        nurse_capacity = random.randint(10,20)
        num_nurses = random.randint(5,20)
        patient_capacity = random.randint(50,100)
        num_patients = random.randint(10,70)
        care_ratio = random.randint(1,4)

        data_dict[i] = create_hospital(i,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio)

    return data_dict

def print_hospital_data(hospital_dict):

    for i in hospital_dict.keys():
        print("Data for Hospital " + str(i) + ":")
        print('nurse capacity =', hospital_dict[i].nurse_capacity)
        print('num nurses = ', hospital_dict[i].num_nurses)
        print('patient capacity = ', hospital_dict[i].patient_capacity)
        print('num patients', hospital_dict[i].num_patients)
        print('care ratio', hospital_dict[i].care_ratio)
        print("-----------------------")

def update_patients(ID, hospital_dict,population, p_better,p_sick):
    hospital = hospital_dict[ID]
    num_patients = hospital.num_patients

    #number of people who get better
    X = np.random.binomial(num_patients,p_better)

    print('X = ' + str(X))

    Y = np.random.binomial(population, p_sick)

    print("Y = " + str(Y))

    hospital_dict[ID].num_patients = num_patients - X + Y
import networkx as nx
import numpy as np
import pandas as pd
import random

class Hospital:
    def __init__(self, ID, nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio, pop_susceptible, pop_infected, pop_recovered):
        self.ID = ID
        self.nurse_capacity = nurse_capacity
        self.num_nurses = num_nurses
        self.patient_capacity = patient_capacity
        self.num_patients = num_patients
        self.care_ratio = care_ratio
        self.care_ratio_delta = num_nurses/num_patients - care_ratio
        self.pop_susceptible =  pop_susceptible
        self.pop_infected = pop_infected
        self.pop_recovered = pop_recovered


    def _update(self):
        self.care_ratio_delta = self.num_nurses/self.num_patients - self.care_ratio

    def echo_care_ratio(self):
        print(self.num_nurses + "/" + self.num_patients)

#Creates a hospital object
def create_hospital(ID,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio):
    
    #Initialize object
    h = Hospital(ID,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio)

    return h

#set any attribute of a hospital object (mainly for development purposes)
def set_hospital_attribute(hospital_dict, ID, attribute, new_val):
    
    #Hard set hospital attributes
    setattr(hospital_dict[ID], attribute, new_val)

#create a dictionary to store hospital attributes (indexed by ID)
def create_data_dict(num):

    #initialize dictionary
    data_dict = {}

    #generate (pseudo)random values for each attribute for each hospital (todo: Find actual values)
    for i in range(1,num+1):
        nurse_capacity = random.randint(30,100)
        num_nurses = random.randint(15,60)
        patient_capacity = random.randint(50,300)
        num_patients = random.randint(10,70)
        care_ratio = num_patients/num_nurses

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

#Prints the data for a single hospital
def print_single_hospital_data(ID,hospital_dict):
    print("Data for Hospital " + str(ID) + ":")
    print('nurse capacity =', hospital_dict[ID].nurse_capacity)
    print('num nurses = ', hospital_dict[ID].num_nurses)
    print('patient capacity = ', hospital_dict[ID].patient_capacity)
    print('num patients = ', hospital_dict[ID].num_patients)
    print('care ratio = ', hospital_dict[ID].care_ratio)
    print("-----------------------")

#Calling this function advances the state for the hospital, absent of control.
def drift_patients(ID, hospital_dict, pop_susceptible, pop_infected, pop_hospitalized, pop_recovered, time_step):
    
    #definition of the rates defining the transition in between states
    rate_susceptibletoinfected = 50                 #number of cases per day (different rates can be tested to see if they're stabilizable)
    rate_recoveredtoinfected = 1                    #random number less than sesceptibletoinfected (needs changing)
    rate_infectedtorecovered = 0.1                  #An infected individual will be sick for 10 days on average
    rate_infectedtohospitalized = 63961 / 2180000   #number of hospitalizations 2020-2021 / number of confirmed cases 2020-2021
    rate_hospitalizedtorecovered = 1/14.7           #on average hospitalized patients spent 14.7 days in the hospital
    
    #isolate hospital object from dictionary
    hospital = hospital_dict[ID]
    num_patients = hospital.num_patients

    #Rate calculations for poisson and binomial distributions
    #average value of an exponential function is the 1/rate
    P1 = 1 - np.exp(-1*rate_infectedtorecovered*time_step)
    P2 = 1 - np.exp(-1*rate_infectedtohospitalized*time_step)
    P3 = 1 - np.exp(-1*rate_susceptibletoinfected*time_step)
    P4 = 1 - np.exp(-1*rate_recoveredtoinfected*time_step)
    P5 = 1 - np.exp(-1*rate_hospitalizedtorecovered*time_step)
    
    #Transition population
    #average value of a poisson is what's inside the brackets
    #average value of a binomial distribution is n*p (i.e. multiply the inputs) 
    infected_to_recovered = np.random.binomial(infected, P1)
    infected_to_hospitalized = np.random.binomial(infected, P2)
    susceptible_to_infected = np.random.poisson(pop_susceptible * P3)
    recovered_to_infected = np.random.poisson(hospitalized * P4)
    hospitalized_to_recovered = np.random.binomial(hospitalized, P5)

    #Evolution of susceptible population
    susceptible = pop_susceptible - susceptible_to_infected

    #Evolution of recovered people
    recovered = pop_recovered + infected_to_recovered + hospitalized_to_recovered - recovered_to_infected

    #Evolution of infected population
    infected = pop_infected + recovered_to_infected + susceptible_to_infected - infected_to_hospitalized - infected_to_recovered

    #Evolution of hospitalized population
    hospitalized = pop_hospitalized + infected_to_hospitalized - hospitalized_to_recovered

    #number of hospitalized people that recover
    #X = np.random.binomial(num_patients,p_recover)
    #print('X = ' + str(X))
    #number of 
    #number of new people who get sick
    #Y = np.random.binomial(population, p_sick)
    #print("Y = " + str(Y))
    delta =  infected_to_hospitalized - hospitalized_to_recovered

    #For testing purposes. just showing info for hospital 3 because looking at all the hospital data hurts my eyes
    if ID == 3: 
        print('\n')
        print("------- State Transition Deltas: -------")
        print("Recovered patients = " + str(hospitalized_to_recovered))
        print("New patients = " + str(infected_to_hospitalized))           
        print("----------------------------------------")
        print('\n')

    #cant have the number of patients exceed the patient capacity
    if num_patients + delta >= hospital.patient_capacity :
        hospital_dict[ID].num_patients = hospital.patient_capacity
        hospital_dict[ID].care_ratio = hospital.num_patients/hospital.num_nurses
        return hospital_dict

    #update number of patients
    hospital_dict[ID].num_patients = hospitalized
    hospital_dict[ID].care_ratio = hospital.num_patients/hospital.num_nurses

    return hospital_dict

#temp function to generate random populations for all the hospitals and stores them in a list
def create_population_dict(keys):

    pop_dict = {}

    for i in keys:
        pop_dict[i] = random.randint(100,2000)

    return pop_dict


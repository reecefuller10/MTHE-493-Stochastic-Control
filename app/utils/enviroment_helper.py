import networkx as nx
import numpy as np
import pandas as pd
import random
import math as m

class Hospital:
    def __init__(self, ID, nurse_capacity, num_nurses, patient_capacity, num_patients, best_care_ratio, pop_susceptible, pop_infected, pop_recovered):
        self.ID = ID
        self.nurse_capacity = nurse_capacity
        self.num_nurses = num_nurses
        self.patient_capacity = patient_capacity
        self.num_patients = num_patients
        self.best_care_ratio = best_care_ratio
        if (self.num_patients == 0):
            self.care_ratio = 0
        else: 
            self.care_ratio = self.num_nurses/self.num_patients
        if(self.num_nurses == 0):
            self.care_ratio = 0
        else:
            self.care_ratio = self.num_nurses/self.num_patients
        self.care_ratio_delta = num_nurses/num_patients - best_care_ratio
        self.pop_susceptible =  pop_susceptible
        self.pop_infected = pop_infected
        self.pop_recovered = pop_recovered


    def echo_care_ratio(self):
        print(self.care_ratio + '(' + self.num_nurses + "/" + self.num_patients + ')')

#Creates a hospital object
def create_hospital(ID,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio, pop_susceptible, pop_infected, pop_recovered):
    
    #Initialize object
    h = Hospital(ID,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio, pop_susceptible, pop_infected, pop_recovered)

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
        '''
        nurse_capacity = random.randint(2,5)
        num_nurses = random.randint(2,nurse_capacity)
        patient_capacity = random.randint(4,20)
        num_patients = random.randint(1,patient_capacity)
        care_ratio = num_patients/num_nurses
        pop_susceptible = random.randint(5,100)
        pop_infected = random.randint(1,int(pop_susceptible/2))
        pop_recovered = 0
        '''
        nurse_capacity = 5
        num_nurses = 3
        patient_capacity = 60
        num_patients = 50
        care_ratio = num_patients/num_nurses
        pop_susceptible = 100000
        pop_infected = 50
        pop_recovered = 0

        #creates a hospital object with the given attributes for each hospital and stores it in the dictionary (indexed by i)
        data_dict[i] = create_hospital(i,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio, pop_susceptible, pop_infected, pop_recovered)

    #return hospital dictionary
    return data_dict

#simple function to print all attributes for each hospital
def print_hospital_data(hospital_dict):
    print("-----------------------")
    for i in hospital_dict.keys():
        print(f"Data for Hospital {str(i)}:")
        print(f'nurses = {hospital_dict[i].num_nurses}/{hospital_dict[i].nurse_capacity}')
        print(f"patients = {hospital_dict[i].num_patients}/{hospital_dict[i].patient_capacity}")
        print('care ratio', hospital_dict[i].num_patients/hospital_dict[i].num_nurses)
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
    '''
    #definition of the rates defining the transition in between states
    rate_susceptibletoinfected = 50                 #number of cases per day (different rates can be tested to see if they're stabilizable)
    rate_recoveredtoinfected = 1                    #random number less than sesceptibletoinfected (needs changing)
    rate_infectedtorecovered = 0.1                  #An infected individual will be sick for 10 days on average
    rate_infectedtohospitalized = 63961 / 2180000   #number of hospitalizations 2020-2021 / number of confirmed cases 2020-2021
    rate_hospitalizedtorecovered = 1/14.7           #on average hospitalized patients spent 14.7 days in the hospital
    '''

    #definition of the rates defining the transition in between states
    rate_susceptibletoinfected = 50                 #number of cases per day (different rates can be tested to see if they're stabilizable)
    rate_recoveredtoinfected = 1                    #random number less than sesceptibletoinfected (needs changing)
    rate_infectedtorecovered = 0.1 #.1/1000                  #An infected individual will be sick for 10 days on average
    rate_infectedtohospitalized = 0.5*63961 / 2180000   #number of hospitalizations 2020-2021 / number of confirmed cases 2020-2021
    rate_hospitalizedtorecovered = 1/14.7           #on average hospitalized patients spent 14.7 days in the hospital
    rate_hospitalizedtorecovered_good = 1/10        #average number of days a patient spends in the hospital when the care ratio is good
    rate_hospitalizedtorecovered_bad = 1/20         #average number of days a patient spends in the hospital when the care ratio is bad


    #isolate hospital object from dictionary
    hospital = hospital_dict[ID]
    num_patients = hospital.num_patients
    
    #Rate calculations for poisson and binomial distributions
    #average value of an exponential function is the 1/rate
    P1 = 1 - np.exp(-1*rate_infectedtorecovered)
    P2 = 1 - np.exp(-1*rate_infectedtohospitalized)
    P3 = 1 - np.exp(-1*rate_susceptibletoinfected)
    P4 = 1 - np.exp(-1*rate_recoveredtoinfected)
    P5 = 1 - np.exp(-1*rate_hospitalizedtorecovered)

    if hospital_dict[ID].num_patients/hospital_dict[ID].num_nurses > 4:
        P5 = 1 - np.exp(-1*rate_hospitalizedtorecovered_good)
    else:
        P5 = 1 - np.exp(-1*rate_hospitalizedtorecovered_bad)
    
    #Transition population
    #average value of a poisson is what's inside the brackets
    #average value of a binomial distribution is n*p (i.e. multiply the inputs) 
    if pop_susceptible < 0:
        pop_susceptible = 0
    if pop_infected < 0:
        pop_infected = 0
    if pop_infected < 0:
        pop_infected = 0
    if pop_hospitalized < 0:
        pop_hospitalized = 0
    if pop_recovered < 0:
        pop_recovered = 0
    
    infected_to_recovered = np.random.binomial(pop_infected, 1-P1)            #changed infected to pop_infected (infected isnt initialized)
    infected_to_hospitalized = np.random.binomial(pop_infected, 1-P2)
    susceptible_to_infected = np.random.poisson(rate_susceptibletoinfected)
    recovered_to_infected = np.random.poisson(rate_recoveredtoinfected)
    hospitalized_to_recovered = np.random.binomial(hospital_dict[ID].num_patients, 1-P5)

    #print(f"susceptible population = {pop_susceptible} susceptible to infected = {susceptible_to_infected} recovered to infected = {recovered_to_infected} infected to recovered = {infected_to_recovered} infected to hospitalized = {infected_to_hospitalized} hospitalized to recovered = {hospitalized_to_recovered}")

    #print(f"infected_to_recovered = {infected_to_recovered}, infected_to_hospitalized = {infected_to_hospitalized}, susceptible_to_infected = {susceptible_to_infected}, recovered_to_infected = {recovered_to_infected}, hospitalized_to_recovered = {hospitalized_to_recovered}")
    
    #Evolution of susceptible population

    hospital_dict[ID].pop_susceptible = hospital_dict[ID].pop_susceptible - susceptible_to_infected

    #Evolution of recovered people
    hospital_dict[ID].pop_recovered = hospital.pop_recovered + infected_to_recovered + hospitalized_to_recovered - recovered_to_infected

    #Evolution of infected population
    hospital_dict[ID].pop_infected = hospital_dict[ID].pop_infected + recovered_to_infected + susceptible_to_infected - infected_to_hospitalized - infected_to_recovered

    #Evolution of hospitalized population
    hospital_dict[ID].num_patients = hospital_dict[ID].num_patients + infected_to_hospitalized - hospitalized_to_recovered

    hospital_dict[ID].care_ratio = hospital.num_patients/hospital.num_nurses

    #number of hospitalized people that recover
    #X = np.random.binomial(num_patients,p_recover)
    #print('X = ' + str(X))
    #number of 
    #number of new people who get sick
    #Y = np.random.binomial(population, p_sick)
    #print("Y = " + str(Y))
    delta =  infected_to_hospitalized - hospitalized_to_recovered

    #cant have the number of patients exceed the patient capacity
    if num_patients + delta >= hospital.patient_capacity :
        hospital_dict[ID].num_patients = hospital.patient_capacity
        hospital_dict[ID].care_ratio = hospital.num_patients/hospital.num_nurses
        return hospital_dict

    if pop_susceptible < 0:
        pop_susceptible = 0
    if pop_infected < 0:
        pop_infected = 0
    if pop_infected < 0:
        pop_infected = 0
    if pop_hospitalized < 0:
        pop_hospitalized = 0
    if pop_recovered < 0:
        pop_recovered = 0

    return hospital_dict

#depreicated
def create_population_dict(keys):

    pop_dict = {}

    for i in keys:
        pop_dict[i] = random.randint(100,2000)

    return pop_dict

def get_average_care_ratio(hospital_dict):

    #get the average care ratio for all hospitals
    total = 0
    for i in hospital_dict.keys():
        if(np.isinf(hospital_dict[i].care_ratio)):
            total += 0
        if(np.isnan(hospital_dict[i].care_ratio)):
            total += 0
        else: 
            total += hospital_dict[i].care_ratio

    return total/len(hospital_dict.keys())

def print_care_ratios(hospital_dict):

    care_ratios = []

    #need a way to not have number of nurses be 0 because that causes infinite care ratios
    for i in hospital_dict.keys():
        if hospital_dict[i].care_ratio == 'inf':
            hospital_dict[i].care_ratio = 0
        if hospital_dict[i].care_ratio == 'nan':
            hospital_dict[i].care_ratio = -1
        care_ratios.append(hospital_dict[i].care_ratio)

    print('care ratios = ',care_ratios)


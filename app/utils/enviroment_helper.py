import networkx as nx
import numpy as np
import pandas as pd
import random
import math as m
import matplotlib.pyplot as plt

class Hospital:
    def __init__(self, ID, nurse_capacity, num_nurses, patient_capacity, num_patients, best_care_ratio, pop_susceptible, pop_infected, pop_recovered):
        self.ID = ID
        self.nurse_capacity = nurse_capacity
        self.num_nurses = num_nurses
        self.num_nurses_unquantized = num_nurses * 6
        self.patient_capacity = patient_capacity
        self.num_patients = num_patients
        self.best_care_ratio = best_care_ratio
        if (self.num_patients == 0):
            self.care_ratio = 0
        elif(self.num_nurses == 0): 
            self.care_ratio = self.num_patients/num_nurses
        else:
            self.care_ratio = self.num_patients/self.num_nurses
        self.pop_susceptible =  pop_susceptible
        self.pop_infected = pop_infected
        self.pop_recovered = pop_recovered


    def echo_care_ratio(self):
        print(self.care_ratio + '(' + self.num_nurses + "/" + self.num_patients + ')')

    def total_population(self):
        return self.pop_susceptible + self.pop_infected + self.pop_recovered + self.num_patients

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
    nurse_capacity = 8
    num_nurses = 4
    patient_capacity = 250
    num_patients = 0
    care_ratio = num_patients/num_nurses
    pop_susceptible = 10*10**4
    pop_infected = 0
    pop_recovered = 0

    #creates a hospital object with the given attributes for each hospital and stores it in the dictionary (indexed by i)
    data_dict[1] = create_hospital(1,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio, pop_susceptible, pop_infected, pop_recovered)

    nurse_capacity = 8
    num_nurses = 4
    patient_capacity = 250
    num_patients = 0
    care_ratio = num_patients/num_nurses
    pop_susceptible = 10*10**4
    pop_infected = 0
    pop_recovered = 0

    #creates a hospital object with the given attributes for each hospital and stores it in the dictionary (indexed by i)
    data_dict[2] = create_hospital(2,nurse_capacity, num_nurses, patient_capacity, num_patients, care_ratio, pop_susceptible, pop_infected, pop_recovered)

    #return hospital dictionary
    return data_dict

#simple function to print all attributes for each hospital
def print_hospital_data(hospital_dict):
    print("-----------------------")
    for i in hospital_dict.keys():
        print(f"Data for Hospital {str(i)}:")
        print(f'nurses (x3) = {hospital_dict[i].num_nurses}/{hospital_dict[i].nurse_capacity}')
        print(f"patients = {hospital_dict[i].num_patients}/{hospital_dict[i].patient_capacity}")
        print('care ratio', hospital_dict[i].num_patients/hospital_dict[i].num_nurses_unquantized)
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
    
    #isolate hospital object from dictionary
    #hospital = hospital_dict[ID]
    

    print(f"pop_hospitalized = {pop_hospitalized}")
    #definition of the rates defining the transition in between states
    rate_susceptibletoinfected = 1/75 * hospital_dict[ID].pop_susceptible                 #number of cases per day (different rates can be tested to see if they're stabilizable)
    rate_recoveredtoinfected = 1/1000 * hospital_dict[ID].pop_recovered                   #random number less than sesceptibletoinfected (needs changing)
    rate_infectedtorecovered = 0.1                  #An infected individual will be sick for 10 days on average
    rate_infectedtohospitalized = 1/10000#63961 / 2180000   #number of hospitalizations 2020-2021 / number of confirmed cases 2020-2021
    rate_hospitalizedtorecovered = 1/14.7           #on average hospitalized patients spent 14.7 days in the hospital
    rate_hospitalizedtorecovered_good = 1/10        #average number of days a patient spends in the hospital when the care ratio is good
    rate_hospitalizedtorecovered_bad = 1/20         #average number of days a patient spends in the hospital when the care ratio is bad


    '''
    #definition of the rates defining the transition in between states
    rate_susceptibletoinfected = 50                 #number of cases per day (different rates can be tested to see if they're stabilizable)
    rate_recoveredtoinfected = 1                    #random number less than sesceptibletoinfected (needs changing)
    rate_infectedtorecovered = 0.1 #.1/1000                  #An infected individual will be sick for 10 days on average
    rate_infectedtohospitalized = 0.5*63961 / 2180000   #number of hospitalizations 2020-2021 / number of confirmed cases 2020-2021
    rate_hospitalizedtorecovered = 1/14.7           #on average hospitalized patients spent 14.7 days in the hospital
    rate_hospitalizedtorecovered_good = 1/10        #average number of days a patient spends in the hospital when the care ratio is good
    rate_hospitalizedtorecovered_bad = 1/20         #average number of days a patient spends in the hospital when the care ratio is bad
    '''

    gamma_S2I = (1/50)*hospital_dict[ID].pop_susceptible #1/75 * 100000                 #number of cases per day (different rates can be tested to see if they're stabilizable)                   #random number less than sesceptibletoinfected (needs changing)
    gamma_I2H = 1/2000   #number of hospitalizations 2020-2021 / number of confirmed cases 2020-2021 63961 / 2180000
    gamma_I2R = 1/14              #.1/1000       #An infected individual will be sick for 10 days on average
                                                         #on average hospitalized patients spent 14.7 days in the hospital
    gamma_R2I = 1/200 * hospital_dict[ID].pop_recovered
    gamma_H2Rgood = 1/10        #average number of days a patient spends in the hospital when the care ratio is good
    gamma_H2Rbad = 1/25         #average number of days a patient spends in the hospital when the care ratio is bad

    if pop_hospitalized/(hospital_dict[ID].num_nurses_unquantized) < 4:
        P5 = gamma_H2Rgood
    else:
        P5 = gamma_H2Rbad
    
    T_S2I = np.random.poisson(gamma_S2I)            #changed infected to pop_infected (infected isnt initialized)
    T_I2H = np.random.binomial(pop_infected, gamma_I2H)
    T_I2R = np.random.binomial(pop_infected, gamma_I2R)
    T_H2R = np.random.binomial(pop_hospitalized, P5)
    T_R2I = np.random.poisson(gamma_R2I)
    print(f"T_S2I = {T_S2I}, T_I2H = {T_I2H}, T_I2R = {T_I2R}, T_H2R = {T_H2R}, T_R2I = {T_R2I}")

    if pop_susceptible - T_S2I < 0:
        T_S2I = pop_susceptible
        pop_susceptible = 0
    else:
        pop_susceptible = pop_susceptible - T_S2I

    #Evolution of infected population
    if pop_infected - T_I2H - T_I2R + T_S2I + T_R2I < 0:
        T_I2H = 0
        T_I2R = pop_infected
        pop_infected = T_S2I + T_R2I
    else:
        pop_infected = pop_infected - T_I2H - T_I2R + T_S2I + T_R2I


    #Evolution of hospitalized population
    if pop_hospitalized + T_I2H - T_H2R < 0:
        T_H2R = pop_hospitalized
        pop_hospitalized = T_I2H
    else:
        pop_hospitalized = pop_hospitalized + T_I2H - T_H2R

    #Evolution of recovered population
    if pop_recovered + T_I2R + T_H2R - T_R2I < 0:
        T_R2I = pop_recovered
        pop_recovered = T_I2R + T_H2R
    else:
        pop_recovered = pop_recovered + T_I2R + T_H2R - T_R2I

        #To run through the simulation many times we will repeat after 240 days
    if ((time_step + 1) % 240) == 0:
        pop_susceptible = pop_recovered
        pop_recovered = 0
    #print(f"susceptible population = {pop_susceptible} susceptible to infected = {susceptible_to_infected} recovered to infected = {recovered_to_infected} infected to recovered = {infected_to_recovered} infected to hospitalized = {infected_to_hospitalized} hospitalized to recovered = {hospitalized_to_recovered}")


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


    hospital_dict[ID].num_patients = pop_hospitalized
    hospital_dict[ID].pop_susceptible =  pop_susceptible
    hospital_dict[ID].pop_infected = pop_infected
    hospital_dict[ID].pop_recovered = pop_recovered

    delta =  T_I2H - T_H2R

    #cant have the number of patients exceed the patient capacity
    if hospital_dict[ID].num_patients + delta >= hospital_dict[ID].patient_capacity :
        pop_hospitalized = hospital_dict[ID].patient_capacity
        hospital_dict[ID].care_ratio = hospital_dict[ID].num_patients/hospital_dict[ID].num_nurses
        return hospital_dict

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


def plot_results(states):

    patients_1 = []
    patients_2 = []
    nurses_1 = []
    nurses_2 = []

    for i in range(len(states)):

        patients_1.append(states[i][0])
        patients_2.append(states[i][1])
        nurses_1.append(6*states[i][2])
        nurses_2.append(6*states[i][3])

    fig,axes = plt.subplots(2,2)
    
    #plot the results

    #axes[0][0].hexbin(x=np.linspace(0,len(patients_1),len(patients_1)),y=patients_1,gridsize=(50,50),cmap=plt.cm.Blues)
    axes[0][0].scatter(x=np.linspace(0,len(patients_1),len(patients_1)),y=patients_1,s=1)
    axes[0][0].set_title('Hospital 1')
    axes[0][1].scatter(x=np.linspace(0,len(patients_2),len(patients_2)),y=patients_2, s=1)
    axes[0][1].set_title('Hospital 2')
    axes[1][0].scatter(x=np.linspace(0,len(nurses_1),len(nurses_1)),y=nurses_1, s=1)

    axes[1][1].scatter(x=np.linspace(0,len(nurses_2),len(nurses_2)),y=nurses_2, s=1)

    axes[1][1].set_xlabel('Time (days)')
    axes[1][0].set_xlabel('Time (days)')
    axes[0][0].set_ylabel('Number of Patients') 
    axes[1][0].set_ylabel('number of Nurses')
    


    plt.show()

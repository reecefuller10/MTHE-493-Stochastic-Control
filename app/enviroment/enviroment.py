import networkx as nx
import numpy as np
import pandas as pd

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








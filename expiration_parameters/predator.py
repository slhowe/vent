#!/bin/bash

import matplotlib.pyplot as plt
import numpy as np

#~~~~~~~~~~~~~~~~~~
# Predator function
#~~~~~~~~~~~~~~~~~~
#
# Take pressure, flow, volume of 5 breaths
# Separate inspiration and expiration
# Normalise each half to 1s and super impose
# Pressure in inspiration takes max, others take mean

def predator(pressures, flows, volumes, sampling_frequency):

    # Data in form [[set1], [set2], ... , [setn]]
    # Start with first set
    number_of_sets = len(pressures)
    for data in range(number_of_sets):
        # find end of inspiration
        end_insp = 15
        i = end_insp
        while(i < len(flow) - 4):
            if((flow[i] < 0.01 or flow[i+1] < 0) and flow[i+4] < 0.01):
                end_insp = i
                i = len(flow)
            i += 1

        # normalise each half of data
        # resample at 0.02s intervals

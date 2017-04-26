#!/bin/bash

# Add my extensions to path
import sys
sys.path.insert(0, '/home/sarah/Documents/Spirometry/python/extensions')

# Import my extensions
from data_struct import DataStore
from breath_analysis import BreathData, split_breaths, calc_flow_delay
from calculus import integral, derivative
from filters import hamming
from split_parameters import split_parameters

#Import built-ins
import matplotlib.pyplot as plt
from math import sin, cos, pi, exp, log
from numpy import nan
import numpy as np
from scipy import io
from scipy.stats.stats import pearsonr
from numpy.linalg import lstsq

'''
Comparing model fit to expiration and inspiration
Idea is that expiration can be used as a guide for inspiration
in asynchronous regions
'''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def sedation_changes_data(mat, key, breath):

    parent_data = mat[key]
    data = parent_data['Breath'][breath][0]

    pressure = [0]*len(data)
    flow = [0]*len(data)
    volume = [0]*len(data)

    for i in range(len(data)):
        pressure[i] = data[i][1]
        flow[i] = data[i][0]
        volume[i] = data[i][2]

    return([pressure, flow, volume])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#################
# Main function #
#################
if(__name__ == '__main__'):
    # Definitions
    INSP = 0
    EXP = 1
    sampling_frequency = 50

    # Place to save plots
    plot_path = '/home/sarah/Documents/Spirometry/lungPlots/'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    path = '/home/sarah/Documents/Spirometry/data/ventilation/sedation_changes/'
    sed_filename ='SedationChanges.mat'
    filename = path + sed_filename

    # Load data from file
    mat_data = io.loadmat(filename)

    keys = [
            'P9Pre',
            'P9Post',
            'P92Pre',
            'P92Post',
            'P10Pre',
            'P10Post',
            'P11Pre',
            'P11Post',
            ]

    pre_post_signal = 0

    pre_post_E_insp = []
    pre_post_E_exp = []
    pre_post_E_other = []
    pre_post_R_insp = []
    pre_post_R_exp = []
    pre_post_R_other = []
    all_E_insp = []
    all_E_exp = []
    all_E_est = []
    all_E_est_other = []
    peep = nan
    breath_data = []

    pred_cycles = 5
    pressures = [[]]*pred_cycles
    flows = [[]]*pred_cycles
    volumes = [[]]*pred_cycles
    pred_index = 0

    trend = 1.10
    offs = 0.0

    for key in keys:

        # Specify breaths to iterate through
        first_breath = 0
        last_breath = 30

        # Make space to save results
        E_insp = []
        E_exp = []
        E_other_method = []
        R_insp = []
        R_exp = []
        R_other_method = []

        # Iterate through every breath in range specified
        for breath in range(first_breath,last_breath):
            print('\nBreath number {}\n~~~~~~~~~~~~~~~~'.format(breath))

            # Extract data for a single breath
            data = sedation_changes_data(mat_data, key, breath)

            pressure = data[0]
            flow = data[1]
            volume = data[2]

            # Predator
            if(breath < pred_cycles):
                pressures[breath] = pressure
                flows[breath] = flows
                volumes[breath] = volumes
            else:
                pressures[pred_index] = pressure
                flows[pred_index] = flow
                volumes[pred_index] = volume

            pred_index += 1
            if(pred_index == 5):
                pred_index = 0

            if(breath <= 10):
                breath_data = breath_data + pressure

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # filter data
#            flow = hamming(flow, 30, sampling_frequency, 10)
#            flow = np.real(flow).tolist()
#            pressure = hamming(pressure, 30, sampling_frequency, 10)
#            pressure = np.real(pressure).tolist()

            res = split_parameters(pressure, flow, volume, sampling_frequency, nan)

            E_insp.append(res[0])
            R_insp.append(res[1])
            E_exp.append(res[2])
            R_exp.append(res[3])

            all_E_est.append(res[2]/trend + offs)
            all_E_est_other.append(res[4]/trend + offs)

        for i in range(len(E_insp)):
            all_E_insp.append(E_insp[i])
            all_E_exp.append(E_exp[i])


            E_other_method.append(res[2])
            R_other_method.append(res[3])


        if(0):
            # Only want to do this is non-async bit
                #f, (ax1, ax2) = plt.subplots(2, sharex=True)
                f, (ax1) = plt.subplots(1, sharex=True)

                ax1.plot(E_insp, E_other_method, 'or')
                ax1.set_title('Elastance comparison')
                ax1.set_xlabel('E insp')
                ax1.set_ylabel('E exp')
                ax1.grid()

                #ax2.plot(R_insp, R_other_method, 'bd')
                #ax2.set_title('Resistance comparison')
                #ax2.set_xlabel('R insp')
                #ax2.set_ylabel('R exp')
                #ax2.grid()

                plt.show()

        # Plot results for all breaths
        if(0):
            'plot E and R for different methods'
            f, (ax1, ax2) = plt.subplots(2, sharex=True)

            ax1.plot(E_insp, 'or')
            ax1.plot(E_exp, '^b')
            ax1.plot(E_other_method , 'd', color='orange')
            ax1.legend(['Insp',
                        'Exp',
                        'Other method',
                        ])
            ax1.set_ylabel('Elastance (cmH20/L)', fontsize=16)

            ax2.plot(R_insp, 'or')
            ax2.plot(R_exp, '^b')
            ax2.plot(R_other_method , 'd', color='orange')
            ax2.legend(['Insp',
                        'Exp',
                        'Other method'
                        ])
            ax2.set_ylabel('Resistance (cmH20s/L)', fontsize=16)
            ax2.set_xlabel('Breath')

            ax1.grid()
            ax2.grid()
            plt.show()

        if(1):
            if(pre_post_signal == 1):
                plt.plot(all_E_insp, 'o')
                #plt.plot(all_E_exp, 'x')
                plt.plot(all_E_est, 'sr')
                plt.plot(all_E_est_other, 'xc')

                plt.legend([
                    'original insp',
                    #'original exp',
                    'estimated insp',
                    'other estimate',
                    ])
                plt.show()

                #all_E_insp = []
                #all_E_exp = []
                #all_E_est = []
                #all_E_est_other = []

        if(0):
            plt.plot(breath_data)
            plt.grid()
            plt.xlabel('datapoint')
            plt.ylabel('Pressure (cmH2O)')
            plt.show()

        if(0):
            # cdf plots
            data_sorted = np.sort(all_E_est)
            proportional_data = 1. * np.arange(len(all_E_est))/(len(all_E_est) - 1)
            all_E_insp = []
            all_E_exp = []
            all_E_est = []
            all_E_est_other = []

            if(pre_post_signal == 1):
                plt.grid()
                plt.plot(data_sorted, proportional_data, 'r')
                plt.xlabel('Elastance (cmH20/L)')
                plt.ylabel('Cumulative probability')
                plt.legend(['pre','post'])
                plt.show()
            else:
                plt.plot(data_sorted, proportional_data, 'b--')

        if pre_post_signal == 0:
            pre_post_signal = 1
        else:
            pre_post_signal = 0

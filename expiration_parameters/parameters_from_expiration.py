#!/bin/bash

# Add my extensions to path
import sys
sys.path.insert(0, '/home/sarah/Documents/Spirometry/python/extensions')

# Import my extensions
from data_struct import DataStore
from breath_analysis import BreathData, split_breaths, calc_flow_delay
from calculus import integral, derivative
from filters import hamming
import data_extraction as extr
from split_parameters import split_parameters
import ransac

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

    # There are different data files with different
    # data structures. This section extracts data
    # from different file types.
    using_ManualDetection_files = 1
    using_dated_files = 1
    using_PS_vs_NAVA_invasive_files = 0
    using_PS_vs_NAVA_non_invasive_files = 0
    using_daniels_sedation_changes_file = 0

    files = []
    file_types = []

    # Declare file names for ManualDetection MV data
    if(using_ManualDetection_files):
        path = '/home/sarah/Documents/Spirometry/data/ventilation/ManualDetection/'
        MD_filenames = [
                        #'ManualDetection_Patient4_PM.mat',
                        'ManualDetection_Patient14_FM.mat',
                        'ManualDetection_Patient17_FM.mat',
                        'ManualDetection_Patient8_PM.mat',
                       ]
        # Make full path names
        # Add names to list of all data
        # Add data type to data type list
        files += [path + name for name in MD_filenames]
        file_types += ['MD' for name in MD_filenames]

    # Declare file names for dated data
    if(using_dated_files):
        path = '/home/sarah/Documents/Spirometry/data/ventilation/ManualDetection/'
        DF_filenames = [
                        '12_11_08.mat',
                        '13_11_21.mat',
                        '9_04_08.mat',
                        '9_04_09.mat',
                        '9_04_10A.mat',
                       ]
        # Make full path names
        # Add names to list of all data
        # Add data type to data type list
        files += [path + name for name in DF_filenames]
        file_types += ['DF' for name in DF_filenames]

   # Declare file names for PS/Nava invasive ventilation data
    if(using_PS_vs_NAVA_invasive_files):
        path = '/home/sarah/Documents/Spirometry/data/ventilation/PS_vs_NAVA_invasive/'
        PNI_filenames = [
                         'BRU1-PS.mat',
                         'BRU2-PS.mat',
                         'BRU4-PS.mat',
                         'BRU6-PS.mat',
                         'BRU14-PS.mat',
                         'GE04-PS.mat',
                         'GE05-PS.mat',
                         'GE11-PS.mat',
                         'GE21-PS.mat',
                        ]
        # Make full path names
        # Add names to list of all data
        # Add data type to data type list
        files += [path + name for name in PNI_filenames]
        file_types += ['PNI' for name in PNI_filenames]

    # Declare file names for PS/NAVA non-invasive ventilation data
    if(using_PS_vs_NAVA_non_invasive_files):
        path = '/home/sarah/Documents/Spirometry/data/ventilation/PS_vs_NAVA_non_invasive/'
        PNN_filenames = [
                        'NIV_BRU01.mat',
                        'NIV_BRU02.mat',
                        'NIV_BRU03.mat',
                        'NIV_BRU04.mat',
                        'NIV_BRU05.mat',
                        'NIV_BRU06.mat',
                        'NIV_BRU07.mat',
                        'NIV_BRU08.mat',
                        'NIV_BRU09.mat',
                        'NIV_BRU10.mat',
                        'NIV_LIE01.mat',
                        'NIV_LIE02.mat',
                        'NIV_LIE03.mat',
                       ]
        # Make full path names
        # Add names to list of all data
        # Add data type to data type list
        files += [path + name for name in PNN_filenames]
        file_types += ['PNN' for name in PNN_filenames]

    if(using_daniels_sedation_changes_file):
        path = '/home/sarah/Documents/Spirometry/data/ventilation/sedation_changes/'
        sed_filenames = [
                        'SedationChanges.mat'
                        ]
        files += [path + name for name in sed_filenames]
        file_types += ['sed' for name in sed_filenames]

    # Go through every file declared
    file_index = 0
    all_E_insp = []
    all_E_exp = []
    for filename in files:
        print(filename)
        # Load data from file
        mat_data = extr.load_mat_file(filename)

        # Determine which file type the data came from
        file_type = file_types[file_index]
        file_index += 1

        # Data extraction for ManualDetection type data,
        if(file_type == 'MD'):
            last_breath = 470
            sampling_frequency = 50
        # Data extraction for dated ventilation data,
        elif(file_type == 'DF'):
            last_breath = 470
            sampling_frequency = 50
        # Data extraction for PS/NAVA invasive ventilation data,
        elif(file_type == 'PNI'):
            full_data = extr.PS_vs_NAVA_invasive_data(mat_data)
            full_pressure = full_data[0]
            full_flow = full_data[1]
            last_breath = len(full_flow)
            sampling_frequency = 100
        # Data extraction for PS/NAVA non-invasive ventilation data,
        elif(file_type == 'PNN'):
            full_data = extr.PS_vs_NAVA_noninvasive_data(mat_data)
            full_pressure = full_data[0]
            full_flow = full_data[1]
            last_breath = len(full_flow)
            sampling_frequency = 100
        elif(filename == 'sed'):
            pass

        # Specify breaths to iterate through
        first_breath = 0
        #last_breath = 60

        # Make space to save results
        E_insp = []
        E_exp = []
        E_other_method= []
        R_insp = []
        R_exp = []
        R_other_method= []

        # Iterate through every breath in range specified
        for breath in range(first_breath,last_breath):
            print('\nBreath number {}\n~~~~~~~~~~~~~~~~'.format(breath))

            # Data for each breath is extracted here depending on file type
            if(file_type == 'MD'):
                breath_data = extr.ManualDetection_data(mat_data, breath)
                pressure = breath_data[0]
                flow = breath_data[1]
            elif(file_type == 'DF'):
                breath_data = extr.dated_data(mat_data, breath)
                pressure = breath_data[0]
                flow = breath_data[1]
            elif(file_type == 'PNI'):
                pressure = full_pressure[breath]
                flow = full_flow[breath]
            elif(file_type == 'PNN'):
                pressure = full_pressure[breath]
                flow = full_flow[breath]

            # Get the volume
            volume = integral(flow, sampling_frequency)

            res = split_parameters(pressure, flow, volume, sampling_frequency)

            if(nan not in res):
                E_insp.append(res[0])
                R_insp.append(res[1])
                #E_other_method.append(res[2])
                #R_other_method.append(res[3])
                E_exp.append(res[4]/1.15)
                R_exp.append(res[5]/1.15)

        # Plot results for all breaths
        if(0):
            'plot E and R for different methods'
            f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

            ax1.plot(E_insp, 'or')
            ax1.plot(E_exp, '^b')
            #ax1.plot(E_other_method , 'd', color='orange')
            ax1.legend(['Insp',
                        'Exp',
                        'Other method'
                        ])
            ax1.set_ylabel('Elastance (cmH20/L)', fontsize=16)

            ax2.plot(R_insp, 'or')
            ax2.plot(R_exp, '^b')
            #ax2.plot(R_other_method , 'd', color='orange')
            ax2.legend(['Insp',
                        'Exp',
                        'Other method'
                        ])
            ax2.set_ylabel('Resistance (cmH20s/L)', fontsize=16)
            ax2.set_xlabel('Breath')

            ax3.plot([E_insp[i]/max(R_insp[i], 1e-3) for i in range(len(E_insp))], 'or')
            ax3.plot([E_exp[i]/max(R_exp[i], 1e-3) for i in range(len(E_exp))], '^b')
            #ax3.plot([E_other_method[i]/max(R_other_method[i], 1e-3)for i in range(len(E_other_method))], 'd', color='orange')
            ax3.legend(['Insp',
                        'Exp',
                        'Other method'
                        ])
            ax3.set_ylabel('E/R (s)', fontsize=16)
            ax3.set_xlabel('Breath')

            ax1.grid()
            ax2.grid()
            ax3.grid()
            plt.show()

        for i in range(len(E_insp)):
            all_E_insp.append(E_insp[i])
            all_E_exp.append(E_exp[i])

    plt.plot(all_E_insp, 'bo')
    plt.plot(all_E_exp, 'rs')
    plt.legend(['insp', 'exp'])
    plt.grid()
    plt.show()

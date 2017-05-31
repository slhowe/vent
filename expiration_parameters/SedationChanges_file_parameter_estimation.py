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
from predator import predator
from astropy.stats import median_absolute_deviation as mad

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

    end_insp = parent_data['InsEnd'][breath]

    return([pressure, flow, volume, end_insp])
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


#################
# Main function #
#################
if(__name__ == '__main__'):
    # Definitions
    INSP = 0
    EXP = 1
    PRE = 1
    POST = 0
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

    pre_post_signal = PRE

    #pre_post_E_insp = []
    #pre_post_E_exp = []
    #pre_post_E_other = []
    #pre_post_R_insp = []
    #pre_post_R_exp = []
    #pre_post_R_other = []
    all_E_insp = []
    all_E_est = []
    all_E_est_other = []
    post_E_insp = []
    post_E_exp = []
    total_breath_count = 0

    peep = nan

    # Plot 10 breaths pre- and post-sedation
    plotting_breaths = False
    if(plotting_breaths):
        breath_data = []
        all_breath_data = []

    # plot cdf of results
    plotting_cdf = 1
    if(plotting_cdf):
        f, ax = plt.subplots(4, 2, sharex=False)
        plot_index = 0

#    pred_cycles = 5
#    pressures = [[]]*pred_cycles
#    flows = [[]]*pred_cycles
#    volumes = [[]]*pred_cycles
#    pred_index = -1

    trend = 1.16
    offs = -1.16

#    E_insp = []
#    E_exp = []
#    E_other_method = []
#    R_insp = []
#    R_exp = []
#    E_est = []
#    R_other_method = []

    for key in keys:
        print('\nDataset {}\n~~~~~~~~~~~~~~~~'.format(key))

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
        E_est = []

        # Iterate through every breath in range specified
        for breath in range(first_breath,last_breath):
            total_breath_count += 1
            #print('\nBreath number {}\n~~~~~~~~~~~~~~~~'.format(breath))

            # Extract data for a single breath
            data = sedation_changes_data(mat_data, key, breath)

            pressure = data[0]
            flow = data[1]
            volume = data[2]
            end_insp = data[3][0][0][0]
            #plt.plot(pressure)
            #plt.show()

            # PREDATOR #
#            pred_index += 1
#            if(pred_index == 5):
#                pred_index = 0
#
#            # Predator
#            if(breath < pred_cycles - 1):
#                pressures[breath] = pressure
#                flows[breath] = flow
#                volumes[breath] = volume
#            else:
#                pressures[pred_index] = pressure
#                flows[pred_index] = flow
#                volumes[pred_index] = volume
#
#                new_data = predator(pressures, flows, volumes)
#                pressure = new_data[0]
#                flow = new_data[1]
#                volume = new_data[2]

            if(plotting_breaths):
                if(breath < 10):
                    breath_data = breath_data + pressure

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # filter data
    #            flow = hamming(flow, 30, sampling_frequency, 10)
    #            flow = np.real(flow).tolist()
    #            pressure = hamming(pressure, 30, sampling_frequency, 10)
    #            pressure = np.real(pressure).tolist()

            res = split_parameters(pressure,
                                    flow,
                                    volume,
                                    sampling_frequency,
                                    prev_peep=nan,
                                    end_insp=nan,
                                    printing=False)

            E_insp.append(res[0])
            R_insp.append(res[1])
            E_exp.append(res[2])
            R_exp.append(res[3])
            E_other_method.append(res[4])
            R_other_method.append(res[5])
            E_est.append((res[2] - offs)/trend)

            all_E_insp.append(res[0])
            all_E_est.append((res[2] - offs)/trend)
            all_E_est_other.append((res[4] - offs)/trend)

        # Print results
        # Median
        # Median absolute deviation
        # IQR
        qi75, qi50, qi25 = np.percentile(E_insp, [75, 50 ,25])
        madi = mad(E_insp)
        print('Inspiration:')
        print('Median:')
        print(qi50)
        print('IQR:')
        print(qi25, qi75)
        print('MAD:')
        print(madi)

        qe75, qe50, qe25 = np.percentile(E_est, [75, 50 ,25])
        made = mad(E_est)
        print('\nExpiration:')
        print('Median:')
        print(qe50)
        print('IQR:')
        print(qe25, qe75)
        print('MAD:')
        print(made)

        print('\nchange:')
        print('Median:')
        print(qe50 - qi50)
        print('IQR:')
        print(qe25-qi25, qe75-qi75)
        print('MAD:')
        print(made-madi)

        print('\ntotal breath count:')
        print(total_breath_count)

        if(plotting_breaths):
            all_breath_data.append(breath_data)
            breath_data = []

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

        if(0):
            if(pre_post_signal == PRE):
                plt.plot(all_E_insp, 'o')
                plt.plot(all_E_est, 'sr')
                #plt.plot(all_E_est_other, 'xc')

                plt.legend([
                    'original insp',
                    #'original exp',
                    'estimated insp',
                    'other estimate',
                    ])
                plt.show()

                #all_E_insp = []
                #all_E_est = []
                #all_E_est_other = []

        # Plot all post sedation elastances and store
        if(0):
            if(pre_post_signal == POST):
                for E in range(len(E_insp)):
                    post_E_insp.append(E_insp[E])
                    post_E_exp.append(E_exp[E])
                plt.plot(E_insp, E_exp, 'o')

        if(plotting_cdf):
            # cdf plots

            # Sort the elastance values
            cdf_Ee = np.sort(all_E_est)
            cdf_Ei = np.sort(all_E_insp)

            # Get list from 0->1
            proportional_data = 1. * np.arange(len(all_E_est))/(len(all_E_est) - 1)

            if(pre_post_signal == POST):
                #ax[plot_index].grid()
                ax[plot_index, 0].plot(cdf_Ei, proportional_data, 'b.-', linewidth=2)
                ax[plot_index, 1].plot(cdf_Ee, proportional_data, 'b.-', linewidth=2)
                plot_index += 1
            else:
                ax[plot_index, 0].plot(cdf_Ei, proportional_data, 'r', linewidth=2)
                ax[plot_index, 1].plot(cdf_Ee, proportional_data, 'r', linewidth=2)

            # Reset lists for next iteration
            all_E_insp = []
            all_E_est = []
            all_E_est_other = []

        if pre_post_signal == PRE:
            pre_post_signal = POST
        else:
            pre_post_signal = PRE

    # plot estimate lines over post_sedation data
    # Check if estimated relationships are close
    if(0):
        dependent = np.array([post_E_exp])
        ones = [1]*len(post_E_insp)
        independent = np.array([post_E_insp, ones])
        res = lstsq(independent.T, dependent.T)
        grad = res[0][0][0]
        offs = res[0][1][0]
        steps = range(51)
        line = [grad*s + offs for s in steps]
        print('results vvv:')
        print(grad, offs)

        dependent = np.array([post_E_exp])
        independent = np.array([post_E_insp])
        res = lstsq(independent.T, dependent.T)
        grad = res[0][0][0]
        offs = 0.0
        line2 = [grad*s + offs for s in steps]
        print(grad, offs)

        plt.plot(steps, line, 'k')
        plt.plot(steps, line2, 'g')
        line1 = [1.12*s + 0 for s in range(51)]
        line2 = [1.1*s + 0 for s in range(51)]
        line3 = [1.16*s - 1.24  for s in range(51)]
        line4 = [1.0*s + 2.24 for s in range(51)]
        plt.plot(range(51), line1, 'r:')
        plt.plot(range(51), line2, 'r--')
        plt.plot(range(51), line3, 'b:')
        plt.plot(range(51), line4, 'b--')
        plt.grid()
        plt.show()

    if(plotting_cdf):
        for (m), subplot in np.ndenumerate(ax):
            subplot.set_xlim([10,30])
            subplot.tick_params(labelsize=16)
            subplot.grid()
        plt.setp([a.get_yticklabels() for a in ax[:,1]], visible=True)

        ax[0, 1].legend([
                        'Pre sedation',
                        'Post sedation',
                        ], loc=2, fontsize=16)
        ax[0, 0].set_title('Inspiration', fontsize=20)
        ax[0, 1].set_title('Expiration', fontsize=20)

        f.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
        plt.xlabel("Elastance (cmH2O/L)", fontsize=20)
        plt.ylabel("Probability density", fontsize=20)
        plt.show()

    if(plotting_breaths):
        f, axarr = plt.subplots(4, 2)
        time = [t/float(sampling_frequency) for t in range(2000)]

        axarr[0, 0].plot(time[0:len(all_breath_data[0])], all_breath_data[0], linewidth=2)
        axarr[0, 0].set_title('Pre-sedation', fontsize=24)
        axarr[0,0].grid()

        axarr[0, 1].plot(time[0:len(all_breath_data[1])], all_breath_data[1], linewidth=2)
        axarr[0, 1].set_title('Post-sedation', fontsize=24)
        axarr[0,1].grid()

        axarr[1, 0].plot(time[0:len(all_breath_data[2])], all_breath_data[2], linewidth=2)
        axarr[1,0].grid()

        axarr[1, 1].plot(time[0:len(all_breath_data[3])], all_breath_data[3], linewidth=2)
        axarr[1,1].grid()

        axarr[2, 0].plot(time[0:len(all_breath_data[4])], all_breath_data[4], linewidth=2)
        axarr[2,0].grid()

        axarr[2, 1].plot(time[0:len(all_breath_data[5])], all_breath_data[5], linewidth=2)
        axarr[2,1].grid()

        axarr[3, 0].plot(time[0:len(all_breath_data[6])], all_breath_data[6], linewidth=2)
        axarr[3,0].grid()

        axarr[3, 1].plot(time[0:len(all_breath_data[7])], all_breath_data[7], linewidth=2)
        axarr[3,1].grid()

        for (m,n), subplot in np.ndenumerate(axarr):
            subplot.set_xlim([0,35])
            subplot.set_ylim([10,30])
            subplot.tick_params(labelsize=20)

        # Fine-tune figure; hide x ticks for top plots and y ticks for right plots
        f.add_subplot(111, frameon=False)
        plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
        plt.xlabel("Time (s)", fontsize=24)
        plt.ylabel("Pressure (cmH2O)", fontsize=24)
        plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
        plt.setp([a.get_xticklabels() for a in axarr[1, :]], visible=False)
        plt.setp([a.get_xticklabels() for a in axarr[2, :]], visible=False)
        plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)

        plt.show()

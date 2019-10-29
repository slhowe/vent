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
    plotting_cdf = True
    if(plotting_cdf):
        f, ax = plt.subplots(2, 2, sharex=False)
        x_plot_index = 0
        y_plot_index = 0

    plotting_est_and_actual_lines = False
    if(plotting_est_and_actual_lines):
        markers = ['.','x','*','+']
        mk = 0

    using_predator = False
    plot_predator = False
    rolling_predator = True
    inspiratory_predator = True
    if(using_predator):
        pred_cycles = 4

    using_threshold = True
    plotting_threshold = False
    if(using_threshold):
        P_index = 0
        P_index_max = 7
        prev_P_max_median = nan
        prev_P_max = [0]*P_index_max
        if(plotting_threshold):
            threshold_breaths = [[] for i in range(P_index_max)]
    else:
        prev_P_max_median = False

    # all the printing in this function
    printing = True

    trend = 1.04
    trend_ci = [1.03, 1.07]
    offs = 1.66
    offs_ci = [2.08, 1.06]

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

        # for predator
        if(using_predator):
            pressures = [[]]*pred_cycles
            flows = [[]]*pred_cycles
            volumes = [[]]*pred_cycles
            pred_index = 0
            ready_to_pred = False

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

            # calculate elastances for inspiratory data
            res = split_parameters(pressure,
                                    flow,
                                    volume,
                                    sampling_frequency,
                                    prev_peep=nan,
                                    end_insp=nan,
                                    printing=False,
                                    prev_P_max=prev_P_max_median)

            if(using_threshold):
                if(breath == 0):
#                    print('lookieeee')
#                    print(breath)
#                    print(res[7])
                    prev_P_max = [res[6] for k in range(P_index_max)]
                else:
                    prev_P_max[P_index] = res[6]
                prev_P_max_median = np.median(prev_P_max)
#                print(prev_P_max)
#                print(res[0])
#                print(res[2])
                if(plotting_threshold):
                    threshold_breaths[P_index] = pressure

            if(plotting_threshold):
                waveform = []
                for k in range(P_index_max):
                    waveform += threshold_breaths[P_index-k-1]
                plt.plot(waveform)
                plt.plot(range(len(waveform)), [(prev_P_max_median*0.9+res[6])]*len(waveform), '--')
                plt.xlabel('datapoint', fontsize=22)
                plt.ylabel('Pressure (cmH20)', fontsize=22)
                plt.grid()
                plt.legend(['Data', 'Threshold (90% median peak pressure)'])
                plt.show()

            # Extract results
            inspiratory_elastance = res[0]
            inspiratory_resistance = res[1]
            expiratory_elastance = res[3]
            expiratory_resistance = res[4]
            adjusted_expiratory_elastance = (expiratory_elastance - offs)/trend

            # save results that are not predator dependent
            if(not inspiratory_predator):
                E_insp.append(inspiratory_elastance)
                R_insp.append(inspiratory_resistance)
                all_E_insp.append(inspiratory_elastance)

            # PREDATOR #
            if(using_predator and (pre_post_signal == PRE or inspiratory_predator == True)):
                # rolling predator shifts one breath at a time
                if(rolling_predator):
                    if(pred_index == pred_cycles):
                        pred_index = 0
                    # Predator
                    if(breath < pred_cycles):
                        pressures[breath] = pressure
                        flows[breath] = flow
                        volumes[breath] = volume
                        # Check if all datasets are full
                        if(breath == pred_cycles-1):
                            ready_to_pred = True
                # non-rolling uses each breath only once
                else:
                    if(pred_index < pred_cycles):
                        pressures[pred_index] = pressure
                        flows[pred_index] = flow
                        volumes[pred_index] = volume
                        pred_index += 1
                        # Check if all datasets are full
                        ready_to_pred = False
                        if(pred_index == pred_cycles):
                            ready_to_pred = True

                if(ready_to_pred):
                    # Rolling needs new set each time
                    if(rolling_predator):
                        pressures[pred_index] = pressure
                        flows[pred_index] = flow
                        volumes[pred_index] = volume
                    # Get new data from predator method
                    new_data = predator(pressures, flows, volumes, plotting=plot_predator)
                    pressure_i = new_data[0]
                    flow_i = new_data[1]
                    volume_i = new_data[2]
                    pressure_e = new_data[3]
                    flow_e = new_data[4]
                    volume_e = new_data[5]
                    # Reset index for next time if batches
                    if(not rolling_predator):
                        pred_index = 0

                    res = split_parameters(pressure_e,
                                            flow_e,
                                            volume_e,
                                            sampling_frequency,
                                            prev_peep=nan,
                                            end_insp=nan,
                                            printing=False,
                                            prev_P_max=prev_P_max_median)

                    if(using_threshold):
                        if(breath == 0):
#                            print('lookieeee')
#                            print(breath)
#                            print(res[7])
                            prev_P_max = [res[6], res[6], res[6]]
                        else:
                            prev_P_max[P_index] = res[6]
                        prev_P_max_median = np.median(prev_P_max)
#                        print(prev_P_max)
#                        print(res[0])
#                        print(res[2])

                    # Extract results
                    expiratory_elastance = res[3]
                    expiratory_resistance = res[4]
                    adjusted_expiratory_elastance = (expiratory_elastance - offs)/trend

                    if(inspiratory_predator):
                        res = split_parameters(pressure_i,
                                                flow_i,
                                                volume_i,
                                                sampling_frequency,
                                                prev_peep=nan,
                                                end_insp=nan,
                                                printing=False,
                                                prev_P_max=prev_P_max_median)

                        inspiratory_elastance = res[0]
                        inspiratory_resistance = res[1]
                        E_insp.append(inspiratory_elastance)
                        R_insp.append(inspiratory_resistance)
                        all_E_insp.append(inspiratory_elastance)

                    E_exp.append(expiratory_elastance)
                    R_exp.append(expiratory_resistance)
                    E_est.append(adjusted_expiratory_elastance)
                    all_E_est.append(adjusted_expiratory_elastance)
                    all_E_est_other.append(expiratory_elastance)    # Use for looking at unadjusted Ee

                if(rolling_predator):
                    pred_index += 1
            else:
                # If not pre-sedation or using predator results, use ones from earlier
                if(inspiratory_predator):
                    E_insp.append(inspiratory_elastance)
                    R_insp.append(inspiratory_resistance)
                    all_E_insp.append(inspiratory_elastance)

                E_exp.append(expiratory_elastance)
                R_exp.append(expiratory_resistance)
                E_est.append(adjusted_expiratory_elastance)
                all_E_est.append(adjusted_expiratory_elastance)
                all_E_est_other.append(expiratory_elastance)    # Use for looking at unadjusted Ee


            if(plotting_breaths):
                if(breath < 10):
                    breath_data = breath_data + pressure


                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # filter data
    #            flow = hamming(flow, 30, sampling_frequency, 10)
    #            flow = np.real(flow).tolist()
    #            pressure = hamming(pressure, 30, sampling_frequency, 10)
    #            pressure = np.real(pressure).tolist()

            # Update indexing for threshold median
            if(using_threshold):
                P_index += 1
                if(P_index >= P_index_max):
                    P_index = 0

        # remove nan from results
        all_E_est = [x for x in all_E_est if not np.isnan(x)]
        all_E_est_other = [x for x in all_E_est_other if not np.isnan(x)]
        all_E_insp = [x for x in all_E_insp if not np.isnan(x)]

        # Print results
        # Median
        # Median absolute deviation
        # IQR
        qi75, qi50, qi25 = np.percentile(all_E_insp, [75, 50 ,25])
        madi = mad(all_E_insp)
        if(printing):
            print('Inspiration:')
            print('Median[IQR], Mad:')
            print('{0:.2f} [{1:.2f}:{2:.2f}] & {3:.2f}'.format(qi50, qi25, qi75, madi))
            print('Breaths used:')
            print(len(all_E_insp))

        if(len(all_E_est) != 0):
            qe75, qe50, qe25 = np.percentile(all_E_est, [75, 50 ,25])
            made = mad(all_E_est)
        else:
            qe75, qe50, qe25 = [nan, nan, nan]
            made = nan
        if(printing):
            print('\nExpiration:')
            print('Median[IQR], Mad:')
            print('{0:.2f} [{1:.2f}:{2:.2f}] & {3:.2f}'.format(qe50, qe25, qe75, made))
            print('Breaths used:')
            print(len(all_E_est))
            print('\n')
            print('{0:.2f} [{1:.2f}:{2:.2f}] & {3:.2f} & {4:.2f} [{5:.2f}:{6:.2f}] & {7:.2f}'.format(
                 qi50, qi25, qi75, madi, qe50, qe25, qe75, made))

#        if(printing):
#            print('\nchange:')
#            print('Median:')
#            print(qe50 - qi50)
#            print('IQR:')
#            print(qe25-qi25, qe75-qi75)
#            print('MAD:')
#            print(made-madi)

        if(printing):
            print('\ntntotal breath count:')
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
        if(plotting_est_and_actual_lines):
            if(pre_post_signal == POST):
                for E in range(len(E_insp)):
                    post_E_insp.append(E_insp[E])
                    post_E_exp.append(E_exp[E])
                plt.plot(E_insp, E_exp, linestyle='', marker=markers[mk], label='_nolegend_')
                mk+=1

        if(plotting_cdf):
            # cdf plots

            # Sort the elastance values
            cdf_Ee = np.sort(all_E_est)
            cdf_Eo = np.sort(all_E_est_other)
            cdf_Ei = np.sort(all_E_insp)
            cdf_Eci_low = [(d-offs_ci[0])/trend_ci[0] for d in all_E_est_other]
            cdf_Eci_low = np.sort(cdf_Eci_low)
            cdf_Eci_high = [(d-offs_ci[1])/trend_ci[1] for d in all_E_est_other]
            cdf_Eci_high = np.sort(cdf_Eci_high)
            cdf_worst_case_high = [e + 2.32 for e in cdf_Ee]
            cdf_worst_case_low= [e - 2.32 for e in cdf_Ee]

            # Get list from 0->1
            #expiration
            proportional_data_e = 1. * np.arange(len(all_E_est))/(len(all_E_est) - 1)
            # expiration pre-shift
            proportional_data_o = 1. * np.arange(len(all_E_est_other))/(len(all_E_est_other) - 1)
            # inspiration
            proportional_data_i = 1. * np.arange(len(all_E_insp))/(len(all_E_insp) - 1)

            if(pre_post_signal == POST):
                #ax[plot_index].grid()
                ax[x_plot_index, y_plot_index].plot(cdf_Ee, proportional_data_e, 'r--', linewidth=3)
                ax[x_plot_index, y_plot_index].plot(cdf_Ei, proportional_data_i, 'g-.', linewidth=3)
               # ax[x_plot_index, y_plot_index].plot(cdf_Eo, proportional_data_e, 'b--', linewidth=2)
               # ax[x_plot_index, y_plot_index].plot(cdf_Eci_low, proportional_data_e, 'k:', linewidth=2, label='_nolegend_')
               # ax[x_plot_index, y_plot_index].plot(cdf_Eci_high, proportional_data_e, 'k:', linewidth=2, label='_nolegend_')
                x_plot_index += 1
                if(x_plot_index >= 2):
                    x_plot_index = 0
                    y_plot_index = 1
            else:
               # ax[x_plot_index, y_plot_index].plot(cdf_Ei, proportional_data_i, 'm', linewidth=3)
               # ax[x_plot_index, y_plot_index].plot(cdf_Eo, proportional_data_e, 'b', linewidth=2)
                ax[x_plot_index, y_plot_index].plot(cdf_Ee, proportional_data_e, 'b', linewidth=3)
                ax[x_plot_index, y_plot_index].plot(cdf_worst_case_high, proportional_data_e, 'k:')
                ax[x_plot_index, y_plot_index].plot(cdf_worst_case_low, proportional_data_e, 'k:', label='_nolegend_')
               # ax[x_plot_index, y_plot_index].plot(cdf_Eci_low, proportional_data_e, 'k:', linewidth=2, label='_nolegend_')
               # ax[x_plot_index, y_plot_index].plot(cdf_Eci_high, proportional_data_e, 'k:', linewidth=2, label='_nolegend_')

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
    if(plotting_est_and_actual_lines):
        # line thorugh data from zero
        dependent = np.array([post_E_exp])
        ones = [1]*len(post_E_insp)
        independent = np.array([post_E_insp, ones])
        res = lstsq(independent.T, dependent.T)
        grad = res[0][0][0]
        offs = res[0][1][0]
        steps = range(51)
        line = [grad*s + offs for s in steps]
        if(printing):
            print('results vvv:')
            print(grad, offs)

        # line thorugh data from wherever
        dependent = np.array([post_E_exp])
        independent = np.array([post_E_insp])
        res = lstsq(independent.T, dependent.T)
        grad = res[0][0][0]
        offs = 0.0
        line2 = [grad*s + offs for s in steps]
        if(printing):
            print(grad, offs)

        plt.plot(steps, line, 'k', linewidth=3)

        line1 = [1.06*s + 1.05 for s in range(51)]
        #line2 = [1.1*s + 0 for s in range(51)]
        #line3 = [1.16*s - 1.24  for s in range(51)]
        #line4 = [1.0*s + 2.24 for s in range(51)]
        plt.plot(range(51), line1, 'r--', linewidth=3)
        #plt.plot(range(51), line2, 'r--')
        #plt.plot(range(51), line3, 'b:')
        #plt.plot(range(51), line4, 'b--')
        plt.tick_params(labelsize=16)
        plt.xlim([10, 40])
        plt.ylim([10, 40])
        plt.xlabel('Inspiratory elastance (cmH2O/L)', fontsize=20)
        plt.ylabel('Expiratory elastance (cmH2O/L)', fontsize=20)
        plt.legend(['Best fit for all data',
                    'Relationship from RM'])
        plt.grid()
        plt.show()

    if(plotting_cdf):
        for (m), subplot in np.ndenumerate(ax):
            subplot.set_xlabel("Elastance (cmH2O/L)", fontsize=20)
            subplot.set_ylabel("Probability density", fontsize=20)
            subplot.tick_params(labelsize=16)
            subplot.grid()
        plt.setp([a.get_yticklabels() for a in ax[:,1]], visible=True)

        ax[0, 0].set_xlim([0,40])
        ax[0, 1].set_xlim([0,40])
        ax[1, 0].set_xlim([0,40])
        ax[1, 1].set_xlim([0,40])

        ax[0, 0].legend([
                  #  'Pre', 'Post',
                        'Expiration pre',
                        'Prediction interval',
                        'Expiration post',
                        'Inspiration post',
                        ], loc=2, fontsize=15)
        ax[0, 0].set_title('(a)', fontsize=20)
        ax[0, 1].set_title('(b)', fontsize=20)
        ax[1, 0].set_title('(c)', fontsize=20)
        ax[1, 1].set_title('(d)', fontsize=20)

        #f.add_subplot(111, frameon=False)
        #plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
        #plt.xlabel("Elastance (cmH2O/L)", fontsize=20)
        #plt.ylabel("Probability density", fontsize=20)
        plt.show()

    if(plotting_breaths):
        f, axarr = plt.subplots(4, 2)
        time = [t/float(sampling_frequency) for t in range(5500)]

        axarr[0, 0].plot(time[0:len(all_breath_data[0])], all_breath_data[0], linewidth=2)
        axarr[0, 0].grid()
        axarr[0, 0].set_xlim([0,35])
        axarr[0, 0].set_ylim([0,30])

        axarr[0, 1].plot(time[0:len(all_breath_data[1])], all_breath_data[1], linewidth=2)
        axarr[0, 1].grid()
        axarr[0, 1].set_xlim([0,35])
        axarr[0, 1].set_ylim([0,30])

        axarr[1, 0].plot(time[0:len(all_breath_data[2])], all_breath_data[2], linewidth=2)
        axarr[1, 0].grid()
        axarr[1, 0].set_xlim([0,35])
        axarr[1, 0].set_ylim([0,30])

        axarr[1, 1].plot(time[0:len(all_breath_data[3])], all_breath_data[3], linewidth=2)
        axarr[1, 1].grid()
        axarr[1, 1].set_xlim([0,35])
        axarr[1, 1].set_ylim([0,30])

        axarr[2, 0].plot(time[0:len(all_breath_data[4])], all_breath_data[4], linewidth=2)
        axarr[2, 0].grid()
        axarr[2, 0].set_xlim([0,35])
        axarr[2, 0].set_ylim([0,30])

        axarr[2, 1].plot(time[0:len(all_breath_data[5])], all_breath_data[5], linewidth=2)
        axarr[2, 1].grid()
        axarr[2, 1].set_xlim([0,35])
        axarr[2, 1].set_ylim([0,30])

        axarr[3, 0].plot(time[0:len(all_breath_data[6])], all_breath_data[6], linewidth=2)
        axarr[3, 0].grid()
        axarr[3, 0].set_xlim([0,35])
        axarr[3, 0].set_ylim([0,30])

        axarr[3, 1].plot(time[0:len(all_breath_data[7])], all_breath_data[7], linewidth=2)
        axarr[3, 1].grid()
        axarr[3, 1].set_xlim([0,35])
        axarr[3, 1].set_ylim([0,30])

        for (m,n), subplot in np.ndenumerate(axarr):
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

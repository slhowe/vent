#!/bin/bash

import sys
sys.path.insert(0, '/home/sarah/Documents/Spirometry/python/extensions')

import RM_data_read as dr
from split_parameters import split_parameters
from calculus import integral
import ransac
import random

import matplotlib.pyplot as plt
import numpy as np
from numpy import mean
from numpy import nan
from numpy.linalg import lstsq
import itertools
from scipy import stats

filenames = [
            'Patient 1a',
            'Patient 1b',
            'Patient 1c',
            'Patient 1d',
            'Patient 1e',
#            'Patient 1f',
#            'Patient 1g',
#            'Patient 1h',
#            'Patient 1i',
            'Patient 2a',
            'Patient 2b',
            'Patient 3a',
            'Patient 3b',
            #'Patient 3c',
            'Patient 4a',
            'Patient 4b',
            'Patient 4c',
            'Patient 4d',
            'Patient 4e',
            ]

data_files = [
            # MVB001
             'RM-7.13.34.192.txt',
             'RM-10.28.22.406.txt',
             'RM-9.40.12.511.txt',
             'RM-11.28.11.503.txt',
             'RM-1.58.37.25.txt',
#            'RM-5.05.05.785.txt',
#             'RM-8.48.21.970.txt', # only 8 breaths
#             'RM-8.49.35.366.txt',
#             'RM-8.56.18.913.txt',
             # MVB002
             'RM-3.30.00.801.txt',
#             'RM-11.08.46.586.txt', # excluded. water in pipes? Very wobbly
             'RM-8.39.35.505.txt', # very tiny wobbles, veers off trend line??
            #MVB003
#             'RM-1.13.20.568.txt', # not volume control w ramp flow?
             'RM-12.15.24.824.txt', # dips in exp pressure, flow (VC)
             'RM-12.28.51.827.txt', # dips in exp pressure, flow (VC)
#             'RM-5.34.33.870.txt', # flow async in insp?
#             'RM-5.35.15.999.txt', # flow async in insp
            # SPV001
#             'RM-2.12.38.582.txt', # pneumonia, long exp, weird insp
             'RM-3.09.32.928.txt',
             'RM-3.16.36.544.txt',
             'RM-5.38.55.203.txt', # 13 breaths
             'RM-5.40.31.221.txt',
             'RM-5.43.34.113.txt',

#            'MBV001', 'MBV002a', 'MBV002b', 'MBV003b', 'MBV003d', 'SPV001b', 'SPV001c', 'SPV001e', 'SPV001f',
             ]
sampling_frequency = 50
peep = nan

fig = plt.figure()

all_E_insp = []
all_E_exp = []

total_breath_count = 0
set_breath_count = 0
total_breaths = 1380 # Check this if different data sets are used
total_datasets = 14 # Check this if different data sets are used
set_breaths = [85, 77, 78, 82, 176, 77, 78, 253, 182, 115, 75, 13, 44, 45]
bad_breath = [[] for i in range(total_datasets)]

# For plotting different sets
markers = ['+', '.', '1', '2', '3', '4', 'x']
mk = 0

plotting_results = 1
plotting_error_lines = 0
through_zero = False

if(plotting_error_lines):
    # How many sets to use when making the error sets
    num_error_sets = 1000
    size_error_sets = 30
    E_insp_error = [0]*size_error_sets
    E_exp_error = [0]*size_error_sets
    error_grads = [0]*num_error_sets
    error_offs = [0]*num_error_sets
    error_pressure = []
    error_flow = []
    # Stores grad, offset, R value for each set
    error_line_data = [[0,0,0] for i in range(num_error_sets)]

data_file_index = -1
for data_file in data_files:
    data_file_index += 1
    store = dr.Storage()
    store.extract_data(data_file)

    E_insp = []
    E_exp = []
    R_insp = []
    R_exp = []
    peeps = []

    # Split parameters for inspiration and expiration
    for breath in dr.Breaths:
        total_breath_count += 1
        set_breath_count += 1

        volume = integral(breath.flow, sampling_frequency)
        res = split_parameters(breath.pressure, breath.flow, volume, sampling_frequency, peep, printing=False)
        #E_insp.append(res[0])
        #E_exp.append(res[4])
        peep = res[6]

        if not nan in res:
            R_insp.append(res[1])
            R_exp.append(res[3])
            #R_exp.append(res[5])
            E_insp.append(res[0])
            E_exp.append(res[4])
            #E_exp.append(res[4])
            peeps.append(res[6])
        else:
            bad_breath[data_file_index].append(set_breath_count-1)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # plotting individual patients separately
    if(plotting_results):
        plt.plot(E_insp, E_exp, linestyle='', marker = markers[mk], label='_nolegend_')
        mk+=1
        if mk >= len(markers):
                mk = 0

    for i in range(len(E_insp)):
        all_E_insp.append(E_insp[i])
        all_E_exp.append(E_exp[i])

    print('\nbreaths this set:')
    print(set_breath_count)
    set_breath_count = 0
    store.clean_up()

E_insp_inliers = all_E_insp
E_exp_inliers = all_E_exp

dependent = np.array([E_exp_inliers])
if(through_zero):
    independent = np.array([E_insp_inliers])
else:
    ones = [1]*len(E_insp_inliers)
    independent = np.array([E_insp_inliers, ones])
res = lstsq(independent.T, dependent.T)
grad = res[0][0][0]
if(through_zero):
    offs = 0.0
else:
    offs = res[0][1][0]
print(res)
print(grad)
print(offs)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~####

steps = range(51)
line = [grad*s + offs for s in steps]
est = [grad*ei for ei in E_insp_inliers]

#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#def squared_error(ys_orig,ys_line):
#    value = sum([(ys_line[j] - ys_orig[j]) * (ys_line[j] - ys_orig[j]) for j in range(len(ys_line))])
#    return value
#
#def coefficient_of_determination(ys_orig,ys_line):
#    y_mean_line = [mean(ys_orig) for y in ys_orig]
#    squared_error_regr = squared_error(ys_orig, ys_line)
#    squared_error_y_mean = squared_error(ys_orig, y_mean_line)
#    return 1 - (squared_error_regr/squared_error_y_mean)
#
#
#r_value= coefficient_of_determination(E_exp_inliers,est)
#print('vvvvvvvvvvvv')
#print(r_value)
#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

gradient, intercept, r_value, p_value, std_err = stats.linregress(E_insp_inliers, E_exp_inliers)
line2 = [gradient*s + intercept for s in steps]
print('vvvvvvvvvvvv')
print(gradient)
print(intercept)
print(r_value)
print(p_value)

print('\ntotal breath count:')
print(total_breath_count)

# Work out error lines at 5th and 95th percentile of many example subsets
if(plotting_error_lines):
    for m in range(num_error_sets):
        for j in range(size_error_sets):
            # Get E of a bunch of random breaths
            # Replace random selection
            # Means could have same breath multiple times
            chose_bad_breath = True
            while(chose_bad_breath):
                # N = randint(a, b) -> a <= N <= b (as integer)
                rand_dataset = random.randint(0,total_datasets - 1)
                rand_breath = random.randint(0,set_breaths[rand_dataset] - 1)

                # Breaths on peep change give weird results
                # These breaths are recorded earlier
                # Make sure these breaths aren't used
                if rand_breath not in bad_breath[rand_dataset]:
                    chose_bad_breath = False

            data_file = data_files[rand_dataset]
            store = dr.Storage()
            store.extract_data(data_file)

            breath = store.breath_list[rand_breath]

            volume = integral(breath.flow, sampling_frequency)

            print('getting results for set {}, breath {}'.format(m, j))
            #print(rand_dataset)
            #print(set_breaths[rand_dataset])
            #print(set_breaths)
            #print(len(store.breath_list))
            res = split_parameters(breath.pressure,
                                    breath.flow,
                                    volume,
                                    sampling_frequency,
                                    prev_peep=nan,
                                    printing=False)

            # Have E for new subset
            #print(rand_dataset, rand_breath)
            #print(bad_breath[rand_dataset])
            E_insp_error[j] = res[0]
            #print(res[0])
            E_exp_error[j] = res[4]
            #print(res[4])

        # get line for the new dataset
        dependent = np.array([E_exp_error])
        if(through_zero):
            independent = np.array([E_insp_error])
        else:
            ones = [1]*len(E_insp_error)
            independent = np.array([E_insp_error, ones])
        res = lstsq(independent.T, dependent.T)
        print(res)

        print(E_insp_error)
        print('gradient and offset:')

        error_grads[m] = res[0][0][0]
        if(through_zero):
            error_offs[m] = 0.0
            print(res[0][0][0], 0)
        else:
            error_offs[m] = res[0][1][0]
            print(res[0][0][0], res[0][1][0])

        # show all datasets on top of eachother
        if(0):
            # plot new dataset
            error_line = [error_grads[m]*s + error_offs[m] for s in range(51)]
            plt.plot(E_insp_error, E_exp_error, linestyle='', marker = markers[mk], label='_nolegend_')
            mk += 1
            if mk >= len(markers):
                mk = 0

            plt.plot(range(51), error_line)

        # empty the data store, otherwise issues...
        store.clean_up()

    # Find 2.5 and 97.5 percentile at every x value
    x_points = [0]*num_error_sets
    curve975 = [0]*51
    curve25 = [0]*51
    for x in range(51):
        for index in range(num_error_sets):
            #find y=mx+c for every m, c
            x_points[index] = error_grads[index]*x + error_offs[index]
        # find percentiles for that x
        res = np.percentile(x_points, [2.5, 97.5])
        curve975[x] = res[0]
        curve25[x] = res[1]

    # find 5th, 50th, 95th percentile of all lines
    res = np.percentile(error_grads, [2.5, 50, 97.5])
    print('Percentiles of gradients:')
    print(res)
    print('error gradients:')
    print(error_grads)

#    if through_zero:
#        offs25 = 0.0
#        offs975 = 0.0
#    else:
#        offs_array = [E_exp_inliers[v] - res[0]*E_insp_inliers[v] for v in range(len(E_insp_inliers))]
#        #plt.plot(offs_array, 'o')
#        offs25 = np.median(offs_array)
#
#        offs_array = [E_exp_inliers[v] - res[2]*E_insp_inliers[v] for v in range(len(E_insp_inliers))]
#        #plt.plot(offs_array, 'o')
#        offs975 = np.median(offs_array)

    grads25 = res[0]
    grads975 = res[2]

    res = np.percentile(error_offs, [2.5, 50, 97.5])
    print('Percentiles of offsets:')
    print(res)
    print('error offsets:')
    print(error_offs)

    offs25 = res[0]
    offs975 = res[2]

    #error_line25 = [grads25*s + offs25 for s in range(51)]
    print('2.5th:')
    print(grads25)
    print(offs25)

    #error_line975 = [grads975*s + offs975 for s in range(51)]
    print('97.5th:')
    print(grads975)
    print(offs975)

    print('actual')
    print(grad)
    print(offs)

    print('rvalue')
    print(r_value)

if(plotting_results):
    ax = fig.add_subplot(111)
    #plt.plot(all_E_insp, all_E_exp, 'xb')
    #plt.plot(E_insp_inliers, E_exp_inliers, 'k,')
    #plt.plot(ransac_fit)
    plt.plot(steps, line, 'r', linewidth=2)
    if(plotting_error_lines):
        #plt.plot(steps, error_line5, 'r--', linewidth=2)
        #plt.plot(steps, error_line95, 'r--', linewidth=2)
        plt.plot(steps, curve975, 'r--', linewidth=2)
        plt.plot(steps, curve25, 'r--', linewidth=2)
    plt.plot(steps, line2, 'k:', linewidth=2)
    plt.ylabel('Expiratory elastance (cmH2O/L)', fontsize=20)
    plt.xlabel('Inspiratory elastance (cmH2O/L)', fontsize=20)
    ax.annotate('E$_e$ = {0:.2f}*E$_i$ + {1:.2f}\n\n'.format(grad, offs),
                    xy=(1, 0), xycoords='axes fraction', fontsize=22,
                    xytext=(-5, 5), textcoords='offset points',
                    ha='right')
    ax.annotate('R$^2$ = {0:.2f}'.format(r_value**2),
                    xy=(1, 0), xycoords='axes fraction', fontsize=22,
                    xytext=(-5, 5), textcoords='offset points',
                    ha='right', va='bottom')
    plt.grid()
    plt.ylim([10, 50])
    plt.xlim([10, 50])
    plt.legend(['best fit', '95% confidence band'], fontsize=16)
    plt.show()

    # Error line on estimation
    Error = [0]*len(all_E_insp)
    Estimates = [0]*len(all_E_insp)

    for i in range(len(all_E_insp)):
        estimate = (all_E_exp[i])/grad
        actual = all_E_insp[i]
        difference = (actual - estimate)
        Estimates[i] = (estimate)
        Error[i] = (difference)

    sample_mean = np.mean(Error)
    sample_var = [(E-sample_mean)**2 for E in Error]
    sample_var = np.mean(sample_var)
    std_dev = np.sqrt(sample_var)
    print(std_dev)

    std_error = [e/std_dev for e in Error]

    #plt.hist(Error, 215, alpha=0.8)
    plt.plot(Estimates, Error, '.')
    plt.plot(range(50), [0]*50, 'k--')
    plt.xlabel('Estimated inspiratory elastance (cmH2O)', fontsize=18)
    plt.ylabel('Residuals', fontsize=18)
    plt.show()

#!/bin/bash

import sys
sys.path.insert(0, '/home/sarah/Documents/Spirometry/python/extensions')

import RM_data_read as dr
from split_parameters import split_parameters
from calculus import integral
import ransac

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
            'Patient 3c',
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
#             'RM-5.05.05.785.txt',
#             'RM-8.48.21.970.txt', # only 8 breaths
#             'RM-8.49.35.366.txt',
#             'RM-8.56.18.913.txt',
             # MVB002
             #'RM-3.30.00.801.txt',
#             'RM-11.08.46.586.txt', # excluded. water in pipes? Very wobbly
             #'RM-8.39.35.505.txt', # very tiny wobbles, veers off trend line??
            #MVB003
             'RM-1.13.20.568.txt',
             'RM-12.15.24.824.txt', # dips in exp pressure, flow (VC)
             #'RM-12.28.51.827.txt', # dips in exp pressure, flow (VC)
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

all_E_insp = []
all_E_exp = []

markers = ['+', '.', '*', '^', 'v', '<', '>', 'x', 'o', 's', 'd']
mk = 0

for data_file in data_files:
    store = dr.Storage()
    store.extract_data(data_file)

    E_insp = []
    E_exp = []
    R_insp = []
    R_exp = []
    peeps = []

    # Split parameters for inspiration and expiration
    for breath in dr.Breaths:
        volume = integral(breath.flow, sampling_frequency)
        res = split_parameters(breath.pressure, breath.flow, volume, sampling_frequency, peep)
        #E_insp.append(res[0])
        #E_exp.append(res[4])
        peep = res[6]

        if not nan in res:
            R_insp.append(res[1])
            R_exp.append(res[3])
            #R_exp.append(res[5])
            E_insp.append(res[0])
            E_exp.append(res[2])
            #E_exp.append(res[4])
            peeps.append(res[6])


    # Can 'optimum' PEEP be found from resistances?
    if(0):
        f, (ax1) = plt.subplots(1)
        plt.plot(breath.pressure, volume, 'ro-')
        plt.show()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Line fit to each data set individually
    if(0):
        E_insp_ary = [[E] for E in E_insp]
        E_exp_ary = [[E] for E in E_exp]

        all_data = np.hstack((E_insp_ary, E_exp_ary))
        n_samples = len(E_insp)
        input_columns = range(1)
        output_columns = [1+i for i in range(1)]
        model = ransac.LinearLeastSquaresModel(input_columns, output_columns, debug=False)

        ransac_fit, ransac_data = ransac.ransac(all_data,model,
                                         10, 800, 2e1, 20,
                                         debug=False, return_all=True)

        E_insp_inliers = [E_insp_ary[i][0] for i in ransac_data['inliers']]
        E_exp_inliers = [E_exp_ary[i][0] for i in ransac_data['inliers']]

        dependent = np.array([E_exp_inliers])
        independent = np.array([E_insp_inliers])
        res = lstsq(independent.T, dependent.T)
        grad_e = res[0][0][0]
        offs_e = 0
        print(res)
        print(grad_e)
        print(offs_e)

        steps = range(50)
        line_e = [grad_e*s + offs_e for s in steps]

        R_insp_inliers = []
        R_exp_inliers = []
        i = 0
        for E in E_insp:
            if E in E_insp_inliers:
                R_insp_inliers.append(R_insp[i])
                R_exp_inliers.append(R_exp[i])
            i += 1

        dependent = np.array([R_exp_inliers])
        ones = [1]*len(R_insp_inliers)
        independent = np.array([R_insp_inliers, ones])
        res = lstsq(independent.T, dependent.T)
        grad_r = res[0][0][0]
        offs_r = res[0][1][0]
        print(res)
        print(grad_r)
        print(offs_r)

        line_r = [grad_r*s + offs_r for s in steps]

        f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

        ax1.plot(E_insp, 'ro')
        ax1.plot(E_exp, 'b^')
        ax1.set_ylabel('Elastance (cmH20/L)', fontsize=16)
        ax1.legend(['Inspiration', 'Expiration'], fontsize=16)
        ax1.grid()

        ax2.plot(R_insp, 'ro')
        ax2.plot(R_exp, 'b^')
        ax2.set_ylabel('Resistance (cmH20s/L)', fontsize=16)
        ax2.legend(['Inspiration', 'Expiration'], fontsize=16)
        ax2.grid()

        ax3.plot(peeps)
        ax3.set_ylabel('PEEP (cmH20)', fontsize=16)
        ax3.set_xlabel('Breath', fontsize=16)
        ax3.grid()
        plt.show()

        f, (ax1, ax2) = plt.subplots(2, sharex=False)

        ax1.plot(E_insp, E_exp, 'o')
        ax1.plot(E_insp_inliers, E_exp_inliers, 'rx')
        ax1.plot(steps, line_e)
        ax1.grid()
        ax1.set_ylabel('Expiratory Elastance (cmH20/L)', fontsize=16)
        ax1.set_xlabel('Inspiratory Elastance (cmH20/L)', fontsize=16)
        ax1.legend([
            'Data',
            'RANSAC inliers',
            ], fontsize=16)

        ax2.plot(R_insp, R_exp, 'o')
        ax2.plot(R_insp_inliers, R_exp_inliers, 'rx')
        ax2.plot(steps, line_r)
        ax2.grid()
        ax2.set_ylabel('Expiratory Resistance (cmH20s/L)', fontsize=16)
        ax2.set_xlabel('Inspiratory Resistance (cmH20s/L)', fontsize=16)
    #    ax2.legend(['Points',
    #                'Inliers',
    #                'gradient:{:.2f}, offset:{:.2f}'.format(grad, offs)])
        plt.show()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Look at RC

    #    f, (ax1) = plt.subplots(1, sharex=False)
    #    ax1.plot([E_insp[i]/R_insp[i] for i in range(len(E_insp))], 'ro')
    #    ax1.plot([E_exp[i]/R_exp[i] for i in range(len(E_exp))], 'b^')
    #    ax1.set_ylabel('E/R (cmH20s/L)', fontsize=16)
    #    ax1.set_xlabel('Breath', fontsize=16)
    #    ax1.legend(['Insp', 'Exp'], fontsize=16)
    #    ax1.grid()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RANSAC and linear fit to scatter data
    if(1):
        plt.plot(E_insp, E_exp, linestyle='', marker = markers[mk])
        mk+=1
        if mk >= len(markers):
                mk = 0

        for i in range(len(E_insp)):
            all_E_insp.append(E_insp[i])
            all_E_exp.append(E_exp[i])

    store.clean_up()

## Line fit to Ei vs Em
#E_insp_ary = [[E] for E in all_E_insp]
#E_exp_ary = [[E] for E in all_E_exp]
#
#all_data = np.hstack((E_insp_ary, E_exp_ary))
#n_samples = len(E_insp)
#input_columns = range(1)
#output_columns = [1+i for i in range(1)]
#model = ransac.LinearLeastSquaresModel(input_columns, output_columns, debug=False)
#
## ransac(data, model, n, k t, d)
## n - min num data values to fit model
## k - mak iterations
## t - fitting threshold value
## d - closest data points to check model fit
#ransac_fit, ransac_data = ransac.ransac(all_data,model,
#                                 40, 500, 1e1, 100,
#                                 debug=False, return_all=True)
#
#E_insp_inliers = [E_insp_ary[i][0] for i in ransac_data['inliers']]
#E_exp_inliers = [E_exp_ary[i][0] for i in ransac_data['inliers']]

E_insp_inliers = all_E_insp
E_exp_inliers = all_E_exp

dependent = np.array([E_exp_inliers])
ones = [1]*len(E_insp_inliers)
independent = np.array([E_insp_inliers])
res = lstsq(independent.T, dependent.T)
grad = res[0][0][0]
offs = 0.0
print(res)
print(grad)
print(offs)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~####
#grad = 1.1545
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~####

steps = range(51)
line = [grad*s + offs for s in steps]
est = [grad*ei for ei in E_insp_inliers]

#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
def squared_error(ys_orig,ys_line):
    value = sum([(ys_line[j] - ys_orig[j]) * (ys_line[j] - ys_orig[j]) for j in range(len(ys_line))])
    return value

def coefficient_of_determination(ys_orig,ys_line):
    y_mean_line = [mean(ys_orig) for y in ys_orig]
    squared_error_regr = squared_error(ys_orig, ys_line)
    squared_error_y_mean = squared_error(ys_orig, y_mean_line)
    return 1 - (squared_error_regr/squared_error_y_mean)


r_squared = coefficient_of_determination(E_exp_inliers,est)
print('vvvvvvvvvvvv')
print(r_squared)
#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'

gradient, intercept, r_value, p_value, std_err = stats.linregress(E_insp_inliers, E_exp_inliers)
line2 = [gradient*s + intercept for s in steps]
print('vvvvvvvvvvvv')
print(gradient)
print(intercept)
print(r_value**2)
print(p_value)

#plt.plot(all_E_insp, all_E_exp, 'xb')
#plt.plot(E_insp_inliers, E_exp_inliers, 'k,')
#plt.plot(ransac_fit)
plt.plot(steps, line, 'r', linewidth=2)
plt.plot(steps, line2, 'r:', linewidth=2)
plt.ylabel('Expiratory elastance (cmH2O/L)', fontsize=18)
plt.xlabel('Inspiratory elastance (cmH2O/L)', fontsize=18)
plt.grid()
plt.ylim([10, 50])
plt.xlim([10, 50])
plt.legend(filenames, fontsize=16)
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

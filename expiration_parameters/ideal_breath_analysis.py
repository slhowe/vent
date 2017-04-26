#!/bin/bash

import sys
sys.path.insert(0, '/home/sarah/Documents/Spirometry/python/extensions')

from calculus import integral, derivative
import ransac

import matplotlib.pyplot as plt
import numpy as np
from numpy import nan
from numpy.linalg import lstsq

# The constants for the data
P = [8.64, 12.474, 20.168064]
E = [17.28, 24.948, 40.336128]
Ee = [8.64/0.4, 39.0, 58.0]
#E = Ee
R = [2.592, 3.7422, 6.0504192]
Re = [3.98765, 2.2, 3.5]
#R = Re
PEEP = 0
SAMPLING_FREQ = 550
exp_len = 2 * SAMPLING_FREQ
insp_len = int(1.0 * SAMPLING_FREQ)

LIN = 0
EXP = 1
SIN = 2

flow_mode = LIN

print('For each, PC = ')
print(P[0]/E[0])
print(P[1]/E[1])
print(P[2]/E[2])
print(P[0]/Ee[0])
print(P[1]/Ee[1])
print(P[2]/Ee[2])
print('For each, 1/RC = ')
print(E[0]/R[0])
print(E[1]/R[1])
print(E[2]/R[2])
print(Ee[0]/Re[0])
print(Ee[1]/Re[1])
print(Ee[2]/Re[2])
print('\n')
w = 0.2*np.pi

for i in range(len(P)):
    print('New Example')
    #Generate some data
    print("E: {}".format(E[i]))
    print("R: {}".format(R[i]))
    print("P: {}\n".format(P[i]))

    times = [t/float(SAMPLING_FREQ) for t in range(insp_len + exp_len)]

    if(flow_mode == LIN):
        volume_in = [(-P[i]/E[i]*(t - 1)**2 + P[i]/E[i]) for t in times[:insp_len]]
        for j in range(1, insp_len):
            if(volume_in[j] - volume_in[j-1] < 0):
                volume_in[j] = P[i]/E[i]
        volume_end = volume_in[-1] + (volume_in[-1]*np.exp(-1/float(SAMPLING_FREQ)/(R[i]/E[i])) - volume_in[-1])/2.0

        flow_in = derivative(volume_in+[volume_end], SAMPLING_FREQ)
        print('grad: {}'.format((flow_in[15]-flow_in[5])*SAMPLING_FREQ/10.0))
        flow_in = [0] + flow_in[:-1]
        flow_end = flow_in[-1]

        pressures_in = [E[i]*volume_in[j] + R[i]*flow_in[j] + PEEP for j in range(insp_len)]

    elif(flow_mode == EXP):
        pressures_in = [P[i] - PEEP]*insp_len

        flow_in = [-((PEEP - P[i])/R[i])*np.exp(-t/(R[i]/E[i])) for t in times[:insp_len]]
        flow_end = -((PEEP - P[i])/R[i])*np.exp(-(insp_len)/float(SAMPLING_FREQ)/(R[i]/E[i]))

        volume_in = [((PEEP - P[i])/E[i])*np.exp(-t/(R[i]/E[i])) + P[i]/E[i] for t in times[:insp_len]]
        #volume_end = ((PEEP - P[i])/E[i])*np.exp(-(insp_len-1)/float(SAMPLING_FREQ)/(R[i]/E[i])) + P[i]/E[i]
        volume_end = volume_in[-1]*np.exp(-1/float(SAMPLING_FREQ)/(Re[i]/Ee[i]))

    elif(flow_mode == SIN):
        QMULT = 4.1
        VMULT = 1
        print('omega: {}'.format(w))
        flow_in = [QMULT*np.sin(w*t) + 0.0*np.cos(w*t) for t in times[:insp_len]]

        volume_in = integral(flow_in, SAMPLING_FREQ)

        pressures_in = [E[i]*volume_in[j] + R[i]*flow_in[j] for j in range(insp_len)]

    #volume_out = [volume_end*np.exp(-t/float(SAMPLING_FREQ)/(Re[i]/Ee[i])) for t in range(0, exp_len+0)]
    volume_out = [volume_in[-1]*np.exp(-t/float(SAMPLING_FREQ)*(Ee[i]/Re[i])) for t in range(0, exp_len+0)]
    print('decay should be....')
    print(Ee[i]/Re[i])
    volume = volume_in + volume_out

    flow_out = [-((pressures_in[-1] - PEEP)/Re[i] - 1*flow_in[-1])*np.exp(-t/float(SAMPLING_FREQ)*(Ee[i]/Re[i]))
             for t in range(exp_len)]
    flow = flow_in + flow_out

    pressures_out = [Ee[i]*volume_out[j] + Re[i]*flow_out[j] for j in range(len(volume_out))]
    pressures = pressures_in + pressures_out

    # zero flow pressure
    pressure_offs = ((pressures_in[-1] - pressures_out[0])*(-flow_out[0]/(flow_in[-1] - flow_out[0]))
                  + pressures_out[0])

    # Repeat breathing cycles
    repeats = 0
    pressures =  pressures + repeats*pressures
    flow = flow + repeats*flow
    volume = volume + repeats*volume

    # Define range to ID parameters over
    s = insp_len + 2
    e = insp_len + 5

    # inspiration
    dependent = np.array([pressures[:insp_len - 1]])
    independent = np.array([volume[:insp_len - 1], flow[:insp_len - 1]])
    res = lstsq(independent.T, dependent.T)
    print('For Inspiration:')
    print(res[0])
    print('E/R: {}'.format(res[0][0][0]/res[0][1][0]))

    remade_insp = [res[0][0][0]*volume[j] + res[0][1][0]*flow[j] for j in range(len(volume)-1)]

    # expiration
    #pressure_offs = 0
    pres = [p - pressure_offs for p in pressures[s:e]]
    #vol = [v - 0 for v in volume[s:e]]
    vol = [v - volume[insp_len] for v in volume[s:e]]
    flw = [q for q in flow[s:e]]

    dependent = np.array([pres])
    independent = np.array([vol, flw])
    res = lstsq(independent.T, dependent.T)
    print('For Expiration:')
    print(res[0])
    print('E/R: {}'.format(res[0][0][0]/res[0][1][0]))
    print('E = R/tau: {}'.format(res[0][1][0]/(Re[i]/Ee[i])))
    print('\n')

    remade_exp = [res[0][0][0]*volume[j] + res[0][1][0]*flow[j] for j in range(len(volume)-1)]
    remade_exp2 = [Ee[i]*volume[j] + Re[i]*flow[j] for j in range(len(volume)-1)]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Plots
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

    #pressure
    ax1.plot(times, pressures, '-', linewidth=3)
    ax1.plot(times[:len(remade_exp)], remade_exp, 'r--', linewidth=2)
    ax1.plot(times[:len(remade_exp)], remade_exp2, 'r.-', linewidth=2)
    ax1.plot(times[:len(remade_insp)], remade_insp, 'k.', linewidth=2)
    ax1.plot(times[s:e], pressures[s:e], 'y-', linewidth=1)
    ax1.legend([
        'Data',
        'fwd sim exp',
        'fwd sim exp with real values',
        'fwd sim insp',
        'Range used for fitting expiration'
        ])

    #flow
    ax2.plot(times, flow, '-', linewidth=3)
    ax2.plot(times[s:e], flow[s:e], 'y', linewidth=1)

    #volume
    ax3.plot(times, volume, '-', linewidth=3)
    ax3.plot(times[s:e], volume[s:e], 'y', linewidth=1)

    ax1.set_ylabel('Pressure')
    ax2.set_ylabel('Flow')
    ax3.set_ylabel('Volume')
    ax3.set_xlabel('Time')
    ax1.grid()
    ax2.grid()
    ax3.grid()

    # QV loop
#    g, (ax4) = plt.subplots(1)
#    ax4.plot(flow, volume, 'r.-')
#    ax4.set_ylabel('volume')
#    ax4.set_xlabel('flow')
#    ax4.grid()

    RC_plot = [flw[j]/vol[j] for j in range(len(flw))]
    vol2 = [v for v in volume[s:e]]
    RC_plot2 = [flw[j]/vol2[j] for j in range(len(flw))]
    RC_plot3 = [flow[j]/volume[j] for j in range(4, insp_len)]
    wt = [w*t for t in times[:insp_len]]
    ideal_flow = [np.sin(x) for x in wt]
    ideal_volume = [-np.cos(x) + 1 for x in wt]
    ideal_QV = [ideal_flow[j]/ideal_volume[j] for j in range(4, insp_len)]
    QV_scaling = [RC_plot3[j]/ideal_QV[j] for j in range(len(ideal_QV))]

    g, (ax4) = plt.subplots(1)
    ax4.grid()
    ax4.plot(RC_plot2)

    print('Checking exponential expiration:')

    lny = [np.log(v) for v in volume[s:e]]
    t = times[s:e]
    ones = [1]*len(t)
    dependent = np.array([lny])
    independent = np.array([ones, t])
    res = lstsq(independent.T, dependent.T)
    print(res)
    res = res[0][1][0]
    print(res)


    print('line decay rate: {}'.format(-flow_out[0]/volume_out[0]))
    print('expected decay rate: {}'.format(Ee[i]/Re[i]))

    plt.show()

#    h, (ax1) = plt.subplots(1)
#    print(i)
#    proof = [p/E[i] for p in pressures]
#    ax1.plot(proof)
#ax1.set_title('PC curves for all data sets used')
#plt.show()


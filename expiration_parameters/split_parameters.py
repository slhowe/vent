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

#Import built-ins
import matplotlib.pyplot as plt
from math import sin, cos, pi, exp, log
from numpy import nan
import numpy as np
from scipy import io
from scipy.stats.stats import pearsonr
from numpy.linalg import lstsq

def split_parameters(pressure, flow, volume, sampling_frequency, prev_peep=nan):
    Ei = 0
    Ri = 0
    Ee = 0
    Re = 0
    Em = 0
    Rm = 0

    # Start of inspiration:
    # This is at first crossing from negative flow to
    # positive flow, or at the first index. Stop looking
    # after max flow value. That point is definitely in
    # inspiration. Work backwards from max flow, because
    # start data can be noisy around zero crossing.
    start_insp = 0
    Q_max = max(flow[:len(flow)/3])
    Q_max_index = flow.index(Q_max)
    i = Q_max_index
    while(i > 0.01):
        if(flow[i] >= 0.01 and flow[i-1] < 0.01):
            start_insp = i
            i = 0
        i -= 1

    # Get peep
    # From the average of last third of data
    peep_data = pressure[-len(pressure)/3:]
    peep = sum(peep_data)/len(peep_data)

    # End of inspiration:
    # Working backwards, find the last
    # point of positive flow in the data
#    end_insp = len(flow) - 1
#    i = len(flow)*1/2
#    while i > 0:
#        if(flow[i] < 0.01 and flow[i-1] > 0.01):
#            end_insp = i
#            i = 0
#        i -= 1
    end_insp = start_insp + 15
    i = end_insp
    while(i < len(flow) - 4):
        if((flow[i] < 0.01 or flow[i+1] < 0) and flow[i+4] < 0.01):
            end_insp = i
            i = len(flow)
        i += 1

    # start of expiration
    start_exp = end_insp + 1
#    i = len(flow)*1/2
#    while(i > end_insp):
#        if(flow[i] < 0 and flow[i-1] >= 0):
#            start_exp = i
#            i = 0
#        i -= 1

    # Get start and end point away from edges of insp
    # for parameter ID
    start = start_insp + (end_insp - start_insp)*1/8
    end = end_insp - 5

    print('start_insp: {}'.format(start_insp))
    print('end_insp: {}'.format(end_insp))
    print('start_exp: {}'.format(start_exp))
    print('start: {}'.format(start))
    print('end: {}'.format(end))
    print('peep: {}'.format(peep))
    print('')

    # Remove peep from pressure
    # Offset for all pressure data is now 0
    # Offset of estimated pressure will be 0
    pressure = [p - peep for p in pressure]

    # Mess with pressure in expiration to make constant 0
    #k = start_exp
    #while k < len(pressure):
    #    pressure[k] = 0
    #    k += 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Check there are more than the minimum data points
    # needed for least squares in inspiration and range
    # for estimating data
    if(
      end_insp - start_insp <= 3    # Data too short
      or end - start <= 3           # Data too short
      or np.isnan(flow[0])          # Data starts with NaN
      or end_insp > len(flow) - 20  # End too close
      ):
        print('Bad data, ignoring')
        plt.plot(flow)
        plt.show()

    else:
        #------------------------------------------------------------------------
        #------------------------------------------------------------------------
        #------------------------------------------------------------------------
        # Params for INSP

        # Crop data to insp range
        flw = flow[start:end]
        pres = pressure[start:end]
        vol = volume[start:end]

        # Params from insp pressure
        dependent = np.array([pres])
        independent = np.array([flw, vol])

        try:
            res = lstsq(independent.T, dependent.T)
            Ei = res[0][1][0]
            Ri = res[0][0][0]
        except(ValueError):
            print('ValueError: Data has nan?')
            Ei = nan
            Ri = nan

        print('E from insp pressure: {}'.format(Ei))
        print('R from insp pressure: {}'.format(Ri))
        print('E/R from insp pressure: {}'.format(Ei/Ri))
        print('')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Params for EXP

        # Get P0 from end insp. That means the zero crossing pressure
        # If pressure dropped from max by 25%, use max pressure
        P_max= max(pressure[start_insp:start_exp])
        P_max_index = pressure.index(P_max)
        P_start = P_max

        zero_crossing_offset = -(flow[start_exp])/(flow[start_exp - 1] - flow[start_exp])
        zero_crossing_pressure = ((pressure[start_exp-1] - pressure[start_exp])* zero_crossing_offset
                               + pressure[start_exp])
        print('zero crossing pressure: {}'.format( zero_crossing_pressure ))
        print('zero crossing offset: {}'.format( zero_crossing_offset ))
        print('zero crossing offset den: {}'.format(flow[start_exp- 1] - flow[start_exp] ))
        P_start = zero_crossing_pressure

        # Shift reference points and crop to expiration only
        drop_pressure = [p - P_start for p in pressure[start_exp:]]
        drop_volume = [v - volume[start_exp] for v in volume[start_exp:]]
        drop_flow = [f for f in flow[start_exp:]]

        # DEFINE START AND END
        start = drop_flow.index(min(drop_flow)) + 5
        end = len(drop_volume) - 5

        dependent = np.array([drop_pressure[start:end]])
        independent = np.array([drop_volume[start:end], drop_flow[start:end]])
        Ee = nan
        Re = nan
        if(end - start > 5):
            try:
                expres = lstsq(independent.T, dependent.T)
                Ee = expres[0][0][0]
                Re = expres[0][1][0]
                fit_error = expres[1][0]
            except(ValueError):
                print('ValueError: Data has nan?')

        print('E from exp pressure: {}'.format(Ee))
        print('R from exp pressure: {}'.format(Re))
        print('E/R from exp pressure: {}'.format(Ee/Re))
        #print('FITTING ERROR: {}'.format(fit_error))
        print('')

         # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Salwa method for better pressure estimation if end asynchrony
        b_offs = 2
        a_offs = 3
        search_offs = 20

        point_b = end_insp + b_offs
        point_a = point_b + a_offs
        point_b_pressure = max(pressure[point_b:point_b + search_offs])

        # pick steeper gradient of start and end of breath
        grad_end = (pressure[point_b] - pressure[point_a])
        grad_start = (pressure[start_insp+2] - pressure[start_insp+1])
        print('grad end {}'.format(grad_end))
        print('grad start {}'.format(grad_start))
        #if(grad_start > grad_end/1.2):
        #    grad = grad_start
        #else:
        #    grad = grad_end
        grad = grad_end

        reconstruction_line = [min(P_max, grad*(b_offs + i) + point_b_pressure) for i in range(0, start_exp-P_max_index)]

        print('Pmax = {}'.format(P_max))
        print('zcp = {}'.format(zero_crossing_pressure))
        print('0.75*Pmax = {}'.format(0.75*P_max))


        # area difference to choose te corner pressure
        old_area = integral(pressure[P_max_index:start_exp], sampling_frequency)
        new_area = integral(reconstruction_line, sampling_frequency)
        area_difference = new_area[-1] - old_area[-1]
        print('ghghghghgh')
        print(area_difference)

        # Really low gradients at the end means the end was mauled
        # or significant drop from max pressure
        if((grad_end < grad_start/3)
        or(zero_crossing_pressure < 0.75*P_max)):
            corner_pressure = P_max
        elif(area_difference > 1.0):
            # Reconstructed corner pressure
            corner_pressure = min(P_max, grad*(b_offs+zero_crossing_offset) + point_b_pressure)
        else:
            corner_pressure = zero_crossing_pressure

        # find pressure at start_exp using gradient.
        # If pressure is less than what is already at start_exp,
        # use that instead
        # (zco relative to end insp, pressure is b_offs away from zc)
        if(corner_pressure < zero_crossing_pressure):
            corner_pressure = zero_crossing_pressure

        # Shift reference points and crop to expiration only
        drop_pressure_new = [p - corner_pressure for p in pressure[start_exp:]]

        dependent = np.array([drop_pressure_new[start:end]])
        independent = np.array([drop_volume[start:end], drop_flow[start:end]])
        Em = nan
        Rm = nan
        if(end - start > 5):
            try:
                expres = lstsq(independent.T, dependent.T)
                Em = expres[0][0][0]
                Rm = expres[0][1][0]
                fit_error = expres[1][0]
            except(ValueError):
                print('ValueError: Data has nan?')


        print('E from exp pressure (other): {}'.format(Em))
        print('R from exp pressure (other): {}'.format(Rm))
        print('E/R from exp pressure (other): {}'.format(Em/Rm))
        #print('FITTING ERROR: {}'.format(fit_error))
        print('')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # exponential fit to expiration
        exp_start = start
        exp_end = start + (end - start)*2/3

        i = exp_start
        while i < exp_end:
            if drop_flow[i] >= 0:
                exp_end = i - 1
                i = exp_end
            i += 1

        ln_flow = [np.log(-f) for f in drop_flow[exp_start:exp_end]]
        ones = [1]*(exp_end - exp_start)
        times = [t/float(sampling_frequency) for t in range(len(ones))]
        full_times = [t/float(sampling_frequency) for t in range(end-start)]

        dependent = np.array([ln_flow])
        independent = np.array([ones, times])
        try:
            res = lstsq(independent.T, dependent.T)
            decay = res[0][1][0]
            offset = -np.exp(res[0][0][0])
        except(ValueError):
            print('ValueError: Data has nan?')
            decay = nan
            offset = nan

        exp_flow = [offset*np.exp(decay*t) for t in times]
        full_exp_flow = [offset*np.exp(decay*t) for t in full_times]
        print('E/R from decay rate of flow: {}'.format(decay))
        print('')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # What is Edrs?

        start_edrs = drop_flow.index(min(drop_flow))
        Edrs = [0]*(len(drop_pressure))
        i = 0
        while i < len(drop_pressure):
            Edrs[i] = ((drop_pressure[i] - Rm*drop_flow[i])
                               / min(drop_volume[i], -1e-2))
            i += 1

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # All plotting below here
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Fitting on expiration
        if(0):
            plt.rc('legend',**{'fontsize':12})
            f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

            # Forward simulate pressure
            press_guess_insp = [Ei*drop_volume[i] + Ri*drop_flow[i]
                          for i in range(0, len(drop_volume))]
            press_guess_exp = [Ee*drop_volume[i] + Re*drop_flow[i]
                          for i in range(start, end)]
            press_guess_other = [Em*drop_volume[i] + Rm*drop_flow[i]
                          for i in range(0, len(drop_volume))]
            EV_guess = [Ee*V for V in drop_volume]
            RQ_guess = [Re*Q for Q in drop_flow]

            ax1.plot(drop_pressure, 'b', linewidth=3)
            ax1.plot(EV_guess, 'c+')
            ax1.plot(RQ_guess, 'gx')
            ax1.plot(range(start, end), press_guess_exp, 'r--', linewidth=3)
            ax1.legend([
                        'Data',
                        'Lung pressure (E = {:.2f})'.format(Ee),
                        'Resistive pressure (R = {:.2f})'.format(Re),
                        'Forward simulation (P = EV + RQ)'
                        ], fontsize=16, loc=1)
            ax1.set_ylabel('Pressure (cmH20)', fontsize=16)

            ax2.plot(drop_flow, 'b', linewidth=3)
            #ax2.plot(range(exp_start, exp_end), exp_flow, color='orange', linewidth=2)
            #ax2.plot(range(start, end), full_exp_flow, '--', color='orange', linewidth=2)
            ax2.legend([
                         'Data',
                         ], fontsize=16)
            ax2.set_ylabel('Flow (L/s)', fontsize=16)

            ax3.plot(drop_volume,'b-', linewidth=3)
            ax3.legend([
                         'Data'
                         ], fontsize=16)
            ax3.set_ylabel('Volume (L)', fontsize=16)
            ax3.set_xlabel('Data point', fontsize=16)

            ax1.grid()
            ax2.grid()
            ax3.grid()
            plt.show()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Exp flow and pressure
        if(0):
            f, (ax1, ax2) = plt.subplots(2, sharex=True)
            ax1.plot(flow, 'b', linewidth=5)
            ax1.plot(range(start_exp+start, start_exp+end), full_exp_flow, 'r--', linewidth=5)
            ax1.legend([
                'Data',
                'Exponential fit',
                ], fontsize=16)
            ax1.grid()
            ax1.set_ylabel('Flow (L/s)', fontsize=16)

            ax2.plot(pressure, 'b', linewidth=5)
            ax2.grid()
            ax2.set_ylabel('Pressure (cmH2O)', fontsize=16)
            ax2.set_xlabel('data point', fontsize=16)

            plt.show()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # What is Edrs?

        start_edrs = drop_flow.index(min(drop_flow))
        Edrs = [0]*(len(drop_pressure))
        i = 0
        while i < len(drop_pressure):
            Edrs[i] = ((drop_pressure[i] - Rm*drop_flow[i])
                               / min(drop_volume[i], -1e-2))
            i += 1

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # All plotting below here
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Fitting on expiration
        if(0):
            'plot exponential fits'
            plt.rc('legend',**{'fontsize':12})
            f, (ax1) = plt.subplots(1, sharex=True)

            # Forward simulate pressure
            press_guess_insp = [Ei*drop_volume[i] + Ri*drop_flow[i]
                          for i in range(0, len(drop_volume))]
            press_guess_exp = [Ee*drop_volume[i] + Re*drop_flow[i]
                          for i in range(start, end)]
            press_guess_other = [Em*drop_volume[i] + Rm*drop_flow[i]
                          for i in range(0, len(drop_volume))]
            EV_guess = [Ee*V for V in drop_volume]
            RQ_guess = [Re*Q for Q in drop_flow]

            ax1.plot(drop_pressure, 'b', linewidth=3)
            ax1.plot(EV_guess, 'c+')
            ax1.plot(RQ_guess, 'gx')
            ax1.plot(range(start, end), press_guess_exp, 'r--', linewidth=3)
            ax1.legend([
                        'Data',
                        'Lung pressure (E = {:.2f})'.format(Ee),
                        'Resistive pressure (R = {:.2f})'.format(Re),
                     ])

            plt.show()



        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Edrs for this breath
        if(0):
            f, (ax0, ax1, ax2, ax3) = plt.subplots(4, sharex=True)
            ax0.set_title('Edrs in exhalation (MV)')

            ax0.plot(drop_pressure[start_edrs:], linewidth=3)
            ax0.set_ylabel('Pressure (cmH20)')
            ax0.grid()

            ax1.plot(drop_flow[start_edrs:], linewidth=3)
            ax1.set_ylabel('Flow (L/s)')
            ax1.grid()

            ax2.plot(drop_volume[start_edrs:], linewidth=3)
            ax2.set_ylabel('Volume (L)')
            ax2.grid()

            ax3.plot(Edrs[start_edrs:], linewidth=3)
            ax3.set_ylabel('Edrs')
            ax3.set_ylim([-20, 40])
            ax3.grid()

            plt.show()

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Pressure, Flow, volume, fwd sim plot
        print('return: {}'.format(Ee))
        if(1):
            'Plot full flow and pressure and volume with estimates'
            plt.rc('legend',**{'fontsize':10})
            f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

            # Remake pressure
            press_guess_insp = [Ei*volume[i] + Ri*flow[i] for i in range(0, end)]
            press_guess_exp = [Ee*volume[i] + Re*flow[i] for i in range(0, end)]
            press_guess_other= [Em*volume[i] + Rm*flow[i] for i in range(0, end)]

            salwa_line = [min(P_max, grad*i + point_b_pressure) for i in range(end_insp+ b_offs + 1)]
            salwa_line.reverse()

            ax1.plot(pressure, 'b', linewidth=3)
            ax1.plot(range(0, end), press_guess_insp, 'm:', linewidth=3)
            ax1.plot(range(0, end), press_guess_exp, 'g--', linewidth=3)
            ax1.plot(range(0, end), press_guess_other, '--', color='orange', linewidth=3)
            ax1.plot(end_insp, corner_pressure, 'mo')
            ax1.plot(end_insp, P_start, 'ko')
            ax1.plot(end_insp - zero_crossing_offset, zero_crossing_pressure, 'co')
            ax1.plot(salwa_line, 'r--', linewidth=2)
            #ax1.plot([-p for p in drop_pressure], 'm', linewidth=2)
            ax1.legend([
                        'Data',
                        'Fwd sim from insp (E={:.1f}, R={:.1f})'.format(Ei, Ri),
                        'Fwd sim from exp (E={:.1f}, R={:.1f})'.format(Ee, Re),
                        'Fwd sim from other (E={:.1f}, R={:.1f})'.format(Em, Rm),
                        'Corner point from Salwa\'s reconstruction method',
                        'Corner point from zero crossing and P_max'
                        ], loc=1)
            ax1.set_ylabel('Pressure (cmH20)', fontsize=16)

            ax2.plot(flow, 'b', linewidth=3)
            ax2.plot((end_insp - zero_crossing_offset), 0, 'co')
            ax2.plot([-p for p in drop_flow], 'm', linewidth=2)
            ax2.plot(end_insp, flow[end_insp], 'ro')
            ax2.set_ylabel('Flow (L/s)', fontsize=16)


            ax3.plot(volume,'b-', linewidth=3)
            ax3.plot([-p for p in drop_volume], 'm', linewidth=2)
            ax3.set_ylabel('Volume (L)', fontsize=16)
            ax3.set_xlabel('Data point', fontsize=16)

            ax1.grid()
            ax2.grid()
            ax3.grid()
            plt.show()

#    if(Ei > 80):
#        Ei = nan
#    if(Em > 80):
#        Em = nan
#    if(Ee > 80):
#        Ee = nan
#    if(Ei < 0):
#        Ei = nan
#    if(Em < 0):
#        Em = nan
#    if(Ee < 0):
#        Ee = nan

    print('return: {}'.format(Ee))
    if(abs(prev_peep - peep) < 0.5) or np.isnan(prev_peep):
        return(Ei, Ri, Em, Rm, Ee, Re, peep)
    else:
        return(nan, nan, nan, nan, nan, nan, peep)
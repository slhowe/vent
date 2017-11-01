#!/bin/bash
import sys
sys.path.insert(0, '/home/sarah/Documents/Spirometry/python/extensions')

import matplotlib.pyplot as plt
import numpy as np

from filters import hamming

#~~~~~~~~~~~~~~~~~~
# Predator function
#~~~~~~~~~~~~~~~~~~
#
# Take pressure, flow, volume of 5 breaths
# Separate inspiration and expiration
# Normalise each half to 1s and super impose
# Pressure in inspiration takes max, others take mean

def predator(pressures, flows, volumes, plotting=False):

    # Data in form [[set1], [set2], ... , [setn]]
    # Start with first set
    number_of_sets = len(pressures)
    set_count = 0

    new_insp_pressures = [[]]*number_of_sets
    new_exp_pressures = [[]]*number_of_sets
    new_insp_flows = [[]]*number_of_sets
    new_exp_flows = [[]]*number_of_sets
    new_insp_volumes = [[]]*number_of_sets
    new_exp_volumes = [[]]*number_of_sets

    for data in range(number_of_sets):
        # find end of inspiration
        end_insp = 15
        i = end_insp
        while(i < len(flows[data]) - 4):
            if((flows[data][i+1] < 0) and flows[data][i+4] < 0.01):
                end_insp = i
                i = len(flows[data])
            i += 1

        # Separate data into two halves
        insp_pressure = pressures[data][:end_insp]
        exp_pressure = pressures[data][end_insp:]
        insp_flow = flows[data][:end_insp]
        exp_flow = flows[data][end_insp:]
        insp_volume = volumes[data][:end_insp]
        exp_volume = volumes[data][end_insp:]

        # normalise data to 1 second
        insp_time = range(len(insp_pressure))
        insp_time = [t/float(insp_time[-1]) for t in insp_time]
        exp_time = range(len(exp_pressure))
        exp_time = [t/float(exp_time[-1]) for t in exp_time]

        def interpolate(points, times, target_time):
            # workout what a value is with linear interpolation between 2 points
            m = (points[1] - points[0])/(times[1] - times[0])
            c = points[0]
            x = target_time - times[0]
            y = m*x + c
            return y

        def resampled(datapoints, datatime, interval):
            # resample data at set interval
            dataset = []
            target_time = 0
            index = 1
            t = datatime[index]
            while index <= len(datapoints) and target_time < 1.0:
                if t >= target_time:
                    # points to interpolate are current and previous
                    points = [datapoints[index - 1], datapoints[index]]
                    times = [datatime[index - 1], datatime[index]]
                    new_sample = interpolate(points, times, target_time)
                    dataset.append(new_sample)
                    target_time += interval
                    # Go back one index in case interpolation time steps are small and
                    # Two interpolations fit within one pair of real data
                    index -= 1
                index += 1
                t = datatime[index]

            dataset.append(new_sample)
            return dataset

        # resample at preset intervals
        interval = 0.01
        new_insp_pressure = resampled(insp_pressure, insp_time, interval)
        new_exp_pressure = resampled(exp_pressure, exp_time, interval)
        new_insp_flow = resampled(insp_flow, insp_time, interval)
        new_exp_flow = resampled(exp_flow, exp_time, interval)
        new_insp_volume = resampled(insp_volume, insp_time, interval)
        new_exp_volume = resampled(exp_volume, exp_time, interval)

        new_insp_time = [t*interval for t in range(len(new_insp_pressure))]
        new_exp_time = [t*interval+new_insp_time[-1] for t in range(len(new_exp_pressure))]

        #plt.plot(new_insp_pressure + new_exp_pressure, 'o-')
        #plt.plot(new_insp_flow + new_exp_flow, 'o-')
        #plt.plot(new_insp_volume + new_exp_volume, 'o-')

        new_insp_pressures[set_count] = new_insp_pressure
        new_exp_pressures[set_count] = new_exp_pressure
        new_insp_flows[set_count] = new_insp_flow
        new_exp_flows[set_count] = new_exp_flow
        new_insp_volumes[set_count] = new_insp_volume
        new_exp_volumes[set_count] = new_exp_volume
        set_count += 1

    # Super impose data
    max_insp_pressure = np.max(new_insp_pressures, axis=0).tolist()
    mean_exp_pressure = np.mean(new_exp_pressures, axis=0).tolist()
    mean_insp_flow =  np.mean(new_insp_flows, axis=0).tolist()
    mean_exp_flow =  np.mean(new_exp_flows, axis=0).tolist()
    mean_insp_volume =  np.mean(new_insp_volumes, axis=0).tolist()
    mean_exp_volume =  np.mean(new_exp_volumes, axis=0).tolist()

    # only return inspiratory data between correct values
    # correct values are assumed before pressure gradient changes
    def sign(x):
        res = [0]*len(x)
        for k in range(len(x)):
            if x[k] > 0:
                res[k] = 1
            elif x[k] < 0:
                res[k] = -1
            elif x[k] == 0:
                res[k] = 0
            else:
                res[k] = x
        return res

    # first filter the data heaps
    filt_pressure = hamming(max_insp_pressure, 12, 125, 25, plot=False)
    filt_pressure = np.real(filt_pressure).tolist()
    #print(len(max_insp_pressure))
    #print(len(filt_pressure))
    #print(len(new_insp_time))

    # find the inflection points
    diff_P = np.diff(filt_pressure)
    #print(diff_P)
    sign_diff_P = sign(diff_P)
    #print(sign_diff_P)
    diff_sign_diff_P = np.diff(sign_diff_P)
    #print(diff_sign_diff_P)
    abs_diff_sign_diff_P = np.abs(diff_sign_diff_P)
    #print(abs_diff_sign_diff_P)
    gradient_change_position = np.where(abs_diff_sign_diff_P == 2)[0]
    #print(gradient_change_position)
    #print(len(gradient_change_position))


    if(plotting):
        plt.show()

        #final_pressure = max_insp_pressure + exp_pressure
        #final_flow = mean_insp_flow + exp_flow
        #final_volume  = mean_insp_volume + exp_volume
        final_pressure = max_insp_pressure + mean_exp_pressure
        final_flow = mean_insp_flow + mean_exp_flow
        final_volume  = mean_insp_volume + mean_exp_volume

        for k in range(len(new_insp_pressures)):
            plt.plot(new_insp_time + new_exp_time, new_insp_pressures[k]+new_exp_pressures[k])

        plt.plot(new_insp_time, filt_pressure, 'orange')
        plt.plot(new_insp_time[gradient_change_position[0]], final_pressure[gradient_change_position[0]], 'rs')
        plt.plot(new_insp_time+new_exp_time, final_pressure, 'k*')
        plt.show()

        for k in range(len(new_insp_flows)):
            plt.plot(new_insp_flows[k])

        plt.plot(final_flow, 'k*')
        plt.show()

    #gradient_change_position = [0]
    final_pressure_e = max_insp_pressure + mean_exp_pressure
    final_flow_e = mean_insp_flow + mean_exp_flow
    final_volume_e  = mean_insp_volume + mean_exp_volume

    if(len(gradient_change_position) >= 2):
        max_insp_pressure = max_insp_pressure[:gradient_change_position[0]]
        new_insp_time = new_insp_time[:gradient_change_position[0]]
        mean_insp_flow = mean_insp_flow[:gradient_change_position[0]]
        mean_insp_volume = mean_insp_volume[:gradient_change_position[0]]

    #final_pressure = max_insp_pressure + exp_pressure
    #final_flow = mean_insp_flow + exp_flow
    #final_volume  = mean_insp_volume + exp_volume
    final_pressure_i = max_insp_pressure + mean_exp_pressure
    final_flow_i = mean_insp_flow + mean_exp_flow
    final_volume_i  = mean_insp_volume + mean_exp_volume

    return [final_pressure_i, final_flow_i, final_volume_i, final_pressure_e, final_flow_e, final_volume_e]

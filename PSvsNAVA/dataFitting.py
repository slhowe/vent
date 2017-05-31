#!/bin/bash

import csv
import matplotlib.pyplot as plt
from numpy import array
from numpy.linalg import lstsq
from splitBreaths import split_breaths

path = '/home/sarah/Documents/PSvsNAVA/data/'
plot_path = '/home/sarah/Documents/PSvsNAVA/lungPlots/'
filename = 'BRU1_PS'
flow_file = path + filename + '_flow.csv'
pres_file = path + filename + '_pres.csv'
eadi_file = path + filename + '_eadi.csv'

# Load some data...
flow = []
pressure = []
eadi = []

print('Loading data from {}'.format(filename))
with open(flow_file, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        flow.append(float(row[0]))
with open(pres_file, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        pressure.append(row)
with open(eadi_file, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        eadi.append(row)

# find the start indices of breaths
indices = split_breaths(flow)

# flow crosses 0 is around
# point pressure drop starts
inv_flow = [-1.0*f for f in flow]
corner_indices = split_breaths(inv_flow)

# Use shorter indices list
number_of_breaths = 0
if len(indices) < len(corner_indices):
    number_of_breaths = len(indices)
else:
    number_of_breaths = len(corner_indices)

fit_pressure = pressure

# one breath at a time
for breath in range(number_of_breaths):
    # Fetch indices
    breath_start = indices(breath)
    breath_corner = corner_indices(breath)
    breath_end = indices(breath+1) -1

    # find volume
    breath_volume =

    # find E and R
    # use R to find new E


# plots
plt.figure(1)
time = range(len(flow))
corner_pressure = [pressure[i] for i in corner_indices]
start_pressure = [pressure[i] for i in indices]

# pressure
plt.subplot(211)
plt.plot(time, pressure, 'b',
        corner_indices, corner_pressure, '.r',
        indices, start_pressure, '.m'
        )

# flow
plt.subplot(212)
plt.plot(time, flow, 'k')
plt.show()

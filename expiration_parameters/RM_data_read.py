#!/bin/bash

import csv

'''
Contains a callable storage class to extract data from RM CURE files.
Data is split into breaths. Breaths are iterable with :
    for breath in RM_data_read.Breaths:
        ...
Breaths contain pressure and flow info only
'''

class IterRegistry(type):
    # Make classes iterable if this is their meta class
    # Child classes must contain self._registry of instances
    def __iter__(cls):
        return iter(cls._registry)

class Breaths:
    # Data storage for individual breaths
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self):
        self._registry.append(self)
        self.pressure = []
        self.flow = []

    def clean_up(self):
        del self._registry[:]

class Storage:
    # Extracts data
    def __init__(self):
        pass

    def extract_data(self, filename):
        # Store data from file
        recording = False
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for row in reader:

                # Start new recording at BS
                if(not recording):
                    if(row[0] == 'BS'):
                        breath_storage = Breaths()
                        recording = True

                # End recording at BE
                elif(recording and row[0] == 'BE'):
                    recording = False

                # Otherwise record
                else:
                    breath_storage.flow.append(float(row[0])/60.0)
                    breath_storage.pressure.append(float(row[1]))

    def clean_up(self):
        cleaner=Breaths()
        cleaner.clean_up()

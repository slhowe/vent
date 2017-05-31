#!/bin/bash

# Add my extensions to path
import sys
sys.path.insert(0, '/home/sarah/Documents/Spirometry/python/extensions')

# Import my extensions
from calculus import integral, derivative
from filters import hamming

#Import built-ins
import matplotlib.pyplot as plt
from math import sin, cos, pi, exp, log
from numpy import nan
import numpy as np
from scipy import io

if __name__ == '__main__':
    pre_na = [20.7, 20.6, 20.2, 21.0, 21.2, 21.9, 21.5, 21.3, 20.5, 20.5, 20.8, 22.0, 19.8, 22.3]
    pre_a = [10.7, 23.4, 12.8, 17.6, 16.1, 29.4, 13.8, 12.3, 25.6, 16.3, 22.5, 16.2, 24.1, 28.7]
    post_na = [20.7, 20.6, 20.2, 21.0, 21.2, 21.9, 21.5, 21.3, 20.5, 20.5, 20.8, 22.0, 19.8, 22.3]
    post_a = [20.7, 20.6, 20.2, 21.0, 21.2, 21.9, 21.5, 21.3, 20.5, 20.5, 20.8, 22.0, 19.8, 22.3]

    # cdf plots
    pre_na = np.sort(pre_na)
    pre_a = np.sort(pre_a)
    post_na = np.sort(post_na)
    post_a = np.sort(post_a)
    proportional_data = 1. * np.arange(len(pre_na))/(len(pre_na) - 1)

    f, ax = plt.subplots(1, 2)

    # Pre first
    ax[0].grid()
    ax[0].plot(pre_a, proportional_data, 'r', linewidth=2)
    ax[0].plot(pre_na, proportional_data, 'b.-')
    ax[0].set_xlabel("Inspiratory Elastance", fontsize=20)
    ax[0].set_ylabel("Probability density", fontsize=20)
    ax[0].set_title("(a)", fontsize=20)

    # Then post
    ax[1].grid()
    ax[1].plot(post_a, proportional_data, 'r', linewidth=2)
    ax[1].plot(post_na, proportional_data, 'b.-')
    ax[1].set_xlabel("Expiratory Elastance", fontsize=20)
    ax[1].set_title("(b)", fontsize=20)

    for (m), subplot in np.ndenumerate(ax):
        subplot.set_xlim([10,30])
        subplot.tick_params(labelsize=15)
    plt.setp([a.get_xticklabels() for a in ax[:3]], visible=False)
    ax[0].legend(['Pre sedation',
                'Post sedation',
                ], loc=0)
    #f.add_subplot(111, frameon=False)
    #plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    plt.show()




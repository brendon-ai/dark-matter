#!/usr/bin/env python3
"""Graph the overall performance of a series of general machine learning techniques for the DEAP experiment"""
# Created by Brendon Matusch, November 2018

import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Create lists containing the performance statistics (in the form (mean, 8th percentile, 92nd percentile))
ALPHA = [(0.996, None, None), (1.0, 1.0, 1.0), (0.9986762886158047, 0.996774193548387, 1.0),
         (0.9985087719298246, 0.9921052631578948, 1.0), (0.9959030977982591, 0.9914285714285715, 1.0), (0.9120370370370369, 0.8888888888888888, 0.9333333333333333)]
WIMP = [(0.91, None, None), (1.0, 1.0, 1.0), (0.7672341098533079, 0.74375, 0.79915611814346),
        (0.9301859015688803, 0.6060606060606061, 1.0), (0.75745328295003, 0.7313432835820896, 0.7927631578947368), (0.7388888888888889, 0.7000000000000001, 0.775)]
# Zip all of these lists into separate high and low arrays
alpha_mean, alpha_low, alpha_high = np.array(list(zip(*ALPHA)))
wimp_mean, wimp_low, wimp_high = np.array(list(zip(*WIMP)))
# Convert the high and low lists to errors, substituting 0 for None
for array, mean in [(alpha_high, alpha_mean), (alpha_low, alpha_mean), (wimp_high, wimp_mean), (wimp_low, wimp_mean)]:
    # Iterate over the indices of the array
    for index in range(len(array)):
        # If the value is None, set it to 0
        if array[index] is None:
            array[index] = 0
        # Otherwise, replace it with the absolute difference from the mean
        else:
            array[index] = np.abs(array[index] - mean[index])

# The names of the configurations corresponding to all these lists
CONFIGURATIONS = ['Conventional', 'Dense NN', 'Cylindrical Proj.', 'Topological CNN', 'Cylindrical Test (Sim)', 'Cylindrical CNN Test (Real,\nBackground May\nInclude WIMPs)']

# Get the locations for the bars
BAR_WIDTH = 0.4
alpha_locations = np.arange(len(CONFIGURATIONS))
wimp_locations = alpha_locations + BAR_WIDTH
# Create a figure with a predefined size
fig, ax = plt.subplots(figsize=(6, 4))
# Use percentage labels for the Y axis
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
# Draw a bar graph using the performance statistics
plt.bar(alpha_locations, alpha_mean * 100, width=BAR_WIDTH, yerr=(alpha_low * 100, alpha_high * 100), label='Alpha/Background Removal')
plt.bar(wimp_locations, wimp_mean * 100, width=BAR_WIDTH, yerr=(wimp_low * 100, wimp_high * 100), label='WIMP Removal')
# Now set the configuration names, with words angled so they fit
plt.xticks(wimp_locations, CONFIGURATIONS, rotation=15)
# Start at 60% so the difference is more obvious
plt.ylim(60, 100)
# Label the Y axis to specify what the numbers mean
plt.ylabel('Percentage Removal')
# Create a legend using the predefined labels
ax.legend(loc='lower left')
# Rearrange the plot to fit the labels
fig.tight_layout()
# Display the graph on screen
plt.show()

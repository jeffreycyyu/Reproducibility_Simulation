import math
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import random

#list of UBC psychology professor h-indexes; values taken from google scholar
#CHANGE_ME (unfinished) need to add all values
h_indexes = [61, 27, 41, 27, 25, 45, 95, 17, 49, 55, 15, 71, 72]

#bin limits, we want to bin into intervals of 5
bin_intervals = np.arange(0, 105, 5).tolist()

#counts for how many professors fall into each bins
bin_counts = pd.cut(h_indexes, bins=bin_intervals).value_counts()

#probabilities of a professor belonging to a given bin
bin_probabilities = [float(i)/sum(bin_counts) for i in bin_counts]

#sample to see which bin the sample will fall into with probabilities given
bin_choice = random.choices(range(1, 21), bin_probabilities)

#uniformly sample an h-index within the given bin choice
simulated_sample_h_index = random.uniform(bin_intervals[bin_choice[0]-1], bin_intervals[bin_choice[0]])

#simulated h_index given real values of all psychology professors at UBC
simulated_sample_h_index

import math
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import random


class SIMULATE_SAMPLE_FROM_WORLD:
    """
    Create a distribution to sample values from given a list of real-world values
    """
    def __init__(
        self,
        real_world_values: list,
        bin_minimum: int,
        bin_maximum: int,
        bin_size: int,
        name: str = 'simulate_sample_from_real_world'
        ):
        """
        Argument(s):
            real_world_values: list of values from the real world to model the simulated sampling distribution from
            bin_minimum: minimum value of variable to simulate a sample of
            bin_maximum: maximum value of variable to simulate a sample of
            bin_size: bin size of variable to simulate a sample of (values within a bin will be pooled together to generate sampling probabilities)
            name: name
        """
        print('class SIMULATE_SAMPLE_FROM_WORLD:.__init__')

        self.real_world_values = real_world_values
        self.bin_minimum = bin_minimum
        self.bin_maximum = bin_maximum
        self.bin_size = bin_size
        self._name = name

    
    def __call__(self):
    
        #bin limits
        bin_intervals = np.arange(self.bin_minimum, self.bin_maximum + self.bin_size, self.bin_size).tolist()

        #counts for how many professors fall into each bins
        bin_counts = pd.cut(self.real_world_values, bins=bin_intervals).value_counts()

        #probabilities belonging to a given bin
        bin_probabilities = [float(i)/sum(bin_counts) for i in bin_counts]

        #sample to see which bin the sample will fall into with probabilities given
        bin_choice = random.choices(range(1, len(bin_intervals)), bin_probabilities)

        #uniformly sample within the given bin choice
        simulated_sample = random.uniform(bin_intervals[bin_choice[0]-1], bin_intervals[bin_choice[0]])

        #simulated sample value
        return simulated_sample
    
    
    
    
#H-INDEX (TEST)

#list of UBC psychology professor h-indexes; values taken from google scholar
#CHANGE_ME (unfinished)
h_indexes_ubc_psychology = [61, 27, 41, 27, 25, 45, 95, 17, 49, 55, 15, 71, 72]
bin_minimum = 0
bin_maximum = 100
bin_size = 5

simulated_ubc_psychology_h_index = SIMULATE_SAMPLE_FROM_WORLD(h_indexes_ubc_psychology, bin_minimum, bin_maximum, bin_size)

print(simulated_ubc_psychology_h_index())
  
  
 

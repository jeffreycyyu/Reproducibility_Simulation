import random
import math, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector

from ipynb.fs.full.agent import RESEARCHER
from ipynb.fs.full.model import SCIENTIFIC_WORLD




test_model = SCIENTIFIC_WORLD(50, 20, 20)
for i in range(20):
    test_model.step()


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


class SCIENTIFIC_WORLD(Model):
    """
    Model class for the SCIENTIFIC_WORLD model.
    """
    def __init__(
        self,
        n_agents
        width: float,
        height: float,
        early_career_proportion: float,
        homophily: int
        ):
        """
        Initialize a research project for a given researcher.
        Argument(s):

        """
        self.n_agents = n_agents
        self.width = width
        self.height = height
        self.early_career_proportion = early_career_proportion
        self.homophily = homophily
        
        self.schedule = SimultaneousActivation(self)
        self.grid = ContinuousSpace(width, height, torus=False)
        
        for i in range(self.n_agents):
            a = RESEARCHER(i, self)
        
        
    def step(self):
        self.schedule.step()



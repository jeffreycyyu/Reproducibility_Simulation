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
        n_agents: int,
        width: float,
        height: float
        ):
        """
        Initialize a research project for a given researcher.
        Argument(s):
            n_agents: number of agents in the model
            width: width of continuous space
            height: height  of continuous space
        ):
        """
        super().__init__()
        
        #'n_agents' number of agents in the model
        self.n_agents = n_agents
        #width of continuous space
        self.width = width
        #height of continuous space
        self.height = height
        #simultaneous since we want neighborhood effects to only take place after the publications of other has been out for some positive amount of time
        self.schedule = SimultaneousActivation(self)
        #continuous space model as opposed to discrete grid-structure; personal preference
        #torus = False means the edges do not wrap around; this way we can observe clustering effects of researchers based on their impact
        self.grid = ContinuousSpace(self.width, self.height, torus=False)
        #self.datacollector = DataCollector( model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"} )        
        
        
        
        
        
        agent_impact_distribution = 'normal'#CHANGE_ME delete and use in init once bug fixed
        initial_publication_count_distribution = 'normal'#CHANGE_ME delete and use in init once bug fixed
        interest_in_replication_distribution = 'normal'#CHANGE_ME delete and use in init once bug fixed
        
        
        
        
        
        
        #generate an agent/researcher
        for i in range(self.n_agents):
            x = self.random.randrange(self.grid.width)#CHANGE_ME
            y = self.random.randrange(self.grid.height)#CHANGE_ME  
            position = (x, y)
            individual = RESEARCHER(i,
                                    self,
                                    position,
                                    agent_impact_distribution,
                                    initial_publication_count_distribution,
                                    interest_in_replication_distribution)
            #add agent into the model
            self.schedule.add(individual)
            #position agent is to be placed on
            #place the agent on the grid
            self.grid.place_agent(INDIVIDUAL, (x, y))
        
        #automated
        self.running = True
        #collects data at each time step
        self.datacollector.collect(self)
    
    #a single time step
    def step(self):
        #take a step
        self.schedule.step()
        #collect data
        self.datacollector.collect(self)
        
    #run the model
    def run_model(self, n):
        #'n' number of steps taken for the model
        for i in range(n):
            self.step()
        

import random
import math, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector

SCIENTIFIC_WORLD.width = 15
SCIENTIFIC_WORLD.height = 15
agent_impact_distribution = 'normal'
initial_publication_count_distribution = 'normal'
interest_in_replication_distribution = 'normal'



class RESEARCHER(Agent):
    """
    Create a RESEARCHER agent
    """
    def __init__(
        self,
        agent_impact_distribution: str,
        initial_publication_count_distribution: str,
        interest_in_replication_distribution: str,
        name: str = 'researcher'
        ):
        """
        Argument(s):
            agent_impact_distribution: distribution to draw from for a researcher's impact in the SCIENTIFIFC_WORLD
            initial_publication_count_distribution: distribution to draw from for a researcher's inititial number of publications
            interest_in_replication_distribution: distribution to draw from for a researcher's probability of conducting a replication study
            name: name
        """
        print('class RESEARCHER(Agent):.__init__')
        super().__init__(position, model)
        
        
        #agent's impact which is different from publication count since different feilds have different publication rates
        self.agent_impact_distribution = getattr(np.random, agent_impact_distribution)
        self.agent_impact = self.agent_impact_distribution(1)
        
        #researcher's permanent interest in replication studies
        self.interest_in_replication_distribution = getattr(np.random, interest_in_replication_distribution) #CHANGE_ME to be a function of researcher impact
        self.interest_in_replication = self.interest_in_replication_distribution(1)
        
        #position within the arbitrary continuous space
        self.position = (np.random(random.uniform(0, SCIENTIFIC_WORLD.width),
                                   np.random(random.uniform(0, SCIENTIFIC_WORLD.height))))
                                   
        #initial publication count; since we don't want to start with all researchers at 0 which would not be possible unless research was "judt discovered"
        self.initial_publication_count_distribution = getattr(np.random, initial_publication_count_distribution)
        self.publication_count = self.initial_publication_count_distribution(1) #CHANGE_ME to be a function of interest in replication; higher interest in replications leads to more publications in general
        
        #how far a researcher can reach within the continuous space to collaborate with another researcher (e.g., high impact researchers can collaborate with anyone but low impact researchers can only collaborate with researchers with slightly higher impact than them)
        self.radius_of_collaboration = self.agent_impact + self.publication_count ** self.interest_in_replication   #CHANGE_ME to a different formula; also more lenient                        
                  

                                   
    def initiate_project(
                    self,
                    sample_size_distribution: str,
                    power_distribution: str
                    ):
        """
        Initialize a research project for a given researcher.
        Argument(s):
            sample_size_distribution: distribution to draw from for a study's sample size
            power_distribution: distribution to draw from for a study's inherent power without regards to sample size (power will be automatically adjusted for a given sample size)
        """
        print('initiated_project')
        
        #decide project type (replication or novel)
        self.study_type = random.choices(
            ['replication', 'novel'],
            [self.interest_in_replication, 1-self.interest_in_replication])
                                   
        #generate a replication study         
        if self.study_type == 'replication':
                    #sample size of replication study
                    self.study_type.sample_size = getattr(np.random, sample_size_distribution)//2 #CHANGE_ME to a different ratio/function that includes researcher impact
                    #power of replication study
                    self.study_type.power = getattr(np.random, power_distribution)//2 #CHANGE_ME to include sample size in equasion  
                    #length of replication study
                    self.study_type.study_length = getattr(np.random, sample_size_distribution) #CHANGE_ME add an equasion that includes sample size and researcher impact; shorter for 'replication'     
                    #effect size of replication study; calculated upon study generation which is not representataive of the real world but won't induce any effects since we are doing a simulation
                    self.study_type.study = getattr(np.random, power_distribution) #CHANGE_ME add an equasion that includes sample size in equasion
                    
                    # time = 0 for this specific study                           
                    self.study_type.time_elapsed = 0
                    
                    print('study_is_a_replication')
                                   
        elif self.study_type == 'novel':
                    #sample size of novel study
                    self.study_type.sample_size = getattr(np.random, sample_size_distribution) #to function that includes researcher impact
                    #power of novel study
                    self.study_type.power = getattr(np.random, power_distribution) #CHANGE_ME to include equasion  
                    #length of replication study
                    self.study_type.study_length = random.uniform(-1, 5) #CHANGE_ME add an equasion that includes sample size and researcher impact; longer for 'replication'    
                    #effect size of replication study; calculated upon study generation which is not representataive of the real world but won't induce any effects since we are doing a simulation
                    self.study_type.effect_size = random.uniform(-1, 5) #CHANGE_ME add an equasion that includes sample size in equasion
                    
                    # time = 0 for this specific study                           
                    self.study_type.time_elapsed = 0
                    
                    print('study_is_novel')
        
        else: raise ValueError('study type was not replication or novel')
        
                                   
    def publication_attempt(self):
        """
        Attempt to publish a research project for a given project for a given researcher.    
        """
        print('publication_attempted')     
        
        self.study_type.publish_status = random.choices(['published', 'rejected'],
            [self.study_type.publishability, 1-self.study_type.publishability])
                                   
        if self.study_type.publish_status == 'published':
                                   self.publication_count += 1
                                   self.agent_impact += 1 #CHANGE_ME
                                   
                                   
        elif self.study_type.publish_status == 'rejected':
                                   self.study_type.publish_status.re_attempt_probability = random.uniform(0, 1) #CHANGE_ME to function dependednt on researcher impact, sample size, etc.
                                   self.study_type.publish_status.re_attempt_status = random.choices(['re_attempt', 'withhold'],
                                                                                                     [self.study_type.publish_status.re_attempt_probability,
                                                                                                      1-self.study_type.publish_status.re_attempt_probability])
                    
                                   if self.study_type.publish_status.re_attempt_status == 're_attempt': pass
                                   
                                   elif self.study_type.publish_status.re_attempt_status == 'withhold': initiate_project()
                                   
                                   else: raise ValueError('study was not re-attempted to publish or withheld; after a failed publication attemp')
                                   
                                   
        else: raise ValueError('study was not published or rejected')                           
                                   
                                   
                              
                                   
    def step(self):
        #update time elapsed
        self.study_type.time_elapsed += 1
          
        #if study time has been reached (try to publish the first time) or has exceeded (try publishing again)                          
        if self.study_type.time_elapsed >= self.study_type.study_length:
                                               
            if self.study_type == 'replication':
                                   self.study_type.publishability = 1
                                   
                                   
                    
            elif self.study_type == 'novel':
                                   self.study_type.publishability = random.uniform(0, 1)#CHANGE_ME function of study effect size and power (which is already a function of sample size) and researcher impact
        
        else: pass

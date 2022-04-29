import random
import math, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector


class RESEARCHER(Agent):
    """
    Create a RESEARCHER agent
    """
    def __init__(
        self,
        unique_id,
        model,
        position: (float, float),
        agent_impact_distribution: str,
        initial_publication_count_distribution: str,
        interest_in_replication_distribution: str,
        sample_size_distribution: str,
        power_distribution: str,
        name: str = 'researcher'
        ):
        """
        Argument(s):
            position: position in arbitrary continuous space
            agent_impact_distribution: distribution to draw from for a researcher's impact in the SCIENTIFIFC_WORLD
            initial_publication_count_distribution: distribution to draw from for a researcher's inititial number of publications
            interest_in_replication_distribution: distribution to draw from for a researcher's probability of conducting a replication study
            sample_size_distribution: distribution to draw from for a study's sample size
            power_distribution: distribution to draw from for a study's inherent power without regards to sample size (power will be automatically adjusted for a given sample size)
            name: name
            """
        print('class RESEARCHER(Agent):.__init__')
        super().__init__(unique_id, model)
        
        self._name = name
        
        #agent's impact which is different from publication count since different feilds have different publication rates
        self.agent_impact_distribution = getattr(np.random, agent_impact_distribution)
        self.agent_impact = self.agent_impact_distribution(1)
        
        #researcher's permanent interest in replication studies
        self.interest_in_replication_distribution = getattr(np.random, interest_in_replication_distribution) #CHANGE_ME to be a function of researcher impact
        self.interest_in_replication = self.interest_in_replication_distribution(1)
        
        # #position within the arbitrary continuous space
        # self.x, self.y = self.position
                                   
        #initial publication count; since we don't want to start with all researchers at 0 which would not be possible unless research was "judt discovered"
        self.initial_publication_count_distribution = getattr(np.random, initial_publication_count_distribution)
        self.publication_count = self.initial_publication_count_distribution(1) #CHANGE_ME to be a function of interest in replication; higher interest in replications leads to more publications in general
        
        #how far a researcher can reach within the continuous space to collaborate with another researcher (e.g., high impact researchers can collaborate with anyone but low impact researchers can only collaborate with researchers with slightly higher impact than them)
        self.radius_of_collaboration = self.agent_impact + self.publication_count * self.interest_in_replication   #CHANGE_ME to a different formula; also more lenient                        
        
        #sample size distribution for when a new project is initiated
        self.sample_size_distribution = sample_size_distribution
        
        #sample size distribution for when a new project is initiated
        self.power_distribution = power_distribution
        
        #set global time to differentiate between first study conducted in run vs. subsequent studies; for all agents
        self.global_time = 0
        
        
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
        if self.study_type[0] == 'replication':
            #initiate a new study
            self.current_study = None
            #sample size of replication study
            self.current_study.sample_size = getattr(np.random, sample_size_distribution)//2 #CHANGE_ME to a different ratio/function that includes researcher impact
            #power of replication study
            self.current_study.power = getattr(np.random, power_distribution)//2 #CHANGE_ME to include sample size in equasion  
            #length of replication study
            self.current_study.study_length = getattr(np.random, sample_size_distribution) #CHANGE_ME add an equasion that includes sample size and researcher impact; shorter for 'replication'     
            #effect size of replication study; calculated upon study generation which is not representataive of the real world but won't induce any effects since we are doing a simulation
            self.current_study.study = getattr(np.random, power_distribution) #CHANGE_ME add an equasion that includes sample size in equasion

            # time = 0 for this specific study                           
            self.current_study.time_elapsed = 0

            print('study_is_a_replication')
        #generate a novel study                            
        elif self.study_type[0] == 'novel':
            #initiate a new study
            self.current_study = None
            #sample size of novel study
            self.current_study.sample_size = getattr(np.random, sample_size_distribution) #to function that includes researcher impact
            #power of novel study
            self.current_study.power = getattr(np.random, power_distribution) #CHANGE_ME to include equasion  
            #length of replication study
            self.current_study.study_length = random.uniform(-1, 5) #CHANGE_ME add an equasion that includes sample size and researcher impact; longer for 'replication'    
            #effect size of replication study; calculated upon study generation which is not representataive of the real world but won't induce any effects since we are doing a simulation
            self.current_study.effect_size = random.uniform(-1, 5) #CHANGE_ME add an equasion that includes sample size in equasion

            # time = 0 for this specific study                           
            self.current_study.time_elapsed = 0

            print('study_is_novel')
        
        else: raise ValueError('study_type was not "replication" or "novel" for "initiate_project" function')
        
                                   
    def publication_attempt(self):
        """
        Attempt to publish a research project for a given project for a given researcher.    
        """
        print('publication_attempted')     
        
        self.current_study.publish_status = random.choices(['published', 'rejected'],
            [self.current_study.publishability, 1-self.current_study.publishability])
                                   
        if self.current_study.publish_status[0] == 'published':
            self.publication_count += 1
            self.agent_impact += 1 #CHANGE_ME
            #start a new project after publishing
            self.move()
            self.initiate_project(self.sample_size_distribution, self.power_distribution)
                    
                                   
                                   
        elif self.current_study.publish_status[0] == 'rejected':
            self.current_study.publish_status.re_attempt_probability = random.uniform(0, 1) #CHANGE_ME to function dependednt on researcher impact, sample size, etc.
            self.current_study.publish_status.re_attempt_status = random.choices(['re_attempt', 'withhold'], 
                                                                              [self.current_study.publish_status.re_attempt_probability, 
                                                                               1-self.current_study.publish_status.re_attempt_probability])
                
            #try publishing again at next timestep
            if self.current_study.publish_status.re_attempt_status[0] == 're_attempt': pass

            #do not add to publication count or agent impact and start a new project
            elif self.current_study.publish_status.re_attempt_status[0] == 'withhold':
                self.move()
                self.initiate_project(self.sample_size_distribution, self.power_distribution)
                
            else: raise ValueError('RESEARCHER did not "re-attempt" to publish or "withheld" current_study; after a failed publication attemp')
                                   
        else: raise ValueError('current_study was not "published" or "rejected"')                           
                        
                
    def move(self): #CHANGE_ME change all parts of function to account for agent impact and radius of collaboration
            possible_steps = self.model.grid.get_neighborhood(
                self.position,
                moore=True,
                include_center=False)
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

                      
                                   
    def step(self):
        
        #if this is the start of the model's run, start by initiating a study
        if self.global_time == 0:
            self.initiate_project(self.sample_size_distribution, self.power_distribution)
        
        #if this is not the start of the model's run, update current study attributes
        elif self.global_time > 0:
        
            #update time elapsed
            self.current_study.time_elapsed += 1

            #if study time has been reached (try to publish the first time) or has exceeded (try publishing again)                          
            if self.current_study.time_elapsed >= self.current_study.study_length:

                if self.study_type[0] == 'replication':
                    #replications are always publishable
                    self.current_study.publishability = 1 #CHANGE_ME maybe change; ask JB
                    publication_attempt()
                    
                #novel studies have a publishability proabbaility as a function of multiple researcher and project parameters
                elif self.study_type[0] == 'novel':
                    self.current_study.publishability = random.uniform(0, 1)#CHANGE_ME function of study effect size and power (which is already a function of sample size) and researcher impact
                    publication_attempt()
                
                else: ValueError('study_type was not "replication" or "novel" for "step" function')
        
            else: pass
        
        else: raise ValueError('global_time is negative') 
        
        

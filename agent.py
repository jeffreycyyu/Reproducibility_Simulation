#study length is built in method or function error 
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
        
        #position within the arbitrary continuous space
        self.position = position
                                   
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

        global global_time
        global study_length
        global time_elapsed
        
        global_time = 0
        study_length = 0
        time_elapsed = 0

        
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
        
        global global_time
        global study_length
        global time_elapsed
        
        global study_type
        #decide project type (replication or novel)
        study_type = random.choices(
            ['replication', 'novel'],
            [self.interest_in_replication, 1-self.interest_in_replication])
        
                                   
        #generate a replication study         
        if study_type[0] == 'replication':
            #sample size of replication study
            self.sample_size = getattr(np.random, sample_size_distribution) #CHANGE_ME to a different ratio/function that includes researcher impact
            #power of replication study
            self.power = getattr(np.random, power_distribution) #CHANGE_ME to include sample size in equasion  
            #length of replication study
            study_length = getattr(np.random, sample_size_distribution) #CHANGE_ME add an equasion that includes sample size and researcher impact; shorter for 'replication' 
            #effect size of replication study; calculated upon study generation which is not representataive of the real world but won't induce any effects since we are doing a simulation
            self.study = getattr(np.random, power_distribution) #CHANGE_ME add an equasion that includes sample size in equasion

            # time = 0 for this specific study  
            time_elapsed = 0

            print('study_is_a_replication')
        #generate a novel study                            
        elif study_type[0] == 'novel':
            #sample size of novel study
            self.sample_size = getattr(np.random, sample_size_distribution) #to function that includes researcher impact
            #power of novel study
            self.power = getattr(np.random, power_distribution) #CHANGE_ME to include equasion  
            #length of replication study
            study_length = random.uniform(-1, 5) #CHANGE_ME add an equasion that includes sample size and researcher impact; longer for 'replication'    
            #effect size of replication study; calculated upon study generation which is not representataive of the real world but won't induce any effects since we are doing a simulation
            self.effect_size = random.uniform(-1, 5) #CHANGE_ME add an equasion that includes sample size in equasion
            
            # time = 0 for this specific study
            time_elapsed = 0

            print('study_is_novel')
        
        else: raise ValueError('study_type was not "replication" or "novel" for "initiate_project" function')
        
                                   
    def publication_attempt(self):
        """
        Attempt to publish a research project for a given project for a given researcher.    
        """
        print('publication_attempted')     
        
        self.publish_status = random.choices(['published', 'rejected'],
            [self.publishability, 1-self.publishability])
                                   
        if self.publish_status[0] == 'published':
            
            self.publication_count += 1
            self.agent_impact += 1 #CHANGE_ME
            #start a new project after publishing
            self.move()
            self.initiate_project(self.sample_size_distribution, self.power_distribution)
                    
                                   
                                   
        elif self.publish_status[0] == 'rejected':
            self.publish_status.re_attempt_probability = random.uniform(0, 1) #CHANGE_ME to function dependednt on researcher impact, sample size, etc.
            self.publish_status.re_attempt_status = random.choices(['re_attempt', 'withhold'], 
                                                                              [float(str(self.publish_status.re_attempt_probability)), 
                                                                               1-float(str(self.publish_status.re_attempt_probability))])
                
            #try publishing again at next timestep
            if self.publish_status.re_attempt_status[0] == 're_attempt': pass

            #do not add to publication count or agent impact and start a new project
            elif self.publish_status.re_attempt_status[0] == 'withhold':
                self.move()
                self.initiate_project(self.sample_size_distribution, self.power_distribution)
                
            else: raise ValueError('RESEARCHER did not "re-attempt" to publish or "withheld" current_study; after a failed publication attemp')
                                   
        else: raise ValueError('current_study was not "published" or "rejected"')                           
                        
                
    def move(self): #CHANGE_ME change all parts of function to account for agent impact and radius of collaboration
            possible_steps = self.model.grid.get_neighbors(self.position, 5.0)
            new_position = self.random.choice(possible_steps)
            self.model.ContinuousSpace.move_agent(self, new_position)
        
                                   
    def step(self):

        global global_time
        global study_length
        global time_elapsed
        
        #if this is the start of the model's run, start by initiating a study
        if global_time == 0:
            self.initiate_project(self.sample_size_distribution, self.power_distribution)
            
            #add a timestep to this agents perception of global time (do this regardless of agent or action taken)
            global_time += 1
        
        #if this is not the start of the model's run, update current study attributes
        elif global_time > 0:
            #update time elapsed
            time_elapsed += 1
            #add a timestep to this agents perception of global time (do this regardless of agent or action taken)
            global_time += 1

            #if study time has been reached (try to publish the first time) or has exceeded (try publishing again)  
            if time_elapsed >= study_length:
                
                global study_type

                if study_type[0] == 'replication':
                    #replications are always publishable
                    self.publishability = 1 #CHANGE_ME maybe change; ask JB
                    self.publication_attempt()
                    
                #novel studies have a publishability proabbaility as a function of multiple researcher and project parameters
                elif study_type[0] == 'novel':
                    self.publishability = random.uniform(0, 1)#CHANGE_ME function of study effect size and power (which is already a function of sample size) and researcher impact
                    self.publication_attempt()
                
                else: ValueError('study_type was not "replication" or "novel" for "step" function')
        
            else:
                
                global_time = global_time
                #add a timestep to this agents perception of global time (do this regardless of agent or action taken)
                global_time += 1
        
        else: raise ValueError('global_time is negative') 

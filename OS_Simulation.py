#Oliver Josué de León Milian
#19270
#Algoritmos y estructura de datos
#Universidad del Valle de Guatemala
#Fecha de entrega: 4 de marzo de 2020
#Operative System Simulation
#This progRAM simulates the execution of an operative system, simulating
#the use of components like RAM and CPU, all of these using python
#simulation tools.

#References
#_init_ model retrieved from: https://simpy.readthedocs.io/en/latest/simpy_intro/process_interaction.html
#Feedback retrieved from: @JulioH

import simpy
import random
import math

#Attributes
CPUs = 1 #Amount of available CPUs
CPUInstructions = 6  # Amount of CPUs instructions
InOut = 1  # I/O operation
Interval = 10 # Process intervale
Time = []  # Time periods 
random.seed(15) #Seed
ProAmount = 200 #Amount of process

#Storages the instances of RAM and CPU
class OperativeSystem:
    
    #Initialize the components of the simulation
    def __init__ (self, env): #Checks references at top of the doc
        #Initialization of RAM component as a container
        self.RAM = simpy.Container(env, init = 100, capacity = 100)
        #Initialization of CPU component as a resource
        self.CPU = simpy.Resource(env, capacity = CPUs)
    
#Execute Simulation
class OS_Simulation:
    

    #Initialize general attributes
    def __init__ (self, ID, i, env, OS):
        
        #Attributes
        #NOTE: self --> allows to get attributes
        self.env = env
        self.ID = ID#ID for each process
        self.i = i
        self.ended = False
        self.instructions = random.randint(1, 10)#Amount of instructions
        self.RequiredMemory = random.randint(1, 10)#Used memory        
        self.OS = OS#Operative System
        
        #Time
        self.originTime = 0
        self.finishedTime = 0
        self.totalTime = 0
        self.process = env.process(self.simulation(env, OS))

    # Follows the behavior of a process
    def simulation(self, env, OS):
        #States a starting time
        start = env.now
        self.originTime = start
        
        #Process has been created
        print('%s: Created in: %d' % (self.ID, start))
        #RAM is required
        with OS.RAM.get(self.RequiredMemory) as getRAM:  
            yield getRAM

            # starts use of RAM
            print('%s: Gets RAM in %d [Waiting]' % (self.ID, env.now))
            #Indicates running order
            next = 0
            #While it's not ended, CPU cannot be recalled
            while not self.ended:
                with OS.CPU.request() as req:  
                    print('%s: Waiting CPU in %d [Waiting]' % (self.ID, env.now))
                    yield req

                    # Starts use of CPU
                    print('%s: Gets CPU in %d [Running]' % (self.ID, env.now))
                    #Allowed amount of instructions are runned
                    for i in range(CPUInstructions):
                        #If there is any instruction, execute it 
                        if self.instructions > 0:
                            self.instructions -= 1
                            #Indicates if instructions are executable or are gonna wait
                            next = random.randint(1, 2)
                    #Amount of time
                    yield env.timeout(1) 

                    # starts process I/O
                    if next == 1:
                        print('%s: Waiting I/O operation in %d [I/O]' % (self.ID, env.now))
                        yield env.timeout(InOut)

                    # RAM killed
                    if self.instructions == 0:
                        self.ended = True  

            print('%s: Ended in %d [Ended]' % (self.ID, env.now))
            #Returns used RAM
            OS.RAM.put(self.RequiredMemory)  
        end = env.now
        #End Process
        self.finishedTime = end
        #Gets each process's time
        self.totalTime = int(self.finishedTime - self.originTime) 
        Time.insert(self.i, self.totalTime)


# Process generator
def process_generator(env, OS):
    for i in range(ProAmount):
        #Use the distribution of 1.0 interval
        originTime = math.exp(1.0/Interval)
        OS_Simulation('Process %d' % i, i, env, OS)
        #Amount of time that each process take to be completed
        yield env.timeout(originTime)  
        

###################################################################################################
#Enviroment is developed
env = simpy.Environment()
#Operative System is created
OS = OperativeSystem(env)
#Processes are created
env.process(process_generator(env, OS))
#Enviroment Runs af
env.run()
####################################################################################################

#Arithmetic stuff
def average(s): return sum(s) * 1.0 / len(s)
#Gets average time
overallTime = average(Time)
varianceTime = map(lambda x: (x - overallTime) ** 2, Time)
#Gets standard deviation
totalTime = math.sqrt(average(list(varianceTime))) 
#Average Statement
print("Average time: ", overallTime, ", Standard deviation: ", \
      totalTime)

        
    
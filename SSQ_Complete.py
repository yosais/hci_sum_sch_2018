from random import *
from queue import *
from statistics import *
from math import *

# Simulation parameters
lamda = 0.2 
mu = 0.3
n = 10000   # Number of simulated packets

# Unique ID for each event
evID = 0

# Count number of simulated packets
count = 0

# State variables
Q = 0
S = False   # Server is free

# Output variables
arrs = [] 
deps = []

# Event list
evList = None

# REG for the arrival event
def get_next_arrival_event (clock):
    global evID
    iat = expovariate(lamda)
    ev = ( clock + iat , evID, arrival_event_handler )
    evID += 1
    return ev

# REG for the departure event	
def get_next_departure_event (clock):
    global evID
    st = expovariate(mu)
    ev = ( clock + st , evID, departure_event_handler )
    evID += 1
    return ev

# Event handler for the arrival event
def arrival_event_handler (clock):
    global n, count, Q, S, arrs
    Q += 1
    arrs.append(clock)  # Record arrival time
    if S == False:
        S = True
        schedule_event( get_next_departure_event(clock) )
    count += 1
    if count < n:	
        schedule_event( get_next_arrival_event(clock) )

# Event handler for the departure event	
def departure_event_handler (clock):
    global Q, S, deps
    Q -= 1
    deps.append(clock)  # Record departure time
    if Q == 0:
        S = False
    else:
        S = True
        schedule_event( get_next_departure_event(clock) )

# Insert an event into the event list		
def schedule_event(ev):
    global evList
    evList.put(ev)

# Main simulation function
def sim():
    global Q, S, arrs, deps, count, evList
    clock = 0
    evList = PriorityQueue()
    # Reset state and output variables
    Q = 0
    S = False
    arrs = []
    deps = []
    count = 0
    # Insert initial events
    ev = get_next_arrival_event(clock)
    schedule_event(ev)
    # Start simulation
    while not evList.empty():
        ev = evList.get()
        clock = ev[0]
        ev[2](clock)

def main():
    global arrs, deps
    m = 50  # Number of replications
    Samples = []
    for i in range(m):
        d = []
        seed()  # Reseed RNG
        sim()
        d = list( map(lambda x,y: x-y, deps, arrs) )
        Samples.append( mean(d) )
    
    sample_mean = mean(Samples)
    sample_std_dev = stdev(Samples)
    t = 1.96
    ci1 = sample_mean - t * (sample_std_dev / sqrt(m))
    ci2 = sample_mean + t * (sample_std_dev / sqrt(m))

    print( "Average Delay = ", round(sample_mean, 2) )
    print( "Confidence Interval: ", "( ", round(ci1, 2), ", ", round(ci2, 2), " )" )
    print( "Population Mean = ", round(1 / (mu-lamda), 2) )

if __name__ == '__main__':
    main()

### Example output
# Average Delay =  10.09
# Confidence Interval:  (  9.96 ,  10.21  )
# Population Mean = 10.0
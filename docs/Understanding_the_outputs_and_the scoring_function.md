# Understanding the outputs and the scoring function

## Where are the outputs stored?

After the last simulation's iteration, the system reaches an *equilibrium state*: the simulation stops. All the outputs generated during this run are stored in a unique output folder *output/siouxfalls-1k__\<date>_\<time>*. (See figure).

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Output_folder_2.png)
Figure 1: Outputs of the simulation

## Scoring function

The main outputs you should be focusing on are the one located in the *competition* folder. 

It contains: 
* The [input files](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Which-inputs-should-I-optimize%3F.md) you used for the simulation run
* The subscores and the general score from the scoring function, which evaluates the quality of the policy-based transportation sytsem 

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/The_scoring_function.png)
Figure 2: Score and subscores

The *scoring function* is a weighted sum of several components: 
* Measures of **congestion**:
  * **vehile hours of delay**: total hours of delay experienced by all motorized vehicles of the system during the simulation. Delay is measured as the difference between the free-flow travel time over the path of a vehicle movement and the actual duration of the movement in the simulation. 
  * **vehicle-miles traveled**: total miles traveled by all motorized vehicles of the system during the simulation.
  
* Measures of **the level of service** of the transportation system:
  * **travel cost**: total trip cost incurred by all agents during the simulation.
  * **bus crowding**:  the total time in hours spent by agents standing in buses occupied above their seating capacity.

* Measures of the **costs** incurred by the city:
  * **operational cost**: total costs incurred by SFBL operations including amortized fixed costs, the cost of fuel consumed, and variable fixed costs. The rates for each of these factors is specified in the vehicle configuration and will be known by contestants when choosing which vehicles to include in the bus fleet.
  * **incentives used**: total incentives used by agents.
  * **incentives unused**: total incentives available but unused by agents. 
  * **revenues**: total bus fares collected


## How to interpret the outputs?



![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Measures_of_congestion.png)

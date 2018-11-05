# Understanding the outputs and the scoring function
After reading this document, you will have a better understanding of the outputs of the simulation, where they are stored after a simulation run, what do they describe and how to interpret them.

## Where are the outputs stored?

After the last simulation's iteration, the system reaches an *equilibrium state*: the simulation stops. All the outputs generated during this run are stored in a unique output folder called *output/siouxfalls-1k__\<date>_\<time>*. It ends with the date and time of the simulation you have just ruuned (see figure).

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Output_folder_2.png)

Figure 1: Outputs of the simulation

## Scoring function

The main outputs you should be focusing on are the one located in the *competition* folder. It contains: 

* The [input files](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Which-inputs-should-I-optimize%3F.md) you used for the simulation run
* The *subscores* and the *general score* from the scoring function, which evaluates the quality of the policy-based transportation sytsem 

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/The_scoring_function.png)
Figure 2: Score and subscores

The *scoring function* is a weighted sum of several components: 
* Measures of **congestion**:
  * **vehile hours of delay** (): total hours of delay experienced by all motorized vehicles of the system during the simulation. Delay is measured as the difference between the free-flow travel time over the path of a vehicle movement and the actual duration of the movement in the simulation. 
  * **vehicle-miles traveled**: total miles traveled by all motorized vehicles of the system during the simulation.

* Measures of **the level of service** of the transportation system:
  * **travel cost**: total trip cost incurred by all agents during the simulation.
  * **bus crowding**:  the total time in hours spent by agents standing in buses occupied above their seating capacity.

* Measures of the **costs** incurred by the city:
  * **operational cost**: total costs incurred by SFBL operations including amortized fixed costs, the cost of fuel consumed, and variable fixed costs. The rates for each of these factors is specified in the vehicle configuration and will be known by contestants when choosing which vehicles to include in the bus fleet.
  * **incentives used**: total incentives used by agents.
  * **incentives unused**: total incentives available but unused by agents. 
  * **revenues**: total bus fares collected

If you want to know more about the mathematical formulation of each of these scoring function components, read the section 4.3 of the [Sioux Faux Hackhaton problem statement]() **link**.

## Other outputs

Besides the scores, the *output/siouxfalls-1k__\<date>_\<time>* folder contains a few graphs with their corresponding textfiles. Their are listed below.

* **Mode choice**
The mode choice graph describes the overall distribution of chosen modes per agent's preference for each iteration of the simulation. In the exemple shown in Fig.3 below, the simulation ended after 100 iterations. In the simulation, agents received a 20$ subsidy per person. Throughout the iterations, we can see that this incentives to take public transit works: the agents leave progressively leave the car for on-demand rideshare and transit.    
![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Mode_choice_histogram.png)
Figure 3: Mode choice of agents for each iteration of the simulation.

* **Ride-hail revenue**

* **Ride-hail stats**

* **Scorestats**

## Summary stats

The *summaryStats.csv* document gathers all raw outputs of the simulation. Their meanings are listed below:

* *agentHoursOnCrowdedTransit*: total time spent by agents in a crowded transit vehicle (with people standing) \[hours]
* *fuelConsumedInMJ_Diesel*:  
* *fuelConsumedInMJ_Food*: ?
* *fuelConsumedInMJ_Gasoline*
* *numberOfVehicles_BODY-TYPE-DEFAULT*: number of vehicles in the system 
* *numberOfVehicles_BUS-DEFAULT*: number of buses of type "DEFAULT" circulating in the system during the day \[units]
* *numberOfVehicles_BUS-SMALL-HD*: number of buses of type "SMALL-HD" circulating in the system during the day \[units]
* *numberOfVehicles_BUS-STD-ART*: number of buses of type "STD-ART" circulating in the system during the day \[units]
* *numberOfVehicles_CAR-TYPE-DEFAULT*: number of cars of type "DEFAULT" circulating in the system during the day \[units]
* *personTravelTime_car*: total time traveled by car by all agents during the day \[person.hours]
* *personTravelTime_drive_transit*: total time traveled by public transit (bus) by all agents during the day \[person.hours]
* *personTravelTime_others*: total time traveled by any  mean different from the bus, the car or walking by all agents during the day \[person.hours]
* *personTravelTime_ride_hail*: total time traveled by on-demand rideshare by all agents during the day \[person.hours]
* *personTravelTime_walk*: total time traveled by foot by all agents during the day \[person.hours]
* *personTravelTime_walk_transit*: total time spent by foot to access public transit by all agents during the day \[person.hours]
* *totalCostIncludingSubsidy_drive_transit*: **SID?**
* *totalCostIncludingSubsidy_ride_hail*: **SID?**
* *totalCostIncludingSubsidy_walk_transit*: **SID?**
* *totalSubsidy_drive_transit*: total subsidies \[$/person] received by all agents for accessing public transit by car \[$] 
* *totalSubsidy_ride_hail*: total subsidies \[$/person] received by all agents for accessing public transit by on-demand rideshare \[$] 
* *totalSubsidy_walk_transit*: total subsidies \[$/person] received by all agents for accessing public transit by foot \[$] 
* *totalTravelTime*: total time traveled by all agents during the day \[hours]
* *totalVehicleDelay*: total hours of delay experienced by all motorized vehicles of the system during the simulation \[hours]
* *vehicleHoursTraveled_BODY-TYPE-DEFAULT*: **SID?**
* *vehicleHoursTraveled_BUS-DEFAULT*: total time traveled by bus of type "DEFAULT" during the day \[vehicle.hours] 
* *vehicleHoursTraveled_BUS-SMALL-HD*:total time traveled by bus of type "SMALL-HD" during the day \[vehicle.hours] 
* *vehicleHoursTraveled_BUS-STD-ART*: total time traveled by bus of type "STD-ART" during the day \[vehicle.hours] 
* *vehicleHoursTraveled_CAR-TYPE-DEFAULT*: : total time traveled by car of type "DEFAULT" during the day \[vehicle.hours] 
* *vehicleMilesTraveled_BODY-TYPE-DEFAULT*: total time traveled by bus of type "DEFAULT" during the day \[vehicle.hours] 
* *vehicleMilesTraveled_BUS-DEFAULT*: total miles traveled by bus of type "DEFAULT" \[vehicle.miles]
* *vehicleMilesTraveled_BUS-SMALL-HD*: total miles traveled by bus of type "SMALL-HD" \[vehicle.miles]
* *vehicleMilesTraveled_BUS-STD-ART*: total miles traveled by bus of type "STD-ART" \[vehicle.miles]
* *vehicleMilesTraveled_CAR-TYPE-DEFAULT*: total miles traveled by car of type "DEFAULT" \[vehicle.miles]
* *vehicleMilesTraveled_total*: total miles traveled by motorized vehicles \[vehicle.miles]



![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Measures_of_congestion.png)

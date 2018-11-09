# Understanding the outputs and the scoring function
After reading this document, you will have a better understanding of the outputs of the simulation, where they are stored after a simulation run, what they describe, and how to interpret them.

## Where are the outputs stored?

After the simulation's last iteration, the system reaches an *equilibrium state* and the simulation stops. All the outputs generated during this last run are stored in a unique output folder called `output/siouxfalls-1k__\<date>_\<time>`. It ends with the date and time of the simulation you have just run (see Figure 1). Note that the figure references a simulation run with a 1k population sample.

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Output_folder_2.png)

Figure 1: Outputs of the simulation

## Scoring function

The main outputs you should focus on are located in the `competition` folder. It contains: 

* The [input files](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Which-inputs-should-I-optimize%3F.md) you used for the simulation run
* The *component scores* and the *submission score* from the scoring function, which evaluates the quality of the policy-based transportation sytsem 

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/The_scoring_function.png)
Figure 2: Score and component scores

The *scoring function* is a weighted sum of several components, listed below. ***Weights are pre-determined based upon...\[fill in]*** 
* Measures of **congestion**:
  * **vehicle-hours of delay** (`Congestion: Vehicle Hours Delay`, \[veh-hours]): total hours of delay experienced by all motorized vehicles in the system during the simulation. Delay is measured as the difference between the free-flow travel time over the path of a vehicle's movement and the actual duration of the movement in the simulation. 
  * **vehicle-miles traveled** (`Congestion: Vehicle Miles Traveled`, \[veh-miles]): total miles traveled by all motorized vehicles in the system during the simulation.

* Measures of **the level of service** of the transportation system:
  * **travel cost** (`Level of Service: Travel expenditures`, \[$]): total trip cost incurred by all agents during the simulation. 
  * **bus crowding** (`Level of Service: Agent Hours on Crowding Transit`,\[hours]): the total time spent by agents standing in buses occupied above their seating capacity. 

* Measures of the **Budget** incurred by the city:
  * **operational cost**, \[$]: total costs incurred by SFBL operations including amortized fixed costs (`Budget : Operational Costs (Fixed)`), the cost of fuel consumed (`Budget : Operational Costs (Fuel)`), and variable costs (`Budget : Operational Costs (Variable, Hourly)`). The rates for each of these factors for motorized vehicles are specified in the `fixed-data/siouxfalls/vehicleTypes.csv` file (see the [inputs](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Which-inputs-should-I-optimize%3F.md) page for more).
  * **incentives used** (`Budget: Subsidies Paid`, \[$]): total incentives used by agents.
  * **incentives unused** (`Budget: Subsidies Unpaid`, \[$]): total incentives available but unused by agents. 
  * **revenues**, (\[$]): total bus fares collected

If you want to know more about the mathematical formulation of each of these scoring function components, read ***check reference section 4 and  4.3*** of the [Sioux Faux Hackathon problem statement]() **link**.

## Other outputs

In addition to the scores, the `output/siouxfalls-1k__\<date>_\<time>` folder contains graphs describing performance outputs of the system along with their corresponding data files. Two of them are described below.

* **Mode choice**
The mode choice graph describes the overall distribution of chosen modes for each iteration of the simulation. In the example shown in Figure 3 below, the simulation ended after 100 iterations. In the simulation, every agent received a $20 subsidy per ride for ridehail. As the iterations progressed, you can see that this incentives to use on-demand rideshare worked: the agents progressively shifted away from cars towards ridehail.    
![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Mode_choice_histogram.png)
Figure 3: Mode choice of agents for each iteration of the simulation

* **Ride-hail revenue**
The ride-hail revenues describe the revenues made by the ridehail company with the fares of the course. 

* **Scorestats**
The score statistics represent the evolution of the agent's plans scores during the simulation. Each iteration simulates one entire day. At the end of each iteration, the daily plan of each agent is evaluated according to how well it performed in the transportation scenario. Based on this score, some agents may change their daily plan (which modes they use to travel from and to their activities) for the next iteration in an attempt to improve it. This learning mechanism can be observed in the Figure 4 below: as iterations progress, the agents' plan scores keep increasing till they reach a plateau after about 50 iterations: the system has reached an equilibrium state where each agent has found its optimal daily plan.

![alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/scorestats.png)
Figure 4: Statistics of agent scores 

## Summary stats

The `summaryStats.csv` file gathers many of the raw outputs of the simulation, which are themselves used to compute the scoring functions.  Details for each output are listed below:

* `agentHoursOnCrowdedTransit`: total time spent by agents in a crowded transit vehicle (with people standing) \[hours]
* `fuelConsumedInMJ_Diesel`: overall amount (in MJ) of diesel consumed by buses during the day
* `fuelConsumedInMJ_Food`: overall amount (in MJ) of food consumed by pedestrians during the day
* `fuelConsumedInMJ_Gasoline`: overall amount (in MJ) of gasoline consumed by cars during the day
* `numberOfVehicles_BODY-TYPE-DEFAULT`: number of vehicles in the system 
* `numberOfVehicles_BUS-DEFAULT`: number of buses of type "DEFAULT" circulating in the system during the day \[units]
* `numberOfVehicles_BUS-SMALL-HD`: number of buses of type "SMALL-HD" circulating in the system during the day \[units]
* `numberOfVehicles_BUS-STD-ART`: number of buses of type "STD-ART" circulating in the system during the day \[units]
* `numberOfVehicles_CAR-TYPE-DEFAULT`: number of cars of type "DEFAULT" circulating in the system during the day \[units]
* `personTravelTime_car`: total time traveled by car by all agents during the day \[person.hours]
* `personTravelTime_drive_transit`: total time traveled by public transit (bus) by all agents during the day \[person.hours]
* `personTravelTime_others`: total time traveled by any  mean different from the bus, the car or walking by all agents during the day \[person.hours]
* `personTravelTime_ride_hail`: total time traveled by on-demand rideshare by all agents during the day \[person.hours]
* `personTravelTime_walk`: total time traveled by foot by all agents during the day \[person.hours]
* `personTravelTime_walk_transit`: total time spent by foot to access public transit by all agents during the day \[person.hours]
<!--TODO: The following stats will be improved for clarity, issue open on BEAM-->
<!--* `totalCostIncludingSubsidy_drive_transit`: **SID*-->
<!--* `totalCostIncludingSubsidy_ride_hail`: **SID?**-->
<!--* `totalCostIncludingSubsidy_walk_transit`: **SID?**-->
* `totalSubsidy_drive_transit`: total subsidies \[$US/person] received by all agents to incentivize trips that access public transit by car \[$US]
* `totalSubsidy_ride_hail`: total subsidies \[$US/person] received by all agents to incentivize trips using on-demand rideshare \[$US]
* `totalSubsidy_walk_transit`: total subsidies \[$US/person] received by all agents to incentivize trips that access public transit on foot \[$US]
* `totalTravelTime`: total time spent traveling by all agents during the day \[person-hours]
* `totalVehicleDelay`: total hours of delay experienced by all motorized vehicles of the system during the simulation \[vehicle-hours]
* `vehicleHoursTraveled_BODY-TYPE-DEFAULT`: total time traveled by foot during the day \[vehicle-hours]. Note that in BEAM, person agents are considered to be "human body vehicles".
* `vehicleHoursTraveled_BUS-DEFAULT`: total time traveled by bus of type "DEFAULT" during the day \[vehicle-hours]
* `vehicleHoursTraveled_BUS-SMALL-HD`: total time traveled by bus of type "SMALL-HD" during the day \[vehicle-hours]
* `vehicleHoursTraveled_BUS-STD-ART`: total time traveled by bus of type "STD-ART" during the day \[vehicle-hours]
* `vehicleHoursTraveled_CAR-TYPE-DEFAULT`: total time traveled by car of type "DEFAULT" during the day \[vehicle-hours]
* `vehicleMilesTraveled_BODY-TYPE-DEFAULT`: total time traveled by bus of type "DEFAULT" during the day \[vehicle-hours]
* `vehicleMilesTraveled_BUS-DEFAULT`: total miles traveled by bus of type "DEFAULT" \[vehicle-miles]
* `vehicleMilesTraveled_BUS-SMALL-HD`: total miles traveled by bus of type "SMALL-HD" \[vehicle-miles]
* `vehicleMilesTraveled_BUS-STD-ART`: total miles traveled by bus of type "STD-ART" \[vehicle-miles]
* `vehicleMilesTraveled_CAR-TYPE-DEFAULT`: total miles traveled by car of type "DEFAULT" \[vehicle-miles]
* `vehicleMilesTraveled_total`: total miles traveled by motorized vehicles \[vehicle-0miles]

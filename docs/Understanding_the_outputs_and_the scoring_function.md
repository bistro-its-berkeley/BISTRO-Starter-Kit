# Understanding the outputs and the scoring function
After reading this document, you will have a better understanding of the outputs of the simulation, where they are stored after a simulation run, what they describe, and how to interpret them.

## Where are the outputs stored?


Outputs are produced after the simulation's last iteration (see the [Introduction to the Urban Transportation System Optimization Framework](./Introduction_transportation_problem.md) page). All the outputs generated during this last run are stored in a unique output folder called `output/siouxfaux-<sample_size>__\<date>_\<time>`. It ends with the date and time of the simulation you have just run (see Figure 1). Note that the figure references a simulation run with a 1k population sample.

![Alt text](/Images/Output_folder_2.png)

Figure 1: Outputs of the simulation

## Scoring function

The main outputs you should focus on are located in the `competition` folder. It contains: 

* The [input files](./Which-inputs-should-I-optimize.md) you used for the simulation run
* The *component scores* and the *submission score* from the scoring function, which evaluates the quality of the policy-based transportation sytsem 

![Alt text](/Images/Subscores.png)
Figure 2: Score and component scores

The *scoring function* is a weighted sum of several components, listed below. If you want to read more about the weights of the scoring function, go to section 6.2 of the [scoring document](./Problem_statement_Phase%20I.pdf).

* Measures of **accessibility**:
  * **work-based trips** (`Accessibility: Number of work locations accessible within 15 minutes`): The sum of the average number of work locations accessible from each node by automotive modes within 15 minutes during the AM peak (7-10 am) and PM peak (5-8 pm) periods.
  * **all other trips** (`Accessibility: Number of secondary locations accessible within 15 minutes`): } The sum of the average number of secondary locations accessible from each node by automotive modes within 15 minutes during the AM peak (7-10 am) and PM peak (5-8 pm) periods.

* Measures of **congestion**:
  * **total Vehicle-Miles Traveled** (`Congestion: total vehicle miles traveled`, \[veh-miles]): total miles traveled by all motorized vehicles of the system during the simulation.
  * **average Vehicle Delay per Person Agent Trip** (`Congestion: average vehicle delay per passenger trip`, \[veh-hours]): the average across agent trips of vehicle hours of delay experienced by all vehicles while occupied by one or more passengers during the simulation
  
* Measures of **the level of service** of the transportation system:
  * **average Travel Expenditure** (`Level of service: average trip expenditure - secondary` and `Level of service: average trip expenditure - work`, \[$]): the average over all trips of the total cost of travel incurred by all person agents during the simulation. Average travel expenditure are assessed for work trips and secondary trips separately.
  * **average Bus Crowding Experienced** (`Level of Service: Agent Hours on Crowding Transit`,\[agent-hours]): the average time spent per agent trip in buses occupied above their seating capacity.
  * **average On-Demand Rides Wait times** (`Level of service: average on-demand ride wait times`, \[hours/ride]):the average wait time agents experience before the on-demand rideshare vehicle arrives.  

* Measures of the **Costs and Benefits of Mass Transit Level of Service Intervention** incurred by the city:
The three following components are gathered in the `Mass transit level of service intervention: costs and benefits` subscore.
  * **operational cost**, \[$]: total costs incurred by SFBL operations including the cost of fuel consumed, and
hourly variable costs.  The rates for each of these factors is specified in the vehicle configuration and
will be known by contestants.
  * **incentives used** (\[$]: total incentives actually used by agents.
  * **revenues**, (\[$]): sum of total bus fares collected
 
* Measures of the **Sustainability**:
  * **Particulate (PM 2.5) Emissions** (`Sustainability: Total PM 2.5 Emissions`, \[g]): total PM 2.5 emissions produced by all motorized vehicles during the simulation.

If you want to know more about the mathematical formulation of each of these scoring function components, read sections 4.3 and 5.3 of the [Sioux Faux  problem statement](./Problem_statement_Phase%20I.pdf).

## Other outputs

In addition to the scores, the `output/siouxfaux-<sample_size>__\<date>_\<time>` folder contains graphs describing performance outputs of the system along with their corresponding data files. Two of them are described below.

* **Mode choice**

The mode choice graph describes the overall distribution of chosen modes for each iteration of the simulation. In the example shown in Figure 3 below, the simulation ended after 100 iterations. In the simulation, every agent received a $20.00 incentive per ride for on-demand rideshare. As the iterations progressed, you can see that providing a monetary incentive for some agents to use on-demand rideshare indeed shifted more agents towards using this mode.
![Alt text](/Images/Mode_choice_histogram.png)
Figure 3: Mode choice of agents for each iteration of the simulation

* **On-demand rides revenue**
The on-demand rides revenues component describes the net revenues earned by the on-demand rideshare company .

* **Score Statistics**
The score statistics represent the evolution of the agent's plans scores during the simulation. Each iteration simulates one entire day. At the end of each iteration, the daily plan of each agent is evaluated according to how well it performed in the transportation scenario. Based on this score, some agents may change their daily plan (which modes they use to travel from and to their activities) for the next iteration in an attempt to improve it. This learning mechanism can be observed in the Figure 4 below: as iterations progress, the agents' plan scores keep increasing until they reach a plateau after about 50 iterations. Once each agent can no longer find plans that improve their score, the system has reached an equilibrium state.

![alt text](/Images/scorestats.png)
***Figure 4: Statistics of agent scores***


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
* `personTravelTime_drive_transit`: total time traveled by mass transit (bus) by all agents during the day \[person.hours]
* `personTravelTime_others`: total time traveled by any  mean different from the bus, the car or walking by all agents during the day \[person.hours]
* `personTravelTime_ride_hail`: total time traveled by on-demand rideshare by all agents during the day \[person.hours]
* `personTravelTime_walk`: total time traveled by foot by all agents during the day \[person.hours]
* `personTravelTime_walk_transit`: total time spent by foot to access mass transit by all agents during the day \[person.hours]
* `totalCost_drive`: total cost of a trip where driving alone is the only mode used \[$US]
* `totalCost_ride_hail`: total cost of a on-demand ride \[$US]
* `totalCost_drive_transit`: total cost of a transit trip where driving alone is the access or egress mode \[$US]
* `totalCost_walk_transit`: total cost of a transit trip where walk is the access or egress mode \[$US]
* `totalIncentive_drive_transit`: total incentives \[$US/person] received by all agents to incentivize trips that access mass transit by car \[$US]
* `totalIncentive_ride_hail`: total incentives \[$US/person] received by all agents to incentivize trips using on-demand rideshare \[$US]
* `totalIncentive_walk_transit`: total incentives \[$US/person] received by all agents to incentivize trips that access mass transit on foot \[$US]
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

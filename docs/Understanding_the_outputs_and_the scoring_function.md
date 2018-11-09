# Understanding the outputs and the scoring function
After reading this document, you will have a better understanding of the outputs of the simulation, where they are stored after a simulation run, what they describe, and how to interpret them.

## Where are the outputs stored?

***Is there a maximum number of iterations, or a stopping criteria for equilibrium?*** After the simulation's last iteration, the system reaches an *equilibrium state* and the simulation stops. All the outputs generated during this last run are stored in a unique output folder called `output/siouxfalls-1k__\<date>_\<time>`. It ends with the date and time of the simulation you have just run (see Figure 1). Note that the figure references a simulation run with a 1k population sample.

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
  * **vehicle hours of delay** (`Congestion: Vehicle Hours Delay`, \[veh-hours]): total hours of delay experienced by all motorized vehicles in the system during the simulation. Delay is measured as the difference between the free-flow travel time over the path of a vehicle's movement and the actual duration of the movement in the simulation. 
  * **vehicle-miles traveled** (`Congestion: Vehicle Miles Traveled`, \[veh-miles]): total miles traveled by all motorized vehicles in the system during the simulation.

* Measures of **the level of service** of the transportation system:
  * **travel cost** (`Level of Service: Travel expenditures`, \[$]): total trip cost incurred by all agents during the simulation. 
  * **bus crowding** (`Level of Service: Agent Hours on Crowding Transit`,\[hours]): the total time spent by agents standing in buses occupied above their seating capacity. 

* Measures of the **Budget** incurred by the city:
  * **operational cost**, \[$]: total costs incurred by SFBL operations including amortized fixed costs (`Budget : Operational Costs (Fixed)`), the cost of fuel consumed (`Budget : Operational Costs (Fuel)`), and variable costs (`Budget : Operational Costs (Variable, Hourly)`). The rates for each of these factors for motorized vehicles are specified in the `fixed-data/siouxfalls/vehicleTypes.csv` file (see the [inputs](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Which-inputs-should-I-optimize%3F.md) page for more).
  * **incentives used** (`Budget: Subsidies Paid`, \[$]): total incentives used by agents.
  * **incentives unused** (`Budget: Subsidies Unpaid`, \[$]): total incentives available but unused by agents. 
  * **revenues**, (\[$]): total bus fares collected **SID?**

If you want to know more about the mathematical formulation of each of these scoring function components, read ***check reference section 4 and  4.3*** of the [Sioux Faux Hackathon problem statement]() **link**.

## Other outputs

In addition to the scores, the `output/siouxfalls-1k__\<date>_\<time>` folder contains graphs describing performance outputs of the system along with their corresponding data files, listed below.

* **Mode choice**
The mode choice graph describes the overall distribution of chosen modes for each iteration of the simulation. In the example shown in Figure 3 below, the simulation ended after 100 iterations. In the simulation, every agent received a $20 subsidy per ride ***for ridehail and/or public transit?***. As the iterations progressed, you can see that this incentives to take ***public transit and/or ridehail*** worked: the agents progressively shifted away from cars towards ridehail and transit.    
![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Mode_choice_histogram.png)
Figure 3: Mode choice of agents for each iteration of the simulation

* **Ride-hail revenue**

* **Ride-hail stats**

* **Scorestats**

## Summary stats

The `summaryStats.csv` file gathers all the raw outputs of the simulation. Details for each output are listed below:

* `agentHoursOnCrowdedTransit`: total time spent by agents in a crowded transit vehicle (with people standing) \[hours]
* `fuelConsumedInMJ_Diesel`:  
* `fuelConsumedInMJ_Food`: ?
* `fuelConsumedInMJ_Gasoline`
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
* `totalCostIncludingSubsidy_drive_transit`: **SID?**
* `totalCostIncludingSubsidy_ride_hail`: **SID?**
* `totalCostIncludingSubsidy_walk_transit`: **SID?**
* `totalSubsidy_drive_transit`: total subsidies \[$/person] received by all agents for accessing public transit by car \[$] 
* `totalSubsidy_ride_hail`: total subsidies \[$/person] received by all agents for accessing public transit by on-demand rideshare \[$] 
* `totalSubsidy_walk_transit`: total subsidies \[$/person] received by all agents for accessing public transit by foot \[$] 
* `totalTravelTime`: total time traveled by all agents during the day \[hours]
* `totalVehicleDelay`: total hours of delay experienced by all motorized vehicles of the system during the simulation \[hours]
* `vehicleHoursTraveled_BODY-TYPE-DEFAULT`: **SID?**
* `vehicleHoursTraveled_BUS-DEFAULT`: total time traveled by bus of type "DEFAULT" during the day \[vehicle.hours] 
* `vehicleHoursTraveled_BUS-SMALL-HD`: total time traveled by bus of type "SMALL-HD" during the day \[vehicle.hours] 
* `vehicleHoursTraveled_BUS-STD-ART`: total time traveled by bus of type "STD-ART" during the day \[vehicle.hours] 
* `vehicleHoursTraveled_CAR-TYPE-DEFAULT`: total time traveled by car of type "DEFAULT" during the day \[vehicle.hours] 
* `vehicleMilesTraveled_BODY-TYPE-DEFAULT`: total time traveled by bus of type "DEFAULT" during the day \[vehicle.hours] 
* `vehicleMilesTraveled_BUS-DEFAULT`: total miles traveled by bus of type "DEFAULT" \[vehicle.miles]
* `vehicleMilesTraveled_BUS-SMALL-HD`: total miles traveled by bus of type "SMALL-HD" \[vehicle.miles]
* `vehicleMilesTraveled_BUS-STD-ART`: total miles traveled by bus of type "STD-ART" \[vehicle.miles]
* `vehicleMilesTraveled_CAR-TYPE-DEFAULT`: total miles traveled by car of type "DEFAULT" \[vehicle.miles]
* `vehicleMilesTraveled_total`: total miles traveled by motorized vehicles \[vehicle.miles]

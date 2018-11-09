# Which inputs should I optimize?


To optimize the transportation system of Sioux Faux, you will need to write an algorithm that generates different inputs according to a specified format. This document provides information on the configurable inputs available to you.
 
## Overview of the repository

The repository details all the required inputs to run the BEAM simulation for the Sioux Faux scenario. You will only have control over some of them (the inputs to optimize), while others are fixed.

For more information on the folders discussed below, see the [How to run a simulation?](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/How_to_run_a_simulation%3F.md) page.

### The Internal Pilot Test inputs to optimize

To help the Sioux Faux Department of Transportation (SFDOT) combat congestion and improve overall mobility in Sioux Faux, you will prepare a set of inputs to the simulation engine, which represent the following transportation system interventions: the composition of the vehicles in the bus fleet and the subsidies for transit and ridehail. These to-be-optimized inputs can be found in .csv format in the `submission-inputs` folder.

#### **Bus fleet composition**

The submission input file *VehicleFleetMix.csv* describes the status of the bus fleet (see Fig.1). Currently, Sioux Faux Bus Lines (SFBL) operates buses on 12 routes in Sioux Faux. During the Pilot Study, you can decide which type of bus  will provide service for each route. Each route may be assigned only **one type of bus**. 

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/Input_VehicleFleetMix.png "*Figure 2: Input1 - composition of the bus fleet")
***Figure 1: Input1 - Bus fleet composition***

SFDOT has four available bus types, each of them with different technical properties (`fixed-data/siouxfalls/vehicleTypes.csv`, see Fig.2) and cost characteristics (`fixed-data/siouxfalls/vehicleCosts.csv`, see Fig.3). Currently, SFDOT owns the minimum number of bus types to provide service for each route, as specifed in the file *submission-inputs/VehicleFleetMix.csv*. Additionally, the number of buses required to service each route is equal to the number of trips: for each headway dispatched, a new bus is used. This does not reflect a realistic scenario combining bus routes into runs, but, for now, it still allows for comparisons to a BAU case.

During the Pilot Study, for each route, you have the opportunity to purchase new types of buses possessing attributes that might improve the level of service for transit along a route (see Figure 2 below).

*Figure to change*
![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/BusTypes.png "Figure 2: Set of available bus types")
***Figure 2: Set of available bus types***



![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/BusCosts.png "Figure 3: Costs of available bus types")
***Figure 3: Costs of available bus types***

#### **Subsidies for transit and on-demand rideshare users**

In an effort to provide a high-quality alternative to private vehicles, you may define subsidies for qualifying agents using public transit or on-demand ridehail. Qualification for a subsidy can be based on the following socio-demographic categories: age and/or income (***and employment status***). The choice of utilized socio-demographic qualifier(s), range(s), mode(s), and subsidy amount(s) are all inputs that you can define. For the hackathon, there is no upper limit to the number of times an agent can claim a subsidy throughout the day.

The Figure 4 below shows an example input file with subsidies for specific socio-demographic groups. These are defined as in mathematical notation where parentheses () indicate exclusive bounds and brackets \[] indicate inclusive bounds. Below, you will find an accompanying statement for each subsidy, in the order they appear in Figure 4.

 * Subsidies for transit trips:
    * Children 10 years old or younger receive $2 off of every transit trip
    * Seniors between 50 and 75 years of age, earning up to $20,000/year receive $2.30 off of every transit trip
* Subsidies for ridehail trips
    * Customers earning $40,000/year or less receive $3.20 off of every ridehail trip
    * Customers earning between $40,000/year and $50,000/year receive $2.20 off of every ridehail trip
    * Customers earning between $50,000/year and $60,000/year receive $1.10 off of every ridehail trip
 
You will be able to modify the characeristics of the subsidies in the input file `submission-inputs/ModeSubsidies.csv`, as shown below. 

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/Input_Subsidies.png "Figure 4: Input2 - Subsidies for transit and on-deamdn rideshare users")
***Figure 4: Input2 - Subsidies for transit and on-demand rideshare users***





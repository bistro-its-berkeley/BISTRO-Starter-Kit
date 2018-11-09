# Which inputs should I optimize?


To optimize the transportation system of Sioux Faux, you will need to test the performance of different policies, or combinations of inputs, by running an agent-based simulation with the BEAM simulator. This document provides the steps for installing BEAM, understanding the inputs to the simulation, where they are stored, and how to modify them.

 
## Overview of the repository

The repository details all the required inputs to run the simulation for Sioux Faux with BEAM. You will only have control over some of them (the inputs to optimize), but understanding all of them is important to run a successful simulation.

For more information on the folders discussed below, see the [How to run a simulation?](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/How_to_run_a_simulation%3F.md) page.

### The fixed inputs 

For each Sioux Faux scenario, the `fixed-data/siouxfalls` folder contains all fixed inputs necessary for one instance of the simulation. In the folder are descriptions of the configuration of the simulation parameters, the configuration of the transportation network, the agents’ desired activity plans and attributes, the households’ attributes and the vehicles characteristics.

*You will not change these parameters.*

### The Internal Pilot Test inputs to optimize

To help the Sioux Faux Department of Transportation (SFDOT) combat congestion and improve overall mobility in Sioux Faux, you will prepare a set of inputs to the simulation engine, which represent the following transportation system interventions: the composition of the vehicles in the bus fleet and the subsidies for transit and ridehail. These to-be-optimized inputs can be found in .csv format in the `submission-inputs` folder.

#### **Bus fleet composition**

The submission input file *VehicleFleetMix.csv* describes the status of the bus fleet (see Fig.1). Currently, SFBL (*agencyID* = 217) operates 12 bus lines in Sioux Faux. During the Hackathon, you can decide which type of bus (i.e. *vehicleTypeId*) will provide service for each route (*routeID*). Each route can utilize only **one type of bus**. 

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/Input_VehicleFleetMix.png "*Figure 2: Input1 - composition of the bus fleet")
***Figure 1: Input1 - Bus fleet composition***

SFDOT has four available bus types, each of them with different technical properties (`fixed-data/siouxfalls/vehicleTypes.csv`, see Fig.2) and costs (`fixed-data/siouxfalls/ vehicleCosts.csv`, see Fig.3). Currently, SFDOT owns the minimum number of bus types to provide service for each route, as specifed in the provided *VehicleFleetMix.csv*. Additionally, the number of buses required to service each route is equal to the number of trips: for each headway dispatched, a new bus is used. This does not reflect a realistic scenario combining bus routes into runs, but it still allows for comparisons to a BAU case.

During the Hackathon, for each route, you have to choose between keeping the currently operated bus types (see Figure 2 below) or purchasing new types of buses. ***For the Internal Pilot Test, the sale of an unused bus is not taken into account, only the purchase of buses.***

*Figure to change*
![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/BusTypes.png "Figure 2: Set of available bus types")
***Figure 2: Set of available bus types***



![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/BusCosts.png "Figure 3: Costs of available bus types")
***Figure 3: Costs of available bus types***

#### **Subsidies for transit and on-demand rideshare users**

In an effort to provide a high-quality alternative to private vehicles, you may define subsidies for qualifying agents using public transit or on-demand ridehail. Qualification for a subsidy can be based on the following socio-demographic categories: age and/or income (***and employment status***). The choice of utilized socio-demographic qualifier(s), range(s), mode(s), and subsidy amount(s) are all inputs that you can define. For the hackathon, there is no upper limit to the number of times an agent can claim a subsidy throughout the day.

The Figure 4 below shows an example input file with subsidies for specific socio-demographic groups. These are defined as in mathematical notation where parentheses () indicate exclusive bounds and brackets \[] indicate inclusive bounds. Below, you will find an accompanying statement for each subsidy, in the order they appear in Figure 4.

  * Subsidies for transit trips
    * Children 10 years old or younger receives $2 off of every transit trip
    * Seniors older than 50 and up through 75 years of age, earning up to $20,000/year receives $2.30 off of every transit trip
  * Subsidies for ridehail trips
    * Anyone earning $40,000/year or less receives $3.20 off of every ridehail trip
    * Anyone earning more than $40,000/year, but no more than $50,000/year receives $2.20 off of every ridehail trip
    * Anyone earning more than $50,000/year, but no more than $60,000/year receives $1.10 off of every ridehail trip
 
You will be able to modify the characeristics of the subsidies in the input file `submission-inputs/ModeSubsidies.csv` shown below. 

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/Input_Subsidies.png "Figure 4: Input2 - Subsidies for transit and on-deamdn rideshare users")
***Figure 4: Input2 - Subsidies for transit and on-demand rideshare users***




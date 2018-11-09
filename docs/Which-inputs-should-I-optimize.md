# Which inputs should I optimize?


To optimize the transportation system of Sioux Faux, you will need to write an algorithm that generates different inputs according to a specified format. This document provides information on the configurable inputs available to you.
 
## Overview of the repository

The repository details all the required inputs to run the BEAM simulation for the Sioux Faux scenario. You will only have control over some of them (the inputs to optimize), while others are fixed.

For more information on the folders discussed below, see the [How to run a simulation?](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/How_to_run_a_simulation.md) page.

### The Internal Pilot Test inputs to optimize

To help the Sioux Faux Department of Transportation (SFDOT) combat congestion and improve overall mobility in Sioux Faux, you will prepare a set of inputs to the simulation engine, which represent the following transportation system interventions: the bus fleet composition, the adjustments to the frequency of buses on routes and the distribution of subsidies for agents using ridehail and/or public transit. These to-be-optimized inputs can be found in .csv format in the `submission-inputs` folder.

#### **Bus fleet composition**

The submission input file *VehicleFleetMix.csv* describes the status of the bus fleet (see Fig.2). Currently, SFBL (*agencyID* = 217) operates 12 bus lines in Sioux Faux. During the Pilot Test, you can decide which type of bus (i.e. *vehicleTypeId*) will provide service for each route (*routeID*, see Fig.1 & 2). Each route can utilize only **one type of bus**. 


![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/sf_route_guide.png)\
***Figure 1: Sioux Faux route IDs guide***
<br/>
<br/>

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/Input_VehicleFleetMix.png "*Figure 2: Input1 - composition of the bus fleet")\
***Figure 2: Input1 - Bus fleet composition***

<br/>

SFDOT has four available bus types, each of them with different technical properties (`fixed-data/siouxfalls/vehicleTypes.csv`, see Fig.2) and cost characteristics (`fixed-data/siouxfalls/vehicleCosts.csv`, see Fig.3). Currently, SFDOT owns the minimum number of bus types to provide service for each route, as specifed in the file *submission-inputs/VehicleFleetMix.csv*. Additionally, the number of buses required to service each route is equal to the number of trips: after the a headway has expired, a new bus is used. This does not reflect a realistic scenario combining bus routes into runs, but, for now, it still allows for comparisons to a BAU case.

During the Pilot Study, for each route, you have the opportunity to purchase new types of buses possessing attributes that might improve the level of service for transit along a route (see Figure 2 below).

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Bus_types.png)\
***Figure 3: Set of available bus types***
<br/>
<br/>


![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/BusCosts.png "Figure 4: Costs of available bus types")\
***Figure 4: Costs of available bus types***
<br/>

#### **Subsidies for transit and on-demand rideshare users**

In an effort to provide a high-quality alternative to private vehicles, you may define subsidies for qualifying agents using public transit or on-demand ridehail. Qualification for a subsidy can be based on the following socio-demographic categories: age and/or income (*Note ot organizer: add employment status*). 

The choice of utilized socio-demographic qualifier(s), range(s), mode(s), and subsidy amount(s) are all inputs that you can define. They are described below. For the Internal Pilot Test, there is no upper limit to the number of times an agent can claim a subsidy throughout the day.
* The *modes* to subsidize can be chosen from the following list: 
  * `drive`: use of the personal car as the main transport mode for the trip
  * `walk`: walking as the main transport mode for the trip
  * `ride_hail`: use of on-demand rideshare as the main transport mode for the trip
  * `drive_transit`: use of the personal car as an access/egress mode to/from transit (bus)
  * `walk_transit`: walking as an access/egress mode to/from transit (bus)
  
* The *groups* are defined as in mathematical notation where parentheses () indicate exclusive bounds and brackets \[] indicate inclusive bounds. Below, you will find an accompanying statement for each subsidy in the order they appear in Figure 4.

* The *amounts* of the subsidies are decimal numbers that must be greater than 0.

The Figure 5 below shows an example input file with subsidies for specific socio-demographic groups. 

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Input_Subsidies.png)
***Figure 5: Input2 - Subsidies for transit and on-demand rideshare users***

The scenario is the following:

  * Subsidies for walking to access transit
    * Children 10 years old or younger receives $2 off of every transit trip
  * Subsidies for using on-deamdn rideshare to access transit
    * Seniors older than 50 and up through 75 years of age, earning up to $20,000/year receives $2.30 off of every transit trip
  * Subsidies for ridehail trips
    * Anyone earning $40,000/year or less receives $3.20 off of every ridehail trip
    * Anyone earning more than $40,000/year, but no more than $50,000/year receives $2.20 off of every ridehail trip
    * Anyone earning more than $50,000/year, but no more than $60,000/year receives $1.10 off of every ridehail trip
 
You will be able to modify the characeristics of the subsidies in the input file `submission-inputs/ModeSubsidies.csv`, as shown below. 





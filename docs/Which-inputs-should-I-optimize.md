# Input Specification


To optimize the transportation system of Sioux Faux, you will need to write an algorithm that generates different inputs as `csv`files. This document describes the nature of inputs available to contestants and provides *detailed schema for the files comprising a valid competition submission entry*.
 
## Introduction

As detailed in the [problem statement](docs/The_Sioux_Faux_case_pilot_study), to help the Sioux Faux Department of Transportation (SFDOT) combat congestion and improve overall mobility in Sioux Faux, you will prepare a set of inputs to the simulation engine, which represent the following transportation system interventions:

1. Bus fleet composition;
2. Adjustments to the frequency of buses on routes; and, 
3. Distribution of subsidies for agents using on-demand carsharing and/or public transit.

A submission entry is a set of input files (i.e., `csvs` named according to the input type), which have been collected into a single folder.

The following subsections provide a detailed description of what each input represents as well as technical details for the schema, data types, and constraints that specify the syntax of each input file. Files representing empty inputs can be found in the `submission-inputs` folder.


## Input Types

### **1. Bus Fleet Composition**

#### Description:



Currently, Sioux Faux Bus Lines (SFBL) operates a small fleet of buses on 12 routes in Sioux Faux. Orginally purchased as a group, each bus in the fleet possesses identical attributes of seating capacity, fuel consumption, operations and maintenance cost, etc. SFBL is considering optimizing bus type in order to better match the specific demand characteristics of each route. Four types of buses are available from its supplier, each of them with different technical properties (`fixed-data/siouxfalls/availableVehicleTypes.csv`, see Fig.2) and cost characteristics (`fixed-data/siouxfalls/vehicleCosts.csv`, see Fig.3). Currently, the number of buses required to service each route is equal to the number of trips: after the a headway has expired, a new bus is used. For instance, if the bus frequency is 10 minutes, a new bus is used every 10 minutes.  This does not reflect a realistic scenario combining bus routes into runs, but, for now, it still allows for comparisons to a BAU case.

![Route IDs](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/sf_route_guide.png)\
***Figure 1: Sioux Faux route IDs guide***
<br/>
<br/>




To provide guidance on vehicle procurement for SFBL, you can recommend purchase of new types of buses possessing attributes (seating capacity, fuel usage, operations and maintenance cost, etc.) that might improve the level of service for transit along a route while (ideally) reducing operational costs and greenhouse gas emissions (see Fig.2 below).


 You can decide to update the type of bus (i.e. `vehicleTypeId`) that will provide service for all trips on each route (`routeID`, see Fig.1 & 2). Each route can utilize only **one type of bus**, and, if **SID???**

For each bus that you purchase, the default bus on the route (i.e., buses designated by `vehicleTypeId` `BUS-DEFAULT`) is automatically sold for a price of <a href="https://www.codecogs.com/eqnedit.php?latex=\$10,000&space;&plus;&space;\$20,000&space;\times&space;\mathcal{N}(0,1)" target="_blank"><img src="https://latex.codecogs.com/png.latex?\$10,000&space;&plus;&space;\$20,000&space;\times&space;\mathcal{N}(0,1)" title="\$10,000 + \$20,000 \times \mathcal{N}(0,1)" /></a>

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Bus_types.png)\
***Figure 2: Set of available bus types***
<br/>
<br/>


![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/BusCosts.png "Figure 4: Costs of available bus types")\
***Figure 3: Costs of available bus types***
<br/>

#### Technical Details:
Your recommendation is to be submitted in a file named `VehicleFleetMix.csv` according to the format specified in Table 1.

| Column Name| Data Type | Description | Validation Criteria |
| :---:| :--- | :--- | :----|
| `agencyId`|`String` | Agency identifier | Must equal agency Id found under `agencyId` in `agencies.txt` of corresponding GTFS file for transit agency with `agency_name` designated by parent directory of `gtfs_data` in starter kit `/reference-data` directory. |
| `routeId` |`String` | The route that will have its vehicle type assignment modified | A route can only have its assignment modified once. The `routeId` name must exist in the `routes.txt` file corresponding to the GTFS data for the agency specified by this entry's `agencyId`|
| `vehicleTypeId`|`String` | The vehicle type identifier | Must be a member of the set of vehicle type Ids listed under `vehicleTypeId` in the `availableVehicleTypes.txt` file corresponding to the GTFS data for the agency specified by this entry's `agencyId`|

**Table 1: Vehicle fleet mix input schema and constraint definitions**


#### Example:

![Bus fleet](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/Input_VehicleFleetMix.png "*Figure 2: Input1 - composition of the bus fleet")\
**Figure 4: Example of Vehicle Fleet Mix Input.**

Only three routes are assigned a different bus; all other routes operate with the standard bus type.

<br/>
<br/>

### **2. Subsidies for transit and on-demand rideshare users**

#### Description

In an effort to encourage the use of sustainable transportation alternatives to private vehicles, SFDOT has asked you to allocate subsidies to incentivize citizens to use public transit and/or on-demand ridesharing.

The travel *modes* and connectivity options to subsidize can be chosen from the following:
  * use of on-demand rideshare as the main transport mode for the trip
  * use of the personal car as an access/egress mode to/from transit (bus)
  * walking as an access/egress mode to/from transit (bus)

Qualification for a subsidy can be based on age and/or income. Subsidies for one mode do not disqualify subsidizing travel for another mode. Additionally, the price of each leg in a multimodal trip is will be adjusted by the amount of subsidy allocated to the qualifying agent undertaking the trip. That is, for each trip the best route for each multimodal type will include subsidies in the overall cost of the trip. This generalized cost will then factor into agent decision-making.

#### Technical Details:
Your recommendation is to be submitted in a file named `ModeSubsidies.csv` according to the format specified in Table 2. See Figure 5 for an example.

| Column Name | Data Type |Description | Validation Criteria |
| :---: |:--- | :--- | :----|
| `mode` | [`Subsidizable`](#subsidizable)| Mode to subsidize. | None |
| `age` | [`Range`](#range) | The range of ages of agents that qualify for this subsidy. | Must be greater than 0 and less than 120 (the maximum age of any resident in Sioux Faux)|
| `income` | [`Range`](#range) | The range of individual incomes of agents that qualify for this subsidy | Must be greater than 0. |
| `amount` | `Float` | The amount (in $US) to subsidize this entry's `mode`| Must be greater than 0.|

**Table 2: Vehicle fleet mix input schema and constraint definitions**

#### Example:

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Input_Subsidies.png)
***Figure 5: Example of Mode Subsidy Input***

Figure 5 depicts an example input file describing the following situation:

 *Subsidies for walking to access transit*:
 * Children 10 years old or younger receive $2 off of every transit trip

 *Subsidies for using rideshare to access transit*:
 * Seniors older than 50 and up through 75 years of age, earning up to $20,000/year receive $2.30 off of every transit trip

 *Subsidies for rideshare trips*:
 * Anyone earning $40,000/year or less receives $3.20 off of every rideshare trip
 * Anyone earning more than $40,000/year, but no more than $50,000/year receives $2.20 off of every rideshare trip
 * Anyone earning more than $50,000/year, but no more than $60,000/year receives $1.10 off of every rideshare trip


### **3. Adjustments to the Frequency of Buses on a Route**

#### Description

An essential aspect of transit system operations is capacity optimization. Route capacity is the number of passengers that can be moved past a fixed point in a given unit of time. In addition to allocating buses with larger or smaller total occupancies, SFBL wants to alter the frequency of buses on a given route. The `FrequencyAdjustment` input works in concert with the `VehicleFleetMix` input so that the capacity of the route is more likely to meet demand as it changes throughout a typical workday.

#### Technical Details

The format for this  input is identical to the `frequencies.txt` component of the [GTFS specification](https://developers.google.com/transit/gtfs/reference/#frequenciestxt). The GTFS data of Sioux Faux are stored in the [reference-data](https://github.com/vgolfier/Uber-Prize-Starter-Kit/tree/master/reference-data/sioux_faux/sioux_faux_bus_lines) folder.

Before explaining how the input works, a few terms must be defined:

* A **route** is made of a group of *trips* that are displayed to riders as a single service. Each bus route can be identified with a `route_id`. To understand the geospatial embedding of each Route corresponding to a `route_id`, please refer to Figure 1, above.   
* A **trip** is a sequence of two or more *stops* that occurs at specific time and is identified by a `trip_id`. The trips corresponding to each route are described in the `trips.txt` [file](https://developers.google.com/transit/gtfs/reference/?csw=1#tripstxt). For Sioux Faux, the existing SFBL trips are described in the [trip.txt](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/gtfs_data/trips.txt) file of the [gtfs-data](https://github.com/vgolfier/Uber-Prize-Starter-Kit/tree/master/reference-data/sioux_faux/sioux_faux_bus_lines).
* Each trip get assigned a **service_id**, which uniquely identifies a set of dates when service is available. SFBL has two operational timeframes (see [`calendar.txt`](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/gtfs_data/calendar.txt) file:
  * service on week days (Mon-Fri): `service_id` = `c_676_b_219_d_31`
  * service on Saturdays only: `service_id` = `c_676_b_219_d_31`

While we term the behavior of this input as frequency adjustment, in fact, it modifies the SFBL bus headways on a particular route. The adjustment wipes out all non-frequency trips from the route and converts them to frequency trips according to the given `headway_secs` defined between `start_time` and `end_time`. Here, we require you to provide the `trip_id` in order to derive the stop pattern and travel times. Please set `exact_times` to 0. This field is not currently being used, but must be included for validation purposes.

  Per the description of the behavior controlled by the Vehicle Fleet Mix input, adding or removing the number of trips on a route will require more or less buses to be assigned to a route. Ensuring input correctness requires the frequency adjustment to be executed prior to computation of the vehicle purchase costs. Thus, policies that include this input implicitly require vehicle purchases or sales--even when no new inputs are specified in the `VehicleFleetMix.csv` file. Therefore, contestants must take care to coordinate modifications to this input with vehicle prices and ensure that they are not inadvertently over-spending exceeding their budgets.

| Column Name | Data Type |Description | Validation Criteria |
| :---: |:--- | :--- | :----|
| `tripId` | `String` | The trip corresponding to the route for which frequencies will be adjusted. | Must reference a `tripId` in the `trips.txt` (and implicitly a `routeId` in the `routes.txt` file) corresponding to the GTFS data for the agency specified by this entry's `agencyId` |
| `startTime` | `Integer`  | The `start_time` field specifies the time (in seconds past midnight) at which the first vehicle departs from the first stop of the trip with the specified frequency. | Must be greater than 0 and less 86400 (the number of seconds in a day).|
| `endTime` | `Integer`  | The end_time field indicates the time at which service changes to a different frequency (or ceases) at the first stop in the trip. | Must be greater than 0 and less 86400 (the number of seconds in a day). |
| `headway_secs` | `Integer`| 	The headway_secs field indicates the time between departures from the same stop (headway) for this trip type, during the time interval specified by start_time and end_time. The headway value must be entered in seconds. | Must be greater than the number of headway seconds. 	Periods in which headways are defined (the rows in frequencies.txt) shouldn't overlap for the same trip, since it's hard to determine what should be inferred from two overlapping headways. However, a headway period may begin at the exact same time that another one ends. |
| `exact_time` | `Integer`|Determines if frequency-based trips should be exactly scheduled based on the specified headway information. |Must be entered as 1 for the purposes of this round of the contest. See the [GTFS specification](https://developers.google.com/transit/gtfs/reference/#frequenciestxt) for further information about what this field represents. |

<!--TODO: Suppress exact time?-->

#### Example:
<!--TODO: Enter here... -->
![Bus Fequency Input](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Bus_frequencies_inputs.png)
***Figure 6: Bus Frequency Input***

### Public Transit Fare Adjustment

#### Description

#### Technical Details


| Column Name | Description | Validation Criteria |
| :---: | :--- | :----|
| `agencyId`| `String` | Agency identifier | Must equal agency Id found under `agencyId` in `agencies.txt` of corresponding GTFS file for transit agency with `agency_name` designated by parent directory of `gtfs_data` in starter kit `/reference-data` directory. |
| `routeId` | `String` | The route that will have its fare specified. | A route can only have its fare set once. The `routeId` name must exist in the `routes.txt` file corresponding to the GTFS data for the agency specified by this entry's `agencyId`|
| `age` | [`Range`](#range) | The range of ages of agents that this fare pertains to. | Must be greater than 0 and less than 120 (the maximum age of any resident in Sioux Faux)|
| `amount` | `Float` | The amount (in $US) to charge an agent in the corresponding fare group. | Must be greater than 0.|


#### Example

### Time-interval-based Road Pricing

#### Description

#### Technical Details

#### Example

---

## Specialized Data Types:

The following are data types that are specializations of simplified data types that are constrained according to a specific syntax

<span id="subsidizable">`Subsidizable`</span>: `Enumeration`; must be a member of the set: {`"ride_hail"`,`"drive_transit"`, `"walk_transit"`

<span id="range">`Range`</span>: `String`; Ranges are defined according to typical mathematical notation conventions whereby parentheses "(" and ")" indicate exclusive bounds and brackets "\[" "]" indicate inclusive bounds. For example, "[0,100)" is interpreted to mean, "0 (inclusive) to 100 (exclusive)".


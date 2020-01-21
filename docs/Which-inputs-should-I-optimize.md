# Input Specification

To optimize the transportation system of a BISTRO Scenario, you will need to write an algorithm that generates different inputs as `csv`files. This document describes the transportation system optimization problem in the context of a benchmark scenario including example inputs and a detailed schema for the files comprising a valid BISTRO policy submission.
 
## Introduction

The [Sioux Faux Benchmark Scenario](./The_Sioux_Faux_scenario.md) is designed to enable BISTRO users to familiarize themselves with the transportation system optimization problem through an example policy scenario. The scenario includes a set of example inputs to the simulation engine, which represent the following transportation system interventions:

1. Public transit fleet composition;
2. Distribution of incentives for agents using on-demand ridehailing and/or public transit;
3. Adjustments to the frequency of public transit service on particular routes; and, 
4. Public transit fares.

A submission is a set of input files (i.e., `csv`s named according to the input type), which have been collected into a single folder.

The following subsections provide a detailed description of what each input represents as well as technical details for the schema, data types, and constraints that specify the syntax of each input file. Files representing empty inputs can be found in the [`submission-inputs`](/submission-inputs/) folder.

## Input Types

### **1. Public Transit Fleet Composition**

#### 1.1. Description:

In the Sioux Faux Benchmark Scenario, Sioux Faux Bus Lines (SFBL) operates a small fleet of buses on 12 routes in Sioux Faux. Orginally purchased as a group, each bus in the fleet possesses identical attributes of seating capacity, fuel consumption, operations and maintenance cost, etc. SFBL is considering optimizing bus type in order to better match the specific demand characteristics of each route. Four types of buses (including the current one used by SFBL, called `BUS-DEFAULT`) are available from its supplier, each of them with different technical properties ([`availableVehicleTypes.csv`](/../../blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/availableVehicleTypes.csv), see Figure 2) and cost characteristics[`vehicleCosts.csv`](/../../blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/vehicleCosts.csv), see Figure 3). Currently, the number of buses required to service each route is equal to the number of trips: after the headway has expired, a new bus is used. For instance, if the bus frequency on a specific route is 10 minutes, a new bus is used every 10 minutes during the service time on this route. When one bus finishes its (unique) tour, it disappears from the simulation. This does not reflect a realistic scenario combining bus routes into runs, but, for now, it still allows for comparisons to a BAU case.


![Route IDs](/Images/sf_route_guide.png) <br/>
***Figure 1: Sioux Faux route IDs guide***
<br/>
<br/>


To provide guidance on vehicle procurement for SFBL, you can recommend purchase of new types of buses possessing attributes (seating capacity, fuel usage, operations and maintenance cost, etc.) that might improve the level of service for transit along a route while (ideally) reducing operational costs and particulate matter (PM2.5) emissions (see Figure 2 below).


 You can decide to update the type of bus (i.e. `vehicleTypeId`) that will provide service for all trips on each route (`routeID`, see Figures 1 & 2). Each route can utilize only **one type of bus**.



![Alt text](/Images/Bus_types.png)\
***Figure 2: Set of available bus types***
<br/>
<br/>


![Alt text](/Images/BusCosts.png)\
***Figure 3: Costs of available bus types***
<br/>

#### 1.2. Technical Details:
Your recommendation is to be submitted in a file named `VehicleFleetMix.csv` according to the format specified in Table 1.

| Column Name| Data Type | Description | Validation Criteria |
| :---:| :--- | :--- | :----|
| `agencyId`|`String` | Agency identifier | Must equal agency Id found under `agencyId` in [`agencies.txt`](/../../blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/gtfs_data/agency.txt) of corresponding GTFS file for transit agency with `agency_name` designated by parent directory of `gtfs_data` in starter kit `/reference-data` directory. Note that for Sioux Faux, SFBL is the only agency operating in the city (`agencId`="217"). Therefore, any entry in the .csv file will have "217" under `agencyId`.|
| `routeId` |`String` | The route that will have its vehicle type assignment modified | A route can only have its assignment modified once. The `routeId` name must exist in the [`routes.txt`](/../../blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/gtfs_data/routes.txt) file corresponding to the GTFS data for the agency specified by this entry's `agencyId`.|
| `vehicleTypeId`|`String` | The vehicle type identifier | Must be a member of the set of vehicle type Ids listed under `vehicleTypeId` in the [`availableVehicleTypes.csv`](/../../blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/availableVehicleTypes.csv)file. |

***Table 1: Vehicle fleet mix input schema and constraint definitions***


#### 1.3. Example:
Figure 4 below depicts an example of Public Transit Vehicle Fleet Mix input file. Only three routes (`1342`, `1350` and `1351`) out of twelve are assigned a new bus type (respectively `BUS-STD-HD`, `BUS-SMALL-HD`, `BUS-STD-ART`); all other routes operate with the default bus type (`BUS-DEFAULT`).

![Bus fleet](/Images/Input_VehicleFleetMix.png)\
***Figure 4: Example of Vehicle Fleet Mix Input.***



### **2. Transit and on-demand rides incentives**

#### 2.1. Description

In an effort to encourage the use of sustainable transportation alternatives to private vehicles, SFBL is considering providing incentives to promote public transit in Sioux Faux. SFBL is exploring options for citizens lacking access to quality transit or means to pay fares, including defraying the cost of certain qualified transit trips and/or on-demand rides. 

You may choose to defray the cost of on-demand rides and/or transit based on either age group, income group, or both.
To do so, the *range of qualifying socio-demographic characteristics* and *value of the incentive provided to each group* must be defined for passengers using each of the following modes of transportation to complete a trip: 
  * "OnDemand_ride": use of on-demand ride(s) as the main transport mode for the trip
  * "drive_transit": use of the personal car as an access/egress mode to/from transit (bus)
  * "walk_transit": walking as an access/egress mode to/from transit (bus)

Qualification for an incentive can be based on *age* and/or *income*. You can find the distributions of Sioux Faux's population over age and income on the [The_Sioux_Faux_scenario](./The_Sioux_Faux_scenario.md) page.

Incentives for one mode do not disqualify providing incentives for another mode. Additionally, the price of each leg in a multimodal trip will be adjusted by the amount of incentive allocated to the qualifying agent undertaking the trip. That is, for each trip (i.e. travel from the agent's origin to the goal activity), the best route for each multimodal type will include incentives in the overall cost of the trip. This generalized cost will then factor into agent decision-making.

#### 2.2. Technical Details:
Your recommendation is to be submitted in a file named `ModeIncentives.csv` according to the format specified in Table 2. See Figure 5 for an example.

| Column Name | Data Type |Description | Validation Criteria |
| :---: |:--- | :--- | :----|
| `mode` | [`Incentive eligible`](#incentive-eligible)| Mode to provide incentive to. | None. |
| `age` | [`Range`](#range) | The range of ages of agents that qualify for this incentive. | Must be greater than 0 and less than 120 (the maximum age of any resident in Sioux Faux). Mode incentives may not isolate a single age; incentives must be defined in bins no smaller than five years in range.|
| `income` | [`Range`](#range) | The range of individual incomes (in $US/person) of agents that qualify for this incentive. | Must be equal or greater than 0 and equal or smaller than 150000. Mode incentives must be defined in bins no smaller than $5,000 in range.|
| `amount` | `Float` | The amount (in $US) of the incentive to provide to this entry's `mode`.| Must be greater than 0 and equal or smaller than 50.|

***Table 2: Vehicle fleet mix input schema and constraint definitions***

#### 2.3. Example:

![Alt text](/Images/Input_ModeIncentives.png)
***Figure 5: Example of Mode Incentive Input***

Figure 5 depicts an example input file describing the following situation:

 *Incentive for walking to access transit*:
 * Children 10 years old or younger receive $2.00 off of every transit trip

 *Incentive for driving to access transit*:
 * Adults older than 50 and up through 75 years of age, earning up to $20,000/year receive $2.30 off of every transit trip

 *Incentives for on-demand rides*:
 * Anyone earning $40,000/year or less receives $3.20 off of every on-demand ride
 * Anyone earning more than $40,000/year, but no more than $50,000/year receives $2.20 off of every on-demand ride
 * Anyone earning more than $50,000/year, but no more than $60,000/year receives $1.10 off of every on-demand ride


### **3. Adjustments to the Frequency of Buses on a Route**

#### 3.1. Description

An essential aspect of transit system operations is capacity optimization. Route capacity is the number of passengers that can be moved past a fixed point in a given unit of time. In addition to allocating buses with larger or smaller total occupancies, SFBL wants to alter the frequency of buses on a given route. The `FrequencyAdjustment` input works in concert with the `VehicleFleetMix` input so that the capacity of the route is more likely to meet demand as it changes throughout a typical workday.

Currently, Sioux Faux buses follow a *non-frequency schedule* based on their arrival and departure times to and from each stop of their route. These arrival and departure times are listed in the [`stop_times.txt`](/../../blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/gtfs_data/stop_times.txt) file of Sioux Faux's GTFS data.
Your role here is to decide if some routes (identified by their `route_id`s, see Figure 6 below) should follow a *frequency schedule* instead of a non frequency one. While we term the behavior of this input as frequency adjustment, in fact, it modifies the SFBL bus headways on a particular route. The adjustment wipes out the *whole* non-frequency schedule from the route and converts it to a frequency schedule according to the given `headway_secs` and within the specified *service period* (defined between `start_time` and `end_time`). You can find a definition of these parameters in Table 3 below. Note that it is assumed that buses operate only on *week days* (i.e. from Monday to Friday).

![Alt text](/Images/route_txt_truncated.png)\
***Figure 6: `Route_id`s as defined in the routes.txt file (truncated version displayed)***


#### 3.2. Technical Details

The format for this input is described in the Table 3 below. 


| Column Name | Data Type |Description | Validation Criteria |
| :---: |:--- | :--- | :----|
| `route_id` | `String` | The route for which frequencies will be adjusted with a new service period (defined between `start_time` and `end_time`) / headway combination . | Must reference a `route_id` in the [`routes.txt`](/../../blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/gtfs_data/routes.txt) file corresponding to the GTFS data for the agency specified by this entry's `agencyId` (see Figure 6). |
| `start_time` | `Integer`  | The `start_time` field specifies the starting time (in seconds) of the service period operating with the new headway. In other words, it is the time (in seconds past midnight) at which the first vehicle departs from the first stop of the trip with the specified frequency. | Must be greater than 0 and less than 86400 (the number of seconds in a day).|
| `end_time` | `Integer`  | The `end_time` field indicates the end time (in seconds) of the service period operating with the new headway. In other words, it is the time at which service changes to a different frequency (or ceases) at the first stop in the trip. | Must be greater than 0 and less than 86400 (the number of seconds in a day). |
| `headway_secs` | `Integer`| 	The `headway_secs` field indicates the time (in seconds) between departures from the same stop (headway) for this trip type, during the time interval specified by `start_time` and `end_time`. The headway value must be entered in seconds. | Must be greater than 180sec (3min) and less than 7200sec (2h). <br> Periods in which headways are defined (the rows in frequencies.txt) shouldn't overlap for the same route, since it's hard to determine what should be inferred from two overlapping headways. However, a headway period may begin at the exact same time that another one ends. |
| `exact_times` | `Integer`|Determines if frequency-based trips should be exactly scheduled based on the specified headway information. |Must be entered as 1 for the purposes of this round of the contest. See the <a href="https://developers.google.com/transit/gtfs/reference/#frequenciestxt">GTFS specification</a> for further information about what this field represents. |

***Table 3: Frequency Adjustments input schema and constraint definitions***

Please, note some important business rules ane remarks: 
* There can be **no more than five** distinct bus service periods per route (this mimics the typical delineation: am peak, midday, pm peak, evening, late night/early morning). Technically, it means that there cannot be more than 5 rows with the same `route_id` in the FrequencyAdjustment.csv input file.
* Giving that defining a new frequency input for a route wipes the whole initial non-frequency schedule, it means that for each modified route, **no bus is operating during the time periods outside of the newly defined service periods**. It is up to you to decide if the new service periods should connect or not to provide a continuous bus service.

<!--TODO: Suppress exact time?-->

#### 3.3. Example:

Figure 7 below depicts an example input file.

![Alt text](/Images/Input_frequency_adjustment.png)
***Figure 7: Example of Frequency Adjustment Input***

In this case, two routes will see their bus frequency adjusted: route 1340 and route 1341. 
*  The bus schedule on route 1340 is changed between 6am (21600 sec) and 10pm (79200 sec) to a 15 minute frequency-schedule (900sec). Outside of this time-window, the bus schedule on the route follow the non-frequency schedule defined by the gtfs-data of the agency.
* The bus frequency on route 1341 is changed between 6am (21600 sec) and 10am (36000 sec) and between 5pm (61200 sec) and 8pm (72000 sec) to a 5 minute frequency-schedule (900 sec).
* Buses operating on all other routes follow the original non-frequency schedule.


### 4. Public Transit Fare Adjustment

#### 4.1. Description
SFBL would like to use this simulation experiment to explore the effect of changing **bus fares**, i.e. the cost to a passenger of traveling by bus. Currently, the Sioux Faux bus fare policy works as follow: 
* Children 5 yrs. and under: FREE
* Children 6 to 10 yrs. : $0.75
* Children 11 to 18 yrs and Adults 65 yrs. and under: $1.50
* Persons over 65 yrs: FREE

Perhaps a lower fare for young adults (ages 12-18) would significantly increase ridership among this population. Alternatively, perhaps a higher fare for middle-aged adults (40-55) would be well-tolerated, while boosting fare-box revenue."

For each new bus fare that you want to introduce, you need to specify the amount of the new fare (`amount`), to which bus route it will apply (`routeId`), which bus company operated this bus route (`agendyId`) and to which age group (`age`) this fare will apply. 

#### 4.2. Technical Details


| Column Name | Data Type | Description | Validation Criteria |
| :---: |:--- | :--- | :----|
| `agencyId`| `String` | Agency identifier | Must equal agency Id found under `agency_id` in [`agencies.txt`](/../../blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/gtfs_data/agency.txt) of corresponding GTFS file for transit agency with `agency_name` designated by parent directory of `gtfs_data` in starter kit `/reference-data` directory. Note that for Sioux Faux, SFBL is the only agency operating in the city (`agencyId`="217"). Therefore, any entry in the .csv file will have "217" under `agencyId`.|
| `routeId` | `String` | The route that will have its fare specified. | A route can only have its fare set once. The `routeId` name must exist in the [`routes.txt`](/../../blob/master/reference-data/sioux_faux/sioux_faux_bus_lines/gtfs_data/routes.txt) file corresponding to the GTFS data for the agency specified by this entry's `agencyId`|
| `age` | [`Range`](#range) | The range of ages of agents that this fare pertains to. | Must be greater than 0 and less than 120 (the maximum age of any resident in Sioux Faux). Bus fares may not isolate a single age; fares must be defined in bins no smaller than five years in range.|
| `amount` | `Float` | The amount (in $US) to charge an agent in the corresponding fare group. | Must be greater than 0 and equal or smaller than 10.|

***Table 4: Pt Fares input schema and constraint definitions***

#### 4.3. Example
Figure 8 depicts an example input file for Public Transit Fare Adjustment.

![Alt text](/Images/Input_MassTransitFares.png)
***Figure 8: Example of Public Transit Fare input***

The file describes the following fare policy:
* Passengers older than 5 and up through 25 years pay a reduced fare of $0.50
* Passengers 65 years old and older pay a reduced fare of $0.50
* All other passengers pay the fare defined in the original Sioux Faux policy (see 4.1)

---

## Specialized Data Types:

The following are data types that are specializations of simplified data types that are constrained according to a specific syntax

<span id="incentive-eligible">`Incentive eligible`</span>: `Enumeration`; must be a member of the set: {`"OnDemand_ride"`,`"drive_transit"`, `"walk_transit"`}

<span id="range">`Range`</span>: `String`; Ranges are defined according to typical mathematical notation conventions whereby parentheses "(" and ")" indicate exclusive bounds and brackets "\[" "]" indicate inclusive bounds. For example, `"[0,100)"` is interpreted to mean, "0 (inclusive) to 100 (exclusive)".

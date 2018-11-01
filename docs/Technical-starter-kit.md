
To be able to optimize the transportation system of Sious Faux, you will need to test some different input-policies  by running an agent-based simulation with the BEAM simulator. This Technical Starter Kit gives you the steps for installing BEAM and understanding where the inputs and outputs of the simulation are stored.

# Installing BEAM

Clone the following GitHub repository in your GitHub Desktop:
https://github.com/sfwatergit/BeamCompetitions

After you unzip the archive, you will see a directory that looks like this when partially expanded:

![Competition Repository](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/CompetitionRepository.png "Competition Repository")
 
# Overview of the repository

The repository contains all required inputs to run the simulation for Sioux Faux with BEAM. You will only have control on a few of them but let’s quickly describe all of them. 

## The fixed inputs 

The folder *fixed-data/siouxfalls* encloses, for each Sioux Faux scenario, all fixed inputs necessary for one instance of the simulation. They describe the configuration of the simulation parameters, the configuration of the transportation network, the agents’ desired activity plans and attributes, the households’ attributes and the vehicles characteristics.

You will not have to change these parameters.

## The inputs to optimize

To help the Sioux Faux Department of Transportation (SFDOT) combat congestion and improve overall mobility in Sioux Faux, you will prepare a set of inputs to the simulation engine, which represent the following transportation system interventions: the bus fleet composition and subsidies for transit and on-demand rideshare. These to-be-optimized inputs can be found in a csv format in the *submission-inputs* folder.

* **Bus fleet composition**

The submission input file *VehicleFleetMix.csv* describes the status of the bus fleet (see Fig.1). Currently, SFBL (*agencyID* = 217) is operating twelve bus lines in Sioux Faux. For four of them, you can decide which type of bus (i.e. *vehicleTypeId*) should be assigned to service each of these four bus routes (i.e. *routeID*). There can be only **one type of bus per route**. 

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/Input_VehicleFleetMix.png "*Figure 1: Input1 - composition of the bus fleet")

You have a set of four available buses to pick from, each of them having different technical properties (*fixed-data/siouxfalls/vehicleTypes.csv*, see Fig.2) and costs (*fixed-data/siouxfalls/ vehicleCosts.csv*, see Fig.3). Based on these characteristics, you have to choose between keeping the currently operated bus types (see Figure 1 above) or purchasinf new types of buses.

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/BusTypes.png "Figure 2: Set of available bus types")


![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/BusCosts.png "Figure 3: Costs of available bus types")

Note:
Currently, the number of buses transiting on each route is trip-based. For each new trip made along the route, a new bus is used. The simulation do not reflect the cycles made by buses in reality.

* **Subsidies for transit and on-demand rideshare users**

In an effort to promote the use of and access to public transportation, you may define subsidies for the users walking or using on-demand rideshare as a last-mile solution to access transit. Those subsidies will be based on the following age and/or income ranges:

 * Subsidies for taking transit 
  * Children under 10 years old (excluded)
  * Seniors from 50 years old (and younger than 75 years old) and earning less than 20’000$/year
 * Subsidies for using on-demand rideshare as a last-mile-solution to access transit 
  * People earning less than 40’000$/year
  * People earning between 40’000$/year and 50’000$/year (excluded)
  * People earning between 50’000$/year and 60’000$/year (excluded)
 
You will be able to change the subsidies amounts [$/person] in the input file *submission-inputs/ModeSubsidies.csv* shown below. 

Then give the syntax for a range. These are defined as in mathematical notation where ( and ) indicate inclusive and [ and ] indicate exclusive upper and lower bounds, respectively.

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/Input_Subsidies.png "Figure 4: Input2 - Subsidies for transit and on-deamdn rideshare users")


Format, where to be placed, what they signify (cf.pb statement)

For more detailed general inputs documentation in BEAM, see Model Inputs.



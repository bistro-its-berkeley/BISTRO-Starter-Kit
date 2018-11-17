# A Brief Introduction to the Urban Transportation System Optimization Framework

This document describes the goal and main components of the Uber Prize challenge, that is, the daily travel simulation environment, its inputs, and its outputs.

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Simulation_Framework.png)

## Goal of Round I:

The overall goal of the preliminary round of the Uber Prize is to develop an algorithms that finds the *policy* that will best improve several indicators of the quality of the transportation system in Sioux Faux**. Here, we use *policy* to refer to a combination of inputs (as `.csv` files) representing changes in mass transit vehicle fleet composition, bus frequencies, and subsidies that could reduce the cost of multimodal transport for commuters.

Policies are tested by simulating the daily travels of a synthetic population of individuals called `Agents`, each with their own socio-demographic characteristics. The *agent-based simulation* is hosted by the BEAM simulator. During the simulated day, each *Agent* has a defined `Plan`, i.e. a sequence of activities with specific locations ordered by activity end times. Throughout the day, the `Agents` will make decisions on which transportation modes they will use, their departure times, and the routes they take to travel between activities. 

By simulating the daily travel behavior of the whole population, the quality of the city's transportation system can be evaluated, based upon scoring criteria, detailed [here](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md).

## A Brief Overview of the Simulation Engine 

The simulation software used for the Uber Prize challenge is an agent-based travel demand simulation framework named BEAM, which stands for Behavior, Energy, Autonomy, and Mobility. It is built on top of a separate agent-based travel demand simulation library called MATSim, and , in particular, leverages its co-evolutionary dynamic traffic assignment mechanism (described below). 

This section presents a brief overview of the most important concepts underlying the operation of these two models. For those who have not yet had exposure to transportation demand models, the amount of new information contained below may seem daunting. Do not despair! It is not necessary to fully understand the subsequent material straight away in order to begin executing the simulation; however, we do introduce important many important terms and concepts in the following section that will be used elsewhere in the documentation. As you begin to execute the simulation and view its outputs, return to this page, and you will likely find it to be much more comprehensible.

### The BEAM Execution Lifecycle

A BEAM simulation computes the interaction of *supply* and *demand* in a virtual urban transportation system. Supply is represented by the physical transportation infrastructure such as roads and subway lines as well as vehicles (personal, mass transit, and shared). Supply data is usually obtained from sources such as [Open Street Map](http://www.openstreetmap.org), General Transit Feed Specification ([GTFS](https://developers.google.com/transit/gtfs/)), and/or general purpose urban data aggregators such as [Coord](https://coord.co/). Demand, on the other hand, consists of the planned *activities* of *synthetic commuters* (agents) populating the virtual urban space. 
This notion of demand may seem counter-intuitive, as it is *indirect*, that is, activities are certainly not the commodities typically associated with transportation services. However, per modern transportation science, travel is theorized to be a by-product of our desire to participate in activities that are distributed in time and space. Accordingly, the model of demand implemented in BEAM and MATSim is an *activity-based model*, which operates on the principle that activities *induce demand* for travel.

 The ability to imbue agents with heterogeneous preferences and characteristics is an important feature of agent-based models. Data for demand models, which takes the form of a population of synthetic agents together with their associated *activity patterns*, may be derived from census products, travel surveys, as well as, increasingly, mobility patterns inferred from statistical regularities in anonymized individual cellular records.  BEAM can model the daily travel patterns of millions of virtual agents, which permits analysts to understand the implications of policy alternatives on regional mobility patterns at high spatiotemporal resolution.
 

Like MATSim, BEAM simulates the simultaneous execution of these daily activity patterns (sometimes referred to here and in practice as *plans*) on a virtual road network represented as a geospatially-embedded graph. Links in the network are modeled using queues that retain an agent for a period of time dictated by real-world road capacity, free-flow speed, and, importantly, whether there is space on the the next link of a planned route to accept the agent. If the queue is full and can no longer admit additional agents during a time-step, then congestion events begin to propagate through the system. 

Since agents prefer being at activities to waiting in traffic, an agent's *utility* is reduced during congested travel (that is, when travelling lower than the posted maximum free speed). In the language of reinforcement learning, this econometric notion of utility represents a reward (cost) when the agent is participating in an activity (travelling). Various additional contributions to individual utility accrue throughout the day such as tolls (negative) and time spent with friends (positive). At day's end, the iteration is complete, and the just-executed plan is assigned a score corresponding to an individual's net utility for that iteration. 

Upon completing the mobility simulation, a proportion of agents have the opportunity to select a strategy to re-plan consequential aspects of their daily itinerary. For example, they may change their departure time, mode of travel, or choose to route around expected congestion. These plans are selected to be executed in the subsequent iteration. Agents that do not re-plan choose an existing, executed plan from a memory that holds a configurable number of plans. Plans with higher scores are more likely to be chosen. In addition, plans with low scores are forgotten once the number of plans in memory is in excess of capacity.

The process of plan execution, scoring, and replanning continues until the average scores of agent plans cease to improve. Once this happens, we may say that the system is in *equilibrium* between supply and demand and the simulation concludes. Based on the travel patterns realized during the iteration when the system is determined to be in an equilibrium state, the simulation concludes and the software enters a post-processing phase, producing summary outputs analyzing the performance of individual agents as well as the overall system. Ultimately, it is from these outputs that the submission score is computed.  


## The Simulation Inputs

 In this competition, the supply and demand data together with calibrated parameters governing a variety of physical and behavioral parameters are taken to be fixed inputs to the simulation. Contestants instead focus on perturbing a more limited set of inputs that represent transportation policy interventions.

The simulation inputs for BEAM are comprised of specifications regarding public transit operations, ridehail partnerships and subsidies, and public transit finances.

For the **pilot test**, the input parameters specify:
* **purchases and sales of buses serving a route**.
* **adjustments to the frequency of buses on routes**.
* **distribution of subsidies** for agents using ridehail and/or public transit.

You will find more information on the Sioux Faux simulation inputs, where they are stored, and how to control them on the [inputs to optimize](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Which-inputs-should-I-optimize.md) page.


## The Simulation Outputs: Evaluating System and Agent Performance

The quality of the new policy-based transportation system is evaluated based upon a comparison against the business as usual (BAU) scenario. The BAU scenario represents the baseline or "current" status-quo of the Sioux Faux transportation system. In other words, this is a "do-nothing" approach. This comparison answers the following question: **How will the new policy improve over the current state of the transportation system**?

The performance of this new policy-based transportation system is measured by a **scoring function**, which computes the weighted sum of three groups of outputs:

* How much *congestion* did the agents experience during the day? 
* What *level of service* did the transportation system offer to agents? 
* What were the *budgetary* impacts?

Positive total scores indicate that, under the evaluated policy portfolio, the system is performing better compared to the BAU scenario<sup id="a1">[1](#f1)</sup>.


You will find more information on the outputs of the simulation, how to interpret them, and the scoring function on the [outputs and the scoring function](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md) page.

You can find more documentation on BEAM or MATSim [here](https://beam.readthedocs.io/en/latest/about.html#overview). 

<sup id="f1">1</sup> Pilot testers, please note the following: We understand that the simulator is inherently stochastic and that score outputs will vary to some extent on the **same** set of input variables. We have not yet officially established what is a statistically difference in scores. There are quite a few subtleties here, and we would love to get your feedback on what seems appropriate.[↩](#a1)

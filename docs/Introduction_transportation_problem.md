# A Brief Introduction to the Urban Transportation System Optimization Framework

This document describes the goal and main components of the Uber Prize challenge, that is, the daily travel simulation environment, its inputs, and its outputs.

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Simulation_Framework.png)

## Goal of Round I:

The overall goal of the preliminary round of the Uber Prize is to develop an algorithms that finds the *policy* that will best improve several indicators of the quality of the transportation system in Sioux Faux**. Here, we use *policy* to refer to a combination of inputs (as `.csv` files) representing changes in mass transit vehicle fleet composition, bus frequencies, and subsidies that could reduce the cost of multimodal transport for commuters.

Policies are tested by simulating the daily travels of a synthetic population of individuals called `Agents`, each with their own socio-demographic characteristics. The *agent-based simulation* is hosted by the BEAM simulator. During the simulated day, each *Agent* has a defined `Plan`, i.e. a sequence of activities with specific locations ordered by activity end times. Throughout the day, the `Agents` will make decisions on which transportation modes they will use, their departure times, and the routes they take to travel between activities. 

By simulating the daily travel behavior of the whole population, the quality of the city's transportation system can be evaluated, based upon scoring criteria, detailed [here](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md).

### What is BEAM?

BEAM stands for Behavior, Energy, Autonomy, and Mobility. It is an extension of the MATSim model, which is an agent-based transportation simulation framework. In this section we present a brief introduction to the agent-based simulation of transportation. You can find more documentation on BEAM or MATSim [here](https://beam.readthedocs.io/en/latest/about.html#overview). 


A BEAM simulation computes the interaction of *supply* and *demand* in a virtual urban transportation system. Supply is represented by the physical transportation infrastructure such as roads and subway lines as well as vehicles (personal, mass transit, and shared). Demand, on the other hand, consists of the planned *activities* of the synthetic commuters populating the virtual urban space. This may seem counter-intuitive, as we do not directly model the demand for transportation services. However, per modern transportation science, travel is theorized to be a by-product of our desire to participate in activities that are distributed in time and space. The less time a person spends traveling, the more *utility* the person gets from time spent at activities. Accordingly, the model of demand implemented in BEAM and MATSim an *activity-based model*, which operates on the principle that activities *induce demand* for travel. 

Like MATSim, BEAM simulates the simultaneous execution of *daily activity schedules* also known as *plans* on the virtual road network.  which consist of sequences of activities, one for each agent.  

Once all agents of the system have chosen their optimal transportation mode to attend their daily activities, the system reaches what we call an *equilibrium state*. Based on this equilibrium state, the simulator produces a series of outputs concerning the individual agents and the overall system. 


## The simulation inputs

The simulation inputs for BEAM are comprised of specifications regarding public transit operations, ridehail partnerships and subsidies, and public transit finances.

For the **pilot test**, the input parameters specify:
* **purchases and sales of buses serving a route**.
* **adjustments to the frequency of buses on routes**.
* **distribution of subsidies** for agents using ridehail and/or public transit.

You will find more information on the Sioux Faux simulation inputs, where they are stored, and how to control them on the [inputs to optimize](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Which-inputs-should-I-optimize.md) page.



## The simulation outputs: evaluating the system 


The quality of the new policy-based transportation system is evaluated based upon a comparison against the business as usual (BAU) scenario. The BAU scenario represents the baseline or "current" status-quo of the Sioux Faux transportation system. In other words, this is a "do-nothing" approach. This comparison answers the following question: **How will the new policy improve over the current state of the transportation system**?

The performance of this new policy-based transportation system is measured by a **scoring function**, which computes the weighted sum of three groups of outputs:

* How much *congestion* did the agents experience during the day? 
* What *level of service* did the transportation system offer to agents? 
* What were the *budgetary* impacts?

Positive total scores indicate that, under the evaluated policy portfolio, the system is performing better compared to the BAU scenario<sup id="a1">[1](#f1)</sup>.


You will find more information on the outputs of the simulation, how to interpret them, and the scoring function on the [outputs and the scoring function](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md) page.

<sup id="f1">1</sup> Pilot testers, please note the following: We understand that the simulator is inherently stochastic and that score outputs will vary to some extent on the **same** set of input variables. We have not yet officially established what is a statistically difference in scores. There are quite a few subtleties here, and we would love to get your feedback on what seems appropriate.[↩](#a1)

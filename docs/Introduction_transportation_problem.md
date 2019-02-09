# A Brief Introduction to the Urban Transportation System Optimization Framework

This document describes the goal and main components of the Uber Prize challenge, that is, the daily travel simulation environment, its inputs, and its outputs.


## Goal of Round I:

The overall goal of the preliminary round of the Uber Prize is to develop an algorithm that **finds the *policy* that will best improve several indicators of the quality of the transportation system in Sioux Faux**. Here, we use *policy* to refer to a combination of inputs (as `.csv` files) representing changes in mass transit vehicle fleet composition, bus frequencies, and incentives that could reduce the cost of multimodal transport for commuters.

Policies can be evaluated after simulating the daily travels of a synthetic population of individuals called *agents*, each with their own socio-demographic characteristics. The *agent-based simulation* is executed by the BEAM simulator. During the simulated day, each *agent* has a defined *plan*, i.e. a sequence of activities with specific locations ordered by activity end times. Throughout the day, these *agents* will make *decisions* as to which transportation *modes* they will use, their *departure times*, and the *routes* they take to travel between activities.

By simulating the daily travel behavior of the whole population, the quality of the city's transportation system can be evaluated, based upon scoring criteria, detailed [here](./Understanding_the_outputs_and_the%20scoring_function.md).

### What is BEAM?

BEAM stands for Behavior, Energy, Autonomy, and Mobility. It is an extension of the MATSim model, which is an agent-based transportation simulation framework. In this section we present a brief introduction to the agent-based simulation of transportation. You can find more documentation on BEAM or MATSim [here](https://beam.readthedocs.io/en/latest/about.html#overview). 

A BEAM simulation computes the interaction of *supply* and *demand* in a virtual urban transportation system. Supply is represented by the physical transportation infrastructure such as roads and subway lines as well as vehicles (personal, mass transit, and shared). Demand, on the other hand, consists of the planned *activities* of the synthetic commuters populating the virtual urban space. This may seem counter-intuitive, as we do not directly model the demand for transportation services. However, per modern transportation science, travel is theorized to be a by-product of our desire to participate in activities that are distributed in time and space. The less time a person spends traveling, the more *utility* the person gets from time spent at activities. Accordingly, the model of demand implemented in BEAM and MATSim is an *activity-based model*, which operates on the principle that activities *induce demand* for travel. 

Like MATSim, each *iteration* of a BEAM *run* simulates the simultaneous execution of *daily activity schedules* also known as *plans* on the virtual road network, which consist of sequences of activities, one for each agent. A single run consists of many iterations-- permitting agents to 

Once all agents of the system have chosen their optimal transportation mode to attend their daily activities, the system reaches what we call an *equilibrium state*. Based on this equilibrium state, the simulator produces a series of outputs concerning the individual agents and the overall system. 


## Policy Inputs

Inputs for **Round I** target improving transit operations, vehicle fleet assignment, and incentives to use non-motorized or on-demand transport.

For , the inputs specify:
* **Bus fleet composition changes**;
* **Distribution of incentives for agents using on-demand carsharing and/or mass transit**;
* **Adjustments to the frequency of buses on routes**; and,
* **Mass transit fares**.


You will find more information on the Sioux Faux simulation inputs, where they are stored, and how to control them on the [inputs to optimize](./Which-inputs-should-I-optimize.md) page.



## Evaluation metrics (scoring criteria)

The quality of changes to the transportation system induced by new policy are evaluated based upon a comparison against a *business as usual (BAU)* scenario. The BAU scenario represents the baseline or "current" status-quo of the Sioux Faux transportation system. In other words, this is the "do-nothing" scenario.

The performance of simulated policies over the baseline is measured using a **scoring function**. The scoring function is comprised of quantitative *metrics* that assess how well policies addressed the following questions:

* How much *congestion* did agents and the system as a whole experience during the day?
* What *level of service* did the transportation system provide to users?
* Did benefits to the transit company exceed its *operational* costs?
* Has *accessibility* to important opportunities or points of interest improved?
* Did the city achieve its *sustainability* goals?

Overall, this comparison answers the following question: *"How much can your policies **improve** the current state of the transportation system"*?

A total submission score less than 1 indicates that, under the evaluated policy portfolio, the system is performing *better* compared to the BAU scenario.

You will find more information on the outputs of the simulation, how to interpret them, and the scoring function on the [outputs and the scoring function](./Understanding_the_outputs_and_the%20scoring_function.md) page.

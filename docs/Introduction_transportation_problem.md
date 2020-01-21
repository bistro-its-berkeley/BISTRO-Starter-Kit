# A Brief Introduction to BISTRO: the Berkeley Integrated System for Transportation Optimization

This document describes the goal and main components of the BISTRO system, that is, the daily travel simulation environment of BISTRO, its inputs, and its outputs.


## Overview:

The primary goals of the BISTRO engine is to enable the optimization of transportation policies and the development of algorithms that **find the *policies* that best improve several indicators of the quality of the transportation system in a given user-defined scenario**. Here, we use *policy* to refer to a combination of inputs (as `.csv` files) representing changes in public transit vehicle fleet composition, service frequencies, and incentives that could improve user-defined metrics representing policy objectives.

Policies are tested via the BISTRO engine (see below), by simulating the daily travels of a synthetic population of individuals called `Agents`, each with their own socio-demographic characteristics. The *agent-based simulation* is hosted by the BEAM simulator. During the simulated day, each *Agent* has a defined `Plan`, i.e. a sequence of activities with specific locations ordered by activity end times. Throughout the day, the `Agents` will make *decisions* on which transportation *modes* they will use, their *departure times*, and the *routes* they take to travel between activities. 

### What is BISTRO?

The Berkeley Integrated System for Transportation Optimization (BISTRO) is an analysis and evaluation superlayer that works in concert with an agent-based simulation: Behavior, Energy, Autonomy, and Mobility (BEAM) to enable the open-sourced development and evaluation of transportation optimization methods in response to given policy priorities. 

### What is BEAM?

BEAM stands for Behavior, Energy, Autonomy, and Mobility. It is an extension of the MATSim model, which is an agent-based transportation simulation framework. Both [BEAM](https://beam.readthedocs.io/en/latest/about.html#overview) and [MATSim](https://matsim.org/docs/) are actively-developed, open source projects with extensive documentation. In this section we present a brief, focused introduction to the basic elements of travel demand modeling underlying these simulations. However we encourage interested participants to peruse the BEAM and MATSim documentation, papers, and code repositories as sources of inspiration for models and analysis.

A BEAM simulation computes the interaction of *supply* and *demand* in a virtual urban transportation system. Supply is represented by the physical transportation infrastructure such as roads and subway lines as well as vehicles (personal, mass transit, and shared). Demand, on the other hand, consists of the planned *activities* of the synthetic commuters populating the virtual urban space. This may seem counter-intuitive, as we do not directly model the demand for transportation services. However, per modern transportation science, travel is theorized to be a by-product of our desire to participate in activities that are distributed in time and space. The less time a person spends traveling, the more *utility* the person gets from time spent at activities. Accordingly, the model of demand implemented in BEAM and MATSim is an *activity-based model*, which operates on the principle that activities *induce demand* for travel. 

Like MATSim, each *iteration* of a BEAM *run* simulates the simultaneous execution of *daily activity schedules* also known as *plans* on the virtual road network, which consist of sequences of activities, one for each agent. Plans are scored based on how well they maximize an agent's trade-off between time and money (i.e., in BEAM, all travel time *costs* are converted to a single monetary scale based on an agent's inherent valuation of travel time). Please note that this "score" __is not__ in any way the same as the contestant's evaluation score. Agents retain a limited memory of previously executed plans together with the plan scores. A single run consists of many iterations-- permitting agents to adjust their plans. At the end of each iteration, a fraction of agents is randomly selected to change their plans according to a strategy that is sampled from a extreme value (softmax) distribution over plan scores (i.e., the plan with the highest score has an exponentially higher chance of being selected than a lower-scoring plan, while plans with the same score have the same probability of selection).  <br>

Unlike MATSim; however, agents in BEAM can adapt to changing conditions during an iteration according to what is known as a _within-day_ or _online_ model. In BEAM, agents are endowed with the ability to make unplanned and time-sensitive choices about how to maximize their mobility under dynamic resource constraints. This feature is essential in modeling how the emerging shared, on-demand, and micromobile travel modalities interact with existing urban transportation infrastructure and services.

Once all of the agents in the system have decided on the best travel modes, departure times, and routes to reach their daily activities, the system reaches what we call an *equilibrium state*. Equilibrium occurs when, after many iterations, agents are no longer able to improve their plan scores, and the cumulative average score over each agents set of plans reaches a fixed point. Upon reaching this point (which may be determined empirically based on the data provided to the simulator and its configuration parameters), BEAM produces a series of statistics and outputs describing the aggregate performance of system components as well as a snapshot of all events that occurred over the course of the simulation. 

## Policy Inputs

Inputs may target improving transit operations, vehicle fleet assignment, and/or incentives to use non-motorized or on-demand transport. 

Example inputs include: 
* **Bus fleet composition changes**;
* **Distribution of incentives for agents using on-demand carsharing and/or mass transit**;
* **Adjustments to the frequency of buses on routes**; and,
* **Mass transit fares**.

You will find more information on the Sioux Faux Benchmark Scenario simulation inputs, where they are stored, and how to control them on the [inputs to optimize](./Which-inputs-should-I-optimize.md) page.


## Key Performance Metrics (scoring criteria)

The quality of the new policy-based transportation system is evaluated based upon a comparison against the *business as usual (BAU) scenario*. The BAU scenario represents the baseline or "current" status-quo of the Sioux Faux transportation system. In other words, this is a "do-nothing" approach. This comparison answers the following question: **How will the new policy improve over the current state of the transportation system**?

The performance of simulated policies over the baseline is measured using a **scoring function**. The scoring function is comprised of one or more quantitative *key performance metrics (KPIs)* that assess how well policies addressed the following questions:

* How much *congestion* did agents and the system as a whole experience during the day?
* What *level of service* did the transportation system provide to users?
* Did benefits to the transit company exceed its *operational* costs?
* Has *accessibility* to important opportunities or points of interest improved?
* Did the city achieve its *sustainability* goals?

Overall, this comparison answers the following question: *"How much can your policies **improve** the current state of the transportation system"*?

A total submission score less than 1 indicates that, under the evaluated policy portfolio, the system is performing *better* in comparison to the BAU scenario.

You will find more information on the outputs of BISTRO, how to interpret them, and the scoring function on the [outputs and the scoring function](./Understanding_the_outputs_and_the%20scoring_function.md) page.

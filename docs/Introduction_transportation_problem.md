# A quick introduction to the Transportation Systems Challenge Framework

This document aims to provide an overview of the challenge framework. It describes the main components of the challenge: the daily travel simulation hosted by BEAM, its inputs, outputs, and the way it all interacts with the optimization algorithm you have to develop.   

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Simulation_Framework.png)

## The simulation of daily urban travels

The overall goal of the first phase of the Uber Prize is to find the **best policy** that will **optimize the quality of the  transportation system in Sioux Faux**. A *policy* is a combination of inputs related to public transit operations, ridehail partnerships and subsidies, and public transit finances.

Policies are tested by simulating the daily travels of a synthetic population of individuals called *Agents*, each with their own socio-demographic characteristics. The *agent-based simulation* is hosted by the BEAM simulator. During the simulated day, each *Agent* has a defined *Plan*, i.e. an ordered series of activites with specific start times, durations that she wants to complete. Throughout the day, the *Agents* will make decisions on which transportation modes they will use to travel to and from their daily activities. 

By simulating the daily travel behavior of the whole population, the quality of the city's transportation system can be evaluated, based upon scoring criteria, detailed [here](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md).

### What is BEAM?

BEAM stands for Behavior, Energy, Autonomy, and Mobility. It is an extension of the MAtSim model, which is an agent-based transportation simulation framework. 

You can find more documentation on BEAM or MATSim [here](https://beam.readthedocs.io/en/latest/about.html#overview).

## The simulation inputs

The simulation inputs for BEAM are comprised of specifications regarding public transit operations, ridehail partnerships and subsidies, and public transit finances.

For the **Hackathon** the input parameters are:
* the **bus fleet composition**
* the **distribution of subsidies** for agents using ridehail and/or public transit

You will find more information on the Sioux Faux simulation inputs, where they are stored, and how to control them on the [inputs to optimize](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Which-inputs-should-I-optimize%3F.md) page.

## The simulation outputs: evaluating the system 

Once all agents of the system have chosen their optimal transportation modes--via iteration--to attend their daily activities, the system reaches what we call an *equilibrium state*. Based on this equilibrium state, the simulator produces a series of outputs concerning the individual agents and the overall system. 

The quality of the new policy-based transportation system is evaluated based upon a comparison against the Business As Usual Scenario (BAU). The BAU scenario represents the baseline or "current" policy of Sioux Faux. This comparison captures **how the new policy will improve the current state of the transportation system**.
The performance of this new policy-based transportation system is measured by a **scoring function S** which computes the weighted sum of three groups of outputs:

* How much *congestion* did the agents experience during the day? 
* What *level of service* did the transportation system offer to agents? 
* What were the *budgetary* impacts?

The higher the score, the better the system is performing compared to the BAU scenario.

You will find more information on the outputs of the simulation, how to interpret them, and the scoring function on the [outputs and the scoring function](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md) page.

## What is the goal of the optimization challenge?  

The Uber Prize optimization problem consists of developing an **optimization algorithm** to **find the best policy**, i.e., the best set of inputs that will **maximize the scoring function S**.

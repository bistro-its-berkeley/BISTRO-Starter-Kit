# A quick introduction to the Transportation Systems Challenge Framework

This document aims at giving you an overview of the challenge framework. It describes the main components of the challenge, i.e. the daily travel simulation host by BEAM, its inputs, outputs and the way it interacts with the optimization algorithm you have to develop.   

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Overview%20Challenge%20Framework.png)

## The simulation of daily urban travels

The overall goal of the first phase of the Uber Prize is to find the **best policy** that will **optimize the quality of the  transportation system in Sioux Faux**. A *policy* is a combination of inputs on public transit operations and public transit financial aspects.

To test a policy, we want to simulate the daily travels of a population of simulated individuals called *Agents*. This agent-based simulation is hosted by the BEAM simulator. During the simulated day, each *Agent* has a defined *Plan*, i.e. a serie of activites with specific start times, durations and in a specific order that he wants to attend. Throughout the day, the *Agents* will make decisions on which transportation modes they will use to travel to and from their daily activities. 

By simulating the daily traveling behavior of the whole population, the quality of the city's transportation system can be evaluated.

### What is BEAM?

The simulator BEAM stands for Behavior, Energy, Autonomy, and Mobility. It is an extension of the MAtSim model, which is a agent-based transportation simulation framework.

You can find more documentation on BEAM or MATSim [here](https://beam.readthedocs.io/en/latest/about.html#overview).

## The simulation inputs

The simulation inputs for BEAM is a combination of inputs on public transit operations and public transit financial aspects.

The one you will have control on for the Hackathon are:
* the **bus fleet composition**
* the **distribution of subsidies** for users using on-demand rideshare or walking to access public transit 

You will find more information on the Sioux Faux simulation inputs, where their are stored and how to control them in the [inputs to optimize](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Which-inputs-should-I-optimize%3F.md) page.

## The simulation outputs: evaluating the system 

Once all agents of the system have chosen their optimal transportation modes to attend their daily activities, the system reaches what we call an *equilibrium state*. Based on this equilibrium state, the simulator gives back a serie of outputs concerning the individuals and the system in general. 

The quality of the new policy-based transportation system is evaluated based on the new system performance over the day compared to the base-policy scenario. The performance is measured thanks to a scoring function S which computes the weighted sum of three groups of outputs:

* How much *congestion* did the agents experience during the day?
* What *level of service* did the transportation system offer to agents?
* What *costs* were incurred by the city?

The bigger the score, the more performant the system.

You will find more information on the outputs of the simulation, the scoring functino and how to interpret them in the [outputs and the scoring function](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md) page.

## What is the goal of the optimization challenge?  

The Uber Prize optimization problem consists of developping an **optimization algorithm** to **find the best policy**, i.e. the best policy-inputs combination, that will **maximize the scoring function S**.

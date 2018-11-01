# A quick introduction to the Transportation Systems Challenge Framework

This document aims at giving you an overview of the challenge framework. It describes the main components of the challenge, i.e. the daily travel simulation host by BEAM, its inputs, outputs and the way it interacts with the optimization algorithm you have to develop.   

![Alt text](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/Images/Overview%20Challenge%20Framework.png)


## The simulation of daily urban travels

2-3 sentence from the pb statement *To be completed*

### What is BEAM?
BEAM stands for Behavior, Energy, Autonomy, and Mobility. - *To be completed*

To read more documentation on BEAM, click [here](https://beam.readthedocs.io/en/latest/about.html#overview).

## The simulation inputs

- *To be completed*
Combination of inputs on public transit operations and public transit financial aspects.


## The simulation outputs: evaluating the system 

Once all agents of the system have chosen their optimal transportation modes to attend their daily activities, the system reaches what we call an *equilibrium state*. Based on this equilibrium state, the simulator gives back a serie of outputs concerning the individuals and the system in general. 

The quality of the new policy-based transportation system is evaluated based on the new system performance over the day compared to the base-policy scenario. The performance is measured thanks to a scoring function S which computes the weighted sum of three groups of outputs:

* How much *congestion* did the agents experience during the day?
* What *level of service* did the transportation system offer to agents?
* What *costs* were incurred by the city?

The bigger the score, the more performant the system.

## What is the goal of the optimization challenge?  

The Uber Prize optimization problem consists of developping an optimization algorithm to find the best policy, i.e. the best policy-inputs combination, that will maximize the scoring function S.

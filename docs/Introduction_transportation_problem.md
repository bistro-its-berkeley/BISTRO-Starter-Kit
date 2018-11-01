# A quick introduction to the Transportation Optimization Problem

Introduction sentence

## What is BEAM?

BEAM stands for Behavior, Energy, Autonomy, and Mobility. *To be completed*

To read more documentation on BEAM, click [here](https://beam.readthedocs.io/en/latest/about.html#overview).

## What are the inputs of BEAM?

(combination of inputs on public transit operations and public transit financial aspects)


## What are the outputs of BEAM and how are they used to evaluate the transportation system? 

Once all agents of the system have chosen their optimal transportation modes to attend their daily activities, the system reaches what we call an *equilibrium state*. Based on this equilibrium state, the simulator gives back a serie of outputs concerning the individuals and the system in general. 

The quality of the new policy-based transportation system is evaluated based on the new system performance over the day compared to the base-policy scenario. The performance is measured thanks to a scoring function S which computes the weighted sum of three groups of outputs:

* How much *congestion* did the agents experience during the day?
* What *level of service* did the transportation system offer to agents?
* What *costs* were incurred by the city?

The bigger the score, the more performant the system.

## Optimizing the policy  

The Uber Prize optimization problem consists of developping an optimization algorithm to find the best policy, i.e. the best policy-inputs combination, that will maximize the scoring function S.

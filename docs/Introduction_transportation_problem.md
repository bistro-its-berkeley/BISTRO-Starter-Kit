# A quick introduction to the Transportation Optimization Problem

Introduction sentence

## What is BEAM?

BEAM stands for Behavior, Energy, Autonomy, and Mobility.

To read more documentation on BEAM, click [here](https://beam.readthedocs.io/en/latest/about.html#overview).

## What are the inputs of BEAM?

(combination of inputs on public transit operations and public transit financial aspects)


## What are the outputs of BEAM? 

Once all agents of the system have chosen their optimal transportation modes to attend their daily activities, the system reaches what we call an *equilibrium state*. The quality of the new policy-based transportation system can then be evaluated based on the new system performance compared to the base-policy scenario. Three elements are evaluated here:

* How much *congestion* did the agents experienced during the day?
* What *level of service* did the transportation system offer to agents?
* What *costs* were incurred by the city?

These three elements are gathered and weighted in a scoring function S. The bigger the score, the more performant the system.

## Optimizing the policy  

The Uber Prize optimization problem consists of developping an optimization algorithm to find the best policy, i.e. the best policy-inputs combination, that will maximize the scoring function S.

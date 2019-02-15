# The Sioux Faux Scenario

For this first Round, you are asked to optimize the transportation network for a *sample of citizens* from a mock city: Sioux Faux. The city’s 157,000 citizens travel between activities using either their personal automobiles, buses provided via a public transit system, taxis enabled via an on-demand carsharing company, active modes such as walking, or a combination of multiple modes in accordance with their preferences. You will compete with other contestants to produce the best transportation outcomes as computed by the [scoring function](./Understanding_the_outputs_and_the%20scoring_function.md).

<img src="/Images/Mode_choice_diagram.png" width="80%"> <br>
***Figure 1: The transportation modes available to Sioux Faux population*** 

## Sioux Faux network
The Sioux Faux road network is shown below (Fig. 1). Currently, the Sioux Faux Bus Lines (SFBL) transportation company operates twelve bus lines in the city.

<img src="/Images/sf_route_guide.png" width="60%"> <br>
***Figure 2: Sioux Faux Network***

## Sioux Faux sample population

In order to simulate the activity and travel behavior of the citizens of Sioux Faux, a population of virtual agents and households was generated such that the sociodemographic attributes of these virtual entities are spatially distributed in accordance with real-world census data (see Figure 3). In order to provide realistic distributions of household and individual attributes for Sioux Faux, we expanded publicly-available survey data for the city of Sioux Falls, South Dakota.

<img src="/Images/Demographics.png"> <br>
***Figure 3: Demographics of Sioux Faux***

For Round 1, you have access to two sample populations with which you can run simulations:
* a 1,000 (1k) individuals sample
* a 15,000 (15k) individuals sample

It is permissible to use either sample as you generate training data for your algorithm. For example, you can develop your algorithm using the 1k scenario and then test it with the 15K population scenario. However, official submissions must be run with the 15K sample population.

## Problem statement 
To get a more thorough description of the Sioux Faux challenge, please refer to the [Problem Statement](./Problem_statement_Phase%20I.pdf).

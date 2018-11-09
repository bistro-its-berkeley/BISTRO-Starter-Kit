# Uber-Prize-Starter-Kit

This is a starter-kit Repository for the **Uber Prize challenge** on **Crowd AI**. 

In this repo you will find background materials that will help you get started with the challenge. 

## Competition Phasing
The competition will be split into two phases:
* The first phase challenges contestants to optimize the transportation network of a small mock city: Sioux Faux 
* The second phase will apply the optimization challenge on a real city, to be announced by the launch of the Uber Prize

## Internal pilot test

The **internal pilot test** aims at testing the ability for participants to compete in Phase 1 of the competition. Given the complexity with a simulator, we want to do an initial round of internal testing with a core group of members from AI Labs in order to identify any issues.

The **objectives** of this internal pilot test are:
* How easy/difficult is it to on-board participants, and feel comfortable moving forward with a solution approach, given the starter kit and associated documentation?
  * Update documentation in response to this.
* We are looking for optimization algorithms that explore the set of feasible solutions to the Sioux Faux scenario given the possible input variables and corresponding constraints.
  * We are not necessarily looking to generate the best solutions, but to assess the difficulty of the problem given the current dimensions of the input space
  * Ideally, we should also identify any obvious “cheats” and address them.
* Review feedback and user-generated reports to identify likely approaches/models.
If an approach seems particularly worthwhile, then request that it be submitted as a “benchmark solution”.


## How do I get started?

Before you can get started, some explanations on the challenge are needed. Even though you will not have to deal with complex transit analysis (the BEAM simulator will do it for you!), understanding a few transportation concepts and the general framework of the simulator will help you to grasp the framework of the challenge. 

We recommend that you proceed through the documentation in the following order:

  * **Introduction to the Transportation Systems Challenge Framework**: First, read the quick [introduction on the Urban Transportation Optimization problem](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Introduction_transportation_problem.md). It will give you a general understanding of the framework of problem you need to solve and the related optimization challenges. 

  * **The Problem statement for the Hackathon**: Then, read through the [presentation of the Sioux-Faux case] for the Hackathon, which provides a high-level description of the tasks, as well as information on the outputs and scoring function. **LINK**
  
  * **The inputs to optimize**: Next, the [Which inputs should I optimize?](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Which-inputs-should-I-optimize%3F.md) page will give you the steps for installing BEAM and understanding what the inputs of the simulation are, where they are stored, and how to modify them.
  
  * **The description of the outputs**: Once you're familiar with the inputs, read the [Understanding the outputs and the scoring function](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md) page to get a better understanding of the outputs of the simulation, where they are stored after a simulation run, what they describe, and how to interpret them. Here you will also find details on how the outputs are used to construct the challenge scoring function.
  
  * **The tutorial on how to run a simulation**: Once you are clear about the inputs you can manipulate, the outputs, and the effects of changes in inputs on the outputs, the [How to run a simulation?](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/How_to_run_a_simulation%3F.md) page will explain the steps to run a simulation.
  
  * **How to submit?** To finish, follow the [How to submit?](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/What_and_how_to_submit%3F.md) instructions to submit your solution.
  

## What do I have to do?

Your will generate a set of inputs (where a set of inputs can be thought of as a policy--find more on this in the [Problem Statement](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Problem_statement_Sioux_Faux_Phase1) to optimize the transportation system of Sioux Faux, based upon the criteria given in the Problem Statement. Solutions will be judged using the scoring function, and your goal is to achieve the **highest score**. In the event of ties, solutions will be further assessed on their performance with respect to other key metrics. *(Note to organizers: metrics [X,Y,Z] + the explanation, potentially? TBD)*.

Once you have a solution, you should submit:
* your **best outputs (.zip)**
* a **brief explanation on your methodology (.doc)**: For example: how did you solve the optimization problem? What was the motivation behind your approach? What did you try? What failed? Is there some room for improvement?
* any comments on this starter kit repository (as pull requests) if you see any unclear information or have any suggestions for improvements.

For info on how to submit, read this [tutorial](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/What_and_how_to_submit%3F.md).

## What can I find in this repository?

* Documentation folder 
  * the [Quick introduction on the Urban Transportation Optimization problem](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Introduction_transportation_problem.md)
  * a note on [how to run a simulation](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/How_to_run_a_simulation%3F.md)
  * a description of the [inputs to optimize](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Which-inputs-should-I-optimize%3F.md)
  * a description of the [outputs and the scoring function](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md)
  * a presentation of [the Sioux-Faux case](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/The_Sioux_Faux_case_Hackathon.md)
  * the Problem statement of the Hackathon - *to be added*
  * the [Problem statement of Phase 1](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Problem_statement_Phase%20I.pdf) 
  * a note on [what and how to submit](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/What_and_how_to_submit%3F.md) 
 

## Contacts

If you have any questions about the challenge, you can ask them on this FAQ chat:
* *(To be set for phase I)*

In case of further questions, you can contact:
* Sid Feygin: sid.feygin@berkeley.edu
* Valentine Golfier-Vetterli: golfiervalentine@gmail.com

*Note to organizers: Consider setting up a troubleshooting email account so you don't have to use your personal ones*

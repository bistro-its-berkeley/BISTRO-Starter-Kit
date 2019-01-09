# Uber Prize Starter Kit

This repository is a starter kit for the **Uber Prize Challenge** on **[Crowd AI](https://www.crowdai.org/)** where you may find background material and competition guidelines to help you get started. 

## Competition Rounds
The competition will be split into two rounds:
* The first round challenges contestants to optimize the transportation network of a small fictitious city: Sioux Faux 
* The second round will require contestants to apply their optimization algorithms to a real city, which will be announced prior to the launch of the Uber Prize.

## How do I get started?

While the problem setting may not be as familiar as that of previous machine learning and AI competitions, our aim has been to make on-boarding to this competition as straightforward as possible for practitioners both with and without domain expertise. However, prior to jumping into developing a solution, please review the background material and preliminaries provided in this repository. Although you will not have to deal with complex transit analysis (the simulation engine will do it for you!), understanding a few transportation planning terms and concepts concepts will likely improve your understanding of the system that you will be modeling. 

We recommend that you proceed through the documentation in the following order:

  * **Introduction to the Urban Transportation System Optimization Problem**: First, read the brief [introduction to the Urban Transportation System problem](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Introduction_transportation_problem.md), which will give you a general understanding of the framework of problem you need to solve as well as the relevant optimization challenges. 

  * **Problem statement for internal pilot testing**: Then, review the [presentation of the Sioux Faux scenario](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/The_Sioux_Faux_case_pilot_study.md), which introduces the problem setting and particulars of transportation system running in the simulation environment.
  
  * **Inputs to optimize**: Next, please refer to the [input file specification schema](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Which-inputs-should-I-optimize.md), which describes the structure of the input files and their relationship to quantities computed in the context of the virtual transportation environment.
  
  * **Submission evaluation and outputs**: The page describing [the outputs and scoring function](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md) will help you to familiarize youself with the outputs of the simulation, where they are stored after a simulation run, what they describe, and how to interpret them. Here you will also find details on how the outputs are used to construct the challenge scoring function.
  
  * **Simulation tutorial**: Once you are clear about the inputs you can manipulate, the outputs, and the effects of changes in inputs on the outputs, try [running a simulation](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/How_to_run_a_simulation.md).
  
  * **Submission instructions** When you are ready, please follow [these instructions](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/What_and_how_to_submit.md) to submit your solution.
  

## What can I find in this repository?

* `docs` folder: 
  * an [introduction to the urban transportation system optimization problem](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Introduction_transportation_problem.md)
  * a note on [how to run a simulation](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/How_to_run_a_simulation.md)
  * a description of the [input schema](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Which-inputs-should-I-optimize.md)
  * a description of the [simulation outputs and the scoring function](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Understanding_the_outputs_and_the%20scoring_function.md)
  * an outline of [the Sioux Faux scenario](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/The_Sioux_Faux_case_pilot_study.md)
  * the [problem statement for the pilot test](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/Problem_Statement_Pilot_Study.pdf)
  * the [problem statement for round 1](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/docs/Problem_statement_Phase%20I.pdf)
  * a note on [what and how to submit](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/docs/What_and_how_to_submit.md)

* `submission-inputs` folder:
  * the input file for the [bus fleet composition](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/submission-inputs/VehicleFleetMix.csv)
  * the input file for the [mode subsidies](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/submission-inputs/ModeSubsidies.csv)
  * the input file for the [bus frequency adjustments](https://github.com/vgolfier/Uber-Prize-Starter-Kit/blob/master/submission-inputs/FrequencyAdjustment.csv)

* `reference-data/sioux_faux_gtfs_data` folder: <br> <br>
List of the Sioux Faux GTFS data (General Transit Feed Specification). It is a series of text files, each of them modeling a particular aspect of the transit agency's operations: stops, routes, trips, and other schedule data. The details of each file and their relationships are defined in the [GTFS reference](https://developers.google.com/transit/gtfs/reference/).

## Contributing

We always welcome bug reports and enhancement requests from both competitors as well as developers on the Uber Prize-Berkeley Working Group team and elsewhere. Guidelines and suggestions on how to contribute code to this repository may be found in [./github/CONTRIBUTING.md](./github/CONTRIBUTING.md].

## Contact Information

If you have any questions about the challenge, you can ask them on uChat:
* https://uchat.uberinternal.com/uber/channels/uber_prize_round1_pilot_test

Alternatively, to contact the Uber Prize working group technical team directly, please e-mail:
* Sid Feygin: sfeygi@ext.uber.com
* Valentine Golfier-Vetterli: vgolfi@ext.uber.com



<!--*Note to organizers: Consider setting up a troubleshooting email account so you don't have to use your personal ones*-->

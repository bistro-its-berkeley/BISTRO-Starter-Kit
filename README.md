<!--Logo Goes Here!-->

This repository is a Starter Kit for the **Uber 2019 ML Hackathon** on **[AICrowd](https://www.aicrowd.com/challenges/uber-prize)**. 

## Competition
The competition aims at solving and hacking the first round of the inaugural Uber Prize, which will be launched in the Spring 2019. It challenges contestants to optimize the transportation network of a small mock city: Sioux Faux. 

## How do I get started?

While the problem setting may not be as familiar as that of previous machine learning and AI competitions, our aim has been to make on-boarding to this competition as straightforward as possible for practitioners both with and without domain expertise. However, prior to jumping into developing a solution, please review the background material and preliminaries provided in this repository. Although you will not have to deal with complex transit analysis (the simulation engine will do it for you!), understanding a few transportation planning terms and concepts will likely improve your understanding of the system that you will be modeling. 

We recommend that you proceed through the documentation in the following order:

  * **Introduction to BISTRO: the Berkeley Integrated System for Transportation Optimization**: First, read the brief [introduction to BISTRO](./docs/Introduction_transportation_problem.md), which will give you a general understanding of the framework of the problem you need to solve as well as the relevant optimization challenges. 

  * **Problem statement**: Then, review the [presentation of the Sioux Faux scenario](./docs/The_Sioux_Faux_scenario.md), which introduces the problem setting and particulars of transportation system running in the simulation environment.
  
  * **Inputs to optimize**: Next, please refer to the [input file specification schema](./docs/Which-inputs-should-I-optimize.md), which describes the structure of the input files and their relationship to quantities computed in the context of the virtual transportation environment.
  
  * **Submission evaluation and outputs**: The page describing [the outputs and scoring function](./docs/Understanding_the_outputs_and_the%20scoring_function.md) will help you to familiarize youself with the outputs of the simulation, where they are stored after a simulation run, what they describe, and how to interpret them. Here you will also find details on how the outputs are used to construct the challenge scoring function.
  
  * **Simulation tutorial**: Once you are clear about the inputs you can manipulate, the outputs, and the effects of changes in inputs on the outputs, try [running a simulation](./docs/How_to_run_a_simulation.md).
  
  * **Submission steps**: When you feel ready to submit a solution, follow [these steps](./docs/What_and_how_to_submit%3F.md).
  
  * **FAQ**: If you have any questions about the transportation problem, simulations or troubleshooting, you may find your answer in the [FAQ](./docs/FAQ.md) page.
  

## What can I find in this repository?

* `docs` folder: 
  * an [introduction to BISTRO: the Berkeley Integrated System for Transportation Optimization](./docs/Introduction_transportation_problem.md)
  * a note on [how to run a simulation](./docs/How_to_run_a_simulation.md)
  * a description of the [input schema](./docs/Which-inputs-should-I-optimize.md)
  * a description of the [simulation outputs and the scoring function](./docs/Understanding_the_outputs_and_the%20scoring_function.md)
  * an outline of [the Sioux Faux scenario](./docs/The_Sioux_Faux_scenario.md)
  * the [problem statement for round 1](./docs/PS_SD_Uber_hackathon_2019.pdf)
  * the steps to [submit a solution](./docs/What_and_how_to_submit%3F.md)
  * a [FAQ](./docs/FAQ.md) page

* `submission-inputs` folder:
  * the input file for the [bus fleet composition](./submission-inputs/VehicleFleetMix.csv)
  * the input file for the [mode incentives](./submission-inputs/ModeIncentives.csv)
  * the input file for the [bus frequency adjustments](./submission-inputs/FrequencyAdjustment.csv)
  * the input file for the [mass transit fares](./submission-inputs/MassTransitFares.csv)


* `reference-data/sioux_faux_gtfs_data` folder: <br> 
List of the Sioux Faux GTFS data (General Transit Feed Specification). It is a series of text files, each of them modeling a particular aspect of the transit agency's operations: stops, routes, trips, and other schedule data. The details of each file and their relationships are defined in the [GTFS reference](https://developers.google.com/transit/gtfs/reference/).

* `utilities` folder: <br> 
List of utility scripts provided to simplify the interface with the BISTRO simulator and its inputs / outputs.
  * the [competition_executor.py](./utilities/competition_executor.py) script
  * the [visualization.py](./utilities/visualization.py) script 
  * the [random_search.py](./utilities/random_search.py) script
  * the [input_sampler.py](./utilities/input_sampler.py) script
 
* `examples` folder: <br> 
Exmaple python notebooks demonstrating the use of the `competition_executor.py`, `input_sampler.py`and `visualization.py` scripts. 
  * the [Starter Kit Utilities Tutorial](./examples/Starter_Kit_Utilities_Tutorial.ipynb) notebook : to run a simulation and generate random inputs
  * the *Visualization* notebook : to plot input and output parameters

## Updates to the Starter Kit

<!--TODO: Provide details on announcement process/location-->

In order to expedite bug support, we may periodically push new Docker images to DockerHub as well as update this 
repository. Whenever such an update is announced, please run `git pull` in this directory (you might wish to move [submission-inputs](./submission-inputs) and update execution paths appropriately. Please also run `docker pull beammodel/beam-competition:0.0.1-SNAPSHOT` to ensure the image is up-to-date as well.


## Contributing

We always welcome bug reports and enhancement requests from both competitors as well as developers on the Uber Prize-Berkeley Working Group team and elsewhere. Guidelines and suggestions on how to contribute code to this repository may be found in [./github/CONTRIBUTING.md](./.github/CONTRIBUTING.md).

## Contact Information
If you have any questions concerning the competition, please, review first the [FAQ page](./docs/FAQ.md).

If your question was note answered in the FAQ page, you can ask it on the [2019 Uber Prize ML Hackathon](https://uchat.uberinternal.com/uber/channels/2019-uber-prize-ml-hackathon) Uchat channel.

<!-- Alternatively, to contact the Uber Prize working group technical team directly, please e-mail:
* Sid Feygin: [sfeygi@ext.uber.com](mailto:sfeygin@ext.uber.com)
* Valentine Golfier-Vetterli: [vgolfi@ext.uber.com](mailto:vgolfi@ext.uber.com)-->

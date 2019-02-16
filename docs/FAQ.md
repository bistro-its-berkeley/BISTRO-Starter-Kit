# Technical FAQ

This document gathers the recurrent questions about the Uber Prize in general, the transportatino problem, the BISTRO simulations and include also a Troubleshooting page.


### 1. TRANSPORTATION PROBLEM
<details>
<summary><strong>Why are alternatives to the car limited to buses and on-demand rideshare? What about metro, bikes, scooters..etc?</strong></summary>
<br>
The goal of Phase I is to evaluate Sioux Faux as a benchmark city. This will provide contestants a first “simple” scenario to discover and familiarize themselves with the optimization problem. Phase II of the Uber Prize will include a broader range of multimodal options.
</details>


<details>
<summary><strong>Why is Sioux Falls/ Sioux Faux used as a benchmark city?</strong></summary>
<br>
The Sioux Falls transportation network has been frequently used in the transportation modelling domain, and, in particular, has often served as a useful test case in agent-based traffic simulations. Its accessible scale and the large amount of previous research work and data available for the city make it a good candidate to build and test transportation models.
</details>

### 2. SIMULATION

*2.1. Simulation Variability*

Contestants may notice that their scores vary between runs when using the same inputs combinations. The following items describe the nature of this variance and how we plan to account for it in when differentiating between top-ranked entries.

<details>
<summary><strong>Is the simulation deterministic?</strong></summary>
<br>
The BEAM model was developed to enable parallel discrete event simulation of transportation systems. This has the benefit of increasing the scalability of what can be simulated (e.g. larger, more populous cities), but there is a tradeoff on absolute determinism, which is not possible with BEAM. The BEAM scheduler dispatches event triggers in chronological order, but these triggers are executed asynchronously by agents in the simulation. In response to an event trigger, an agent may reserve a resource in the simulation (e.g. a parking space) before another agent, even if both agents do so at the same simulation time step. 

</details>

<details>
<summary><strong>Is the score reproducible/numerically stable between runs using identical inputs?</strong></summary>
<br>
As explained in the answer to the previous question, there is no guarantee which agent will acquire the resource first and therefore there can be no guarantee about absolute reproducibility between runs with identical inputs. However, in experiments, BEAM has been demonstrated to achieve reproducibility by reporting aggregate statistics from a number of runs. The approximate number of runs necessary to converge on a stable value of the key metrics of interest must be determined empirically; however, we have empirically found that between 5 and 10 total runs per submission is sufficient to determine the overall score with 99.99% confidence. 


</details><br>

*2.2. Simulation Settings*

<details>
<summary><strong>What is warm start and how is it used?</strong></summary>
<br>
Every simulation run starts from the baseline calibrated scenario (BAU) in order to have a standard of comparison. The BAU scenario itself is the result of dynamic traffic assignment performed by BEAM using a modified version of the MATSim co-evolutionary approach (see < link to documentation />). Warm start avoids having to redo this process, which can add an extra 100 iterations to the simulation. Using this approach is the prevailing practice in the literature, so also permits comparison with similar policy evaluation systems.
</details>

<details>
<summary><strong>What is the “--iters” option? How many iterations should I choose for my simulation?</strong></summary>
<br>
After playing with several policy variants and analyzing the outputs (in particular, paying attention to the scoreStats.png/.txt), you may notice that the agent ensemble average scores get worse at first and then begin to improve after a number of iterations. This process, known as relaxation, may seem familiar to those familiar with reinforcement learning, as it is analogous to the concept of exploration. Agents explore new routes, modes, and activity timings to try to find better plans after policies perturb the travel environment. The number of iterations needed to reach a fixed point will vary between sets of inputs; however, it is likely that you will see some immediate change to highly sensitive indicators such as mode choice. In contrast to MATSim, which (by default) slowly varies agent plans, BEAM’s reactive agents respond rapidly to changes in the transportation system. Thus, while the plans may continue to improve many over iterations, the magnitude of immediate change in behavior following a certain change in policy may provide enough information to pursue or discard a search coordinate. Running for only one iteration could permit rapid exploration of the search space. On the other hand, it is difficult to predict the rate of evolution of scores to a final fixed point. We thus leave it up to the contestant to determine how many fewer iterations (if any) than the official 150 iteration evaluation run could be a useful strategy in accelerating search algorithms. 
</details>




### 3. TROUBLESHOOTING

Contestants may complain that simulations take a long time. The following items suggest some hints to improve execution time or otherwise accelerate search.

*3.1. Computational Complexity*

<details>
<summary><strong>Nothing is happening! Is the simulation stuck?</strong></summary>
<br>
Most likely not! You will have probably seen a validation error if your inputs do not match the schema specified in <link_to_schema>. In this case, the simulation should end immediately and a “Failed” indicator will appear on the “Submissions” tab next to this submission. You may examine beamLog.out and validation-errors.out files to determine the source of the error.

</details>

<details>
<summary><strong>How can I maximize use of compute resources available to me?</strong></summary>
<br>
Consider using the “1k”-scenario (see <link to PS section> for more info).
</details>

<details>
<summary><strong>A simulation run takes way too long! Why? How can I make the simulation run more quickly? What is the maximum performance that I can expect?</summary>
<br>
* This is to be expected. The simulation may run slowly depending on your computational environment. Currently, the primary bottleneck is routing. Even for the 15k scenario, the routing engine generates millions of routes (reflecting multimodal options for agents to choose between) for a single simulation run.  
* Routing is highly CPU-bound, so once you’ve met the minimum memory requirements (~8-16GB) the more CPUs you can throw at it, the better! 
* Depending on whether you run on a local machine meeting minimal hardware requirements (4 CPU/8GB)  or a beefy cloud server (72 CPU/148 GB) you should expect the following times for a single simulation run of 100 iterations:

</details>



# How to run a simulation?

## Requirements

*Software Requirements*:

There is only one firm software requirement at the moment:
- [Docker](https://www.docker.com)

You can find the instructions to install Docker for Mac [here](https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac) and for Windows [here](https://docs.docker.com/docker-for-windows/install/)

Thus, the code is OS-agnostic.

Note that some of the provided utility scripts require a python installation with the [docker-py](https://docker-py.readthedocs.io/en/stable/) installed. Please run `pip install docker` prior to running the scripts.

*Hardware Requirements*:

There are no strict hardware requirements; however, performance will increase substantially with more CPUs (as well as, to some extent, more memory). At a bare minimum, we recommend 8GB RAM and 2 CPUs. Initial observations for the 1k sample on the minimum hardware clock in at ~5s/iteration. On a more powerful machine with 12 CPUs We provide some parameter settings on the `docker run` entrypoint below so that this parameter can be customized to container service (i.e., Docker)'s host machine.

## Running via [Docker](https://www.docker.com/)

An external wrapper library around BEAM evaluates submissions via a set of [Docker](https://www.docker.com/) images that are currently on [Docker Hub](https://hub.docker.com/). 

A python utility, `competition_executor.py` is available in `/utilities` to simplify the interface to `docker`.

## Requirements

**Software requirements**:

For execution:
- [Docker](https://www.docker.com) <sup id="a1">[1](#f1)</sup>.


### Running a Simulation Locally

For the first round, we expect you will be running containers locally.

To run the simulation with default parameters, simply open a terminal in the root directory of this folder and run the following command:

**Note to Windows users**: you will need to execute the following command from PowerShell to initiate a run.

`docker-compose up`

The console should provide an indication of simulation progress and then print a submission score. By default, [output data](Understanding_the_outputs_and_the%20scoring_function.md) is written to the folder `output/<scenario_name>/<scenario_name>-<sample_size>__<execution_date>` The values in angle brackets (`<x>`) are automatically generated according to the parameters of the simulation (described below).

**Important**: After a simulation run executed using `docker-compose up` completes, please issue the command `docker-compose down` in order to remove the running container. Unfortunately, the container does not remove itself automatically.

#### Modifying Simulation Parameter Values

The `docker-compose.yml` file specifies several important configuration parameters used to initialize the simulation. The file is written using [YAML](https://yaml.org/spec/1.2/spec.html), so the terms below will follow the YAML specification. Below a key indicating the version of the docker compose file domain-specific language (DSL), there is a `services` heading beneath which there are two keys defined on the same indent level in the `docker-compose` file: `python` and `scala`. These keys reference the two containers that will be run over the course of this simulation. Each `service` is structured similarly, with identical configuration keys such as `image:`, `entrypoint:`, and `volumes:` followed by one or more parameters values (see the [docker compose file documentation](https://docs.docker.com/compose/compose-file/) for a more thorough explanation about the syntax of this file). Multiple parameter values are indicated using a `-` and typeset indented on separate lines. In this section, we will focus solely on the parameter values defined under `scala` service.

**Setting Simulation Execution Parameter Values:**

Under the `entrypoint` heading of the `scala` service in the `docker-compose` file, you will see a list of entries defining the command-line argument _keys_ and their _values_ for the main method of the simulation (the first line after `entrypoint`). Currently, to run a simulation, you must minimally define the scenario name (`--scenario`, must be "sioux_faux" for Round 1), the sample size (`--sample_size`, one of {"1k" or "15k" to execute a 1,000 agent or 15,000 agent run representing a 1% and 15% sample of the total Sioux Faux population, respectively), and the number of iterations that the simulation should run for (`--iters`, the meaning of this parameter as well as tips on how to set it are presented in . run the simulation users need to specify the submission folder and output folder in the [background on the simulation engine, BEAM](Introduction_transportation_problem.md)). Change the value of the inputs by changing the value of the parameters below the key. For example, specify a 15,000 agent simulation by changing the entry below `--sample_size` from `"1k"` to `"15k"` or run the simulation for 20 iterations by changing the entry below `--iters` from the default of `"1"` to `"20"`.

**Setting Input and Output Directories:**

The other pertinent definitions in the `scala` service `docker-compose` may be found under the `volumes` heading. This section maps directories on the host machine (i.e., your PC if running locally) to directories within the docker container in the form `<host_path>:<container_path>`. You may set `<host_path>` for the input and output directories (currently designated `./submission-inputs` and `./output`), although you **must** leave the `<container_path>` as is.

### Updating the Starter Kit

In order to expedite bug support, we may periodically push new Docker images to DockerHub as well as update this 
repository. Whenever such an update is announced, please run `git pull` in this directory (you might wish to move `/submission-inputs/`) and update execution paths appropriately. Please also run `docker pull beammodel/beam-competition:0.0.1-SNAPSHOT` and `docker pull beammodel/beam-competition:accessibility-0.0.1` to ensure the pertinent images are up-to-date as well.

<!--TODO: Is docker pull really necessary?-->

<b id="f1">1</b> See [www.get.docker.com](http://get.docker.com) for an automated Linux installation. [↩](#a1)

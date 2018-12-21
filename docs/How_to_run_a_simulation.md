# How to run a simulation?

## Requirements

*Software Requirements*:

There is only one firm software requirement at the moment:
- [Docker](https://www.docker.com)

You can find the instructions to install Docker for Mac [here](https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac) and for Windows [here](https://docs.docker.com/docker-for-windows/install/)

Thus, the code is OS-agnostic.

Note that some of the provided utility scripts require a python installation with the [docker-py](https://docker-py.readthedocs.io/en/stable/) installed. Please run `pip install docker` prior to running the scripts.

*Hardware Requirements*:

There are no strict hardware requirements; however,
performance will increase substantially with more CPUs (as well as, to some extent, more memory). At a bare minimum, we recommend 8GB RAM and 2 CPUs. Initial observations for the 1k sample on the minimum hardware clock in at ~24s/iteration. On a more powerful machine with 12 CPUs We provide some parameter settings on the `docker run` entrypoint below so that this parameter can be customized to container service (i.e., Docker)'s host machine.

## Running via [Docker](https://www.docker.com/)

An external wrapper library around BEAM evaluates submissions via a [Docker](https://www.docker.com/) image that is currently on [Docker Hub](https://hub.docker.com/). 

A python utility, `competition_executor.py` is available in `/utilities` to simplify the interface to `docker`. 

## Requirements

**Software requirements**:

For execution:
- [Docker](https://www.docker.com) <sup id="a1">[1](#f1)</sup>.

**Hardware requirements**:

### Running a Container Locally

For the first round, we expect you will be running containers locally.

**Note to Windows users**: you will need to execute the following from PowerShell.


`docker run -it --memory=4g --cpus=2  -v <absolute_path_to_submission_inputs>:/submission-inputs:ro -v <path_to_output_root>:/output:rw beammodel/beam-competition:0.0.1-SNAPSHOT --config /fixed-data/siouxfalls/siouxfalls-1k.conf`

To run the container users need to specify the submission folder and output folder and then run the following command (subsititute <x> as appropriate, keeping in mind that there are sample submission inputs in the root of this repo i.e., `/submission-inputs`). For example, you may run

`docker run -v C:\Users\sidfe\current_code\scala\BeamCompetitions\submission-inputs\:/submission-inputs:ro -v C:\Users\sidfe\current_code\scala\BeamCompetitions\output\:/output:rw beammodel/beam-competition:0.0.1-SNAPSHOT --scenario siouxfalls --sample-size 1k --iters 10`

to execute the 1k Sioux Faux scenario for 10 iterations (this would be for a Windows user in PowerShell--Mac/Linux users can just switch slash directions).

_Note_: To those unfamiliar with the `docker run` command, `-v` binds a local volume (the `.../submission-input` directory, say) to a volume inside the container, which is what follows the `:` (e.g., `/submission-input`). The `ro` or `rw` flags indicate if the directory is to be bound as read-only or write-only, respectively.

If desired, users may pass Java Virtual Machine (JVM) attributes and add JAVA_OPTS `env` arguments to the `docker run` command. For example,
`docker run -it --memory=4g --cpus=2 -v <absolute_path_to_submission_inputs>:/submission-inputs:ro -v <path_to_output_root>/output:/output:rw -e JAVA_OPTS='"-Xmx4g" "-Xms2g"' beammodel/beam-competition:0.0.1-SNAPSHOT --scenario siouxfalls --sample-size 1k --iters 10`

sets the memory used by docker instance to 4 GB and uses 2 cpus. BEAM, in fact, uses _ncpu_-1 for each run, where _ncpu_ is the number of CPUs available on the host machine (virtual or otherwise). While this is sensible for a single run on
one machine, it is not very useful for multiple runs (one CPU is left alone in order to avoid freezing the system).


### Shell Script (Linux/Mac only)

For convenience, the `docker run` command is wrapped by a bash script, `competition.sh`.

To run the script, users enter `./competition.sh -m 4g -c 2 -s siouxfalls -sz 15k -n 10 -i <absolute_path_to_submission-inputs>`, where

* `-m` is the memory limit
* `-c` is the number of CPUs
* `-s` is the scenario name
* `-sz` is the sample size
* `-n` is the number of BEAM iterations
* `-i` is the input folder path

_Reminder_: Substitute `<path_to_submission-inputs>` as appropriate.

### Updating the Starter Kit

In order to expedite bug support, we may periodically push new Docker images to DockerHub as well as update this 
repository. Whenever such an update is announced, please run `git pull` in this directory (you might wish to move `/submission-inputs/`) and update execution paths appropriately. Please also run `docker pull beammodel/beam-competition:0.0.1-SNAPSHOT` to ensure the image is up-to-date as well.

<!--TODO: Is docker pull really necessary?-->

<b id="f1">1</b> See [www.get.docker.com](http://get.docker.com) for an automated Linux installation. [↩](#a1)

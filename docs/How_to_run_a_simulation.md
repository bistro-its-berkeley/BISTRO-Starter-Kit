# How to Run a `BISTRO` Simulation?

## 1. Requirements

### 1.1. Software Requirements

* There is only one firm software requirement at the moment:
[Docker](https://www.docker.com).

You can find the instructions to install Docker **for Mac** [here](https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac) and **for Windows** [here](https://docs.docker.com/docker-for-windows/install/). <br>
      * Note that for Windows, the *Windows 10 64bit: Pro, Enterprise or Education* (1607 Anniversary Update, Build 14393 or later) version must be installed. <br>
      * See [www.get.docker.com](http://get.docker.com) for an automated Linux installation.

Thus, the code is OS-agnostic.

* Note that some of the provided utility scripts require a python installation with the [docker-py](https://docker-py.readthedocs.io/en/stable/) package installed as well as some other [requirements](/requirements.txt). Please run `pip install docker` and `docker login` prior to running the scripts.

```bash
$ pip install -r requirements.txt
$ pip install docker
$ docker login
```

### 1.2. Hardware Requirements and Performance Considerations

There are no strict hardware requirements; however, performance will increase substantially with more CPUs (as well as, to some extent, more memory). At a bare minimum, we recommend 8GB RAM and 4 CPUs. Initial observations for the 15k sample on the minimum hardware clock in at ~49s/iteration. We recommend use of **computers** or **Amazon EC2 instances** with at least **8 CPUs** and at least **32 GB of RAM**.

## 2. Running the Simulation

For your convenience, we've provided several interfaces to running simulations.

### 2.1. Running Using Python API
A python utility, [`competition_executor.py`](/utilities/competition_executor.py) is available in the [`utilities`](/utilities) folder to simplify the interface to docker. See the accompanying ["BISTRO Starter-Kit Simulation Tutorial" Jupyter notebook](examples/BISTRO_Starter-Kit_Simulation_Tutorial.ipynb) for instructions on its use, recommended for first time users to try out the essential features of BISTRO and Beam.

### 2.2. Running a Container From the Command Line

This section explains how to run simulations directly from the command line using docker's `run` command.

To run a container based on the image containing the BISTRO framework, users need to specify the **submission folder** and **output folder** and then run the following command (subsititute <x> as appropriate, keeping in mind that there are sample submission inputs in the root of this repo i.e., `/submission-inputs`). For example, you may run

```bash
$ docker run -v <absolute_path_to_submission_inputs>:/submission-inputs:ro -v <path_to_output_root>:/output:rw beammodel/beam-competition:0.0.3-noacc-SNAPSHOT --scenario sioux_faux --sample-size 15k --iters 10
```

to execute the 15k Sioux Faux scenario for 10 iterations.

***Note***: To those unfamiliar with the `docker run` command:
* The `-v` flag binds a local volume (the `.../submission-input` directory, say) to a volume inside the container, which is what follows the `:` (e.g., `/submission-input`);
* The `ro` or `rw` flags indicate if the directory is to be bound as read-only or write-only, respectively.

If desired, users may pass **Java Virtual Machine (JVM) attributes** and add JAVA_OPTS `env` arguments to the `docker run` command. For example:

```bash
$ docker run -it --memory=4g --cpus=2 -v <absolute_path_to_submission_inputs>:/submission-inputs:ro -v <path_to_output_root>/output:/output:rw -e JAVA_OPTS='"-Xmx4g" "-Xms2g"' beammodel/beam-competition:0.0.3-noacc-SNAPSHOT --scenario sioux_faux --sample-size 15k --iters 10
```

sets the memory used by docker instance to 4 GB and uses 2 cpus. BISTRO, in fact, uses _ncpu_-1 for each run, where _ncpu_ is the number of CPUs available on the host machine (virtual or otherwise). While this is sensible for a single run on
one machine, it is not very useful for multiple runs (one CPU is left to run background processes in order to avoid freezing the system).

### 2.3. Shell Script (Linux/Mac only)

For convenience, **the `docker run` command is wrapped by a bash script, `competition.sh`**.

To run the script, users may enter, for example:

```bash
$ ./competition.sh -m 4g -c 2 -s sioux_faux -sz 15k -n 10 -i <absolute_path_to_submission-inputs>
```

, where

* `-m` is the memory limit
* `-c` is the number of CPUs
* `-s` is the scenario name
* `-sz` is the sample size
* `-n` is the number of BEAM iterations
* `-i` is the input folder path

_Reminder_: Substitute `<path_to_submission-inputs>` as appropriate.

An example run with existing data can be run like so:

```bash
$ ./competition.sh -m 4g -c 2 -s sioux_faux -sz 1k -n 1 -i ../submission-inputs/
```

***Note:*** When you run the simulation again via the **competition script**, you will have to manually delete the container created via the previous `./competition.sh` run. You can do so with `sudo docker rm <container id>`, after looking up the `<container id>` via `sudo docker ps | grep beam-competition`, since docker requires unique container id for each run. 


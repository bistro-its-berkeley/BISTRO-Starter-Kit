# How to run a simulation?


## Running via [Docker](https://www.docker.com/)

A wrapper library around BEAM, `BEAMCompetition` evaluates submissions via a [Docker](https://www.docker.com/) image that is currently on [Docker Hub](https://hub.docker.com/) with tag `beammodel/beam-competition:0.0.1-SNAPSHOT`.

### Running a Container Locally

For the first round, we expect you will be running containers locally.

**Note to Windows users**: you will need to execute the following from PowerShell.

To run the container users need to specify the submission folder and output folder and then run the following command (subsititute <x> as appropriate, keeping in mind that there are sample submission inputs in the root of this repo (`/submission-inputs`)):
`docker run -it --memory=4g --cpus=2  -v <path_to_submission_inputs>/submission-inputs:/submission-inputs:ro -v <path_to_output_root>/output:/output:rw beammodel/beam-competition:0.0.1-SNAPSHOT --config /fixed-data/siouxfalls/siouxfalls-1k.conf`

If desired, users may pass Java Virtual Machine (JVM) attributes and add JAVA_OPTS `env` arguments to the `docker run` command:
`docker run -it --memory=4g --cpus=2 -v <path_to_submission_inputs>:/submission-inputs:ro -v <path_to_output_root>/output:/output:rw -e JAVA_OPTS='"-Xmx4g" "-Xms2g"' beammodel/beam-competition:0.0.1-SNAPSHOT --config /fixed-data/siouxfalls/siouxfalls-1k.conf`

As an alternative to the config file, you may specify the scenario name with flag `--scenario` or `-s` (`siouxfalls` only, for now), the sample size using flag `--sample-size` or `-sz` (either `1k` or `15k` for the two Sioux Faux scenarios for now), and the number of BEAM iterations `--iters` or `n` (an integer number 0 or greater). For example, in a Windows environment on PowerShell (Linux/Mac users just change the direction of directory slashes), you could run:

`docker run -v C:\Users\sidfe\current_code\scala\BeamCompetitions\submission-inputs\:/submission-inputs:ro -v C:\Users\sidfe\current_code\scala\BeamCompetitions\output\:/output:rw beammodel/beam-competition:0.0.1-SNAPSHOT --scenario siouxfalls --sample-size 1k --iters 10`

to execute the 1k Sioux Faux scenario for 10 iterations.

### Shell Script (Linux/Mac only)

For convenience, the `docker run` command is wrapped by a bash script, `competition.sh`.

To run the script, users enter `./competition.sh -m 4g -c 2 -s siouxfalls -sz 15k -i -n 10 "$(pwd)"/submission-inputs/`, where

* `-m` is the memory limit
* `-c` is the number of CPUs
* `-s` is the scenario name
* `-sz` is the sample size
* `-n` is the number of BEAM iterations
* `-i` is the input folder path


<b id="f1">1</b> See [www.get.docker.com](http://get.docker.com) for an automated Linux installation. [↩](#a1)

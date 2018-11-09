# How to run a simulation?

## Installing BEAM

Clone the following GitHub repository in your GitHub Desktop:
https://github.com/sfwatergit/BeamCompetitions

After you unzip the archive, you will see a directory that looks like this when partially expanded:

![Competition Repository](https://github.com/vgolfier/Uber-Prize-Starter-Kit-/blob/master/Images/CompetitionRepository.png "Competition Repository")

***Figure 1: Competition Repository***

## Running a simulation

### [Docker](https://www.docker.com/) Container Management and Execution

The wrapper around `BeamCompetitions` has a Docker image on [Docker Hub](https://hub.docker.com/) with tag `beammodel/beam-competition:0.0.1-SNAPSHOT`.

This section details how administrators can manage and execute this image via the Docker toolkit.


### Running a Container

Once built and pushed, the container is ready to be executed by the competitors.

To run the container users need to specify the submission folder and output folder and then run the following command:
` docker run -it --memory=4g --cpus=2  -v "$(pwd)"/submission-inputs:/submission-inputs:ro -v "$(pwd)"/output:/output:rw beammodel/beam-competition:0.0.1-SNAPSHOT --config /fixed-data/siouxfalls/siouxfalls-1k.conf`

If desired, users may pass Java Virtual Machine (JVM) attributes and add JAVA_OPTS `env` arguments to the `docker run` command:
`docker run -it --memory=4g --cpus=2  -v "$(pwd)"/submission-inputs:/submission-inputs:ro -v "$(pwd)"/output:/output:rw -e JAVA_OPTS='"-Xmx4g" "-Xms2g"' beammodel/beam-competition:0.0.1-SNAPSHOT --config /fixed-data/siouxfalls/siouxfalls-1k.conf`

### Shell Script

For convenience, the `docker run` command is wrapped by a bash script, `competition.sh`.

To run it, users enter `./competition.sh -m 4g -c 2 -s siouxfalls -sz 15k -i "$(pwd)"/submission-inputs/`, where

* `-m` is the memory limit
* `-c` is the number of cpus
* `-s` is the scenario name
* `-sz` is the sample size
* `-i` is the input folder path.

<b id="f1">1</b> See [www.get.docker.com](http://get.docker.com) for an automated Linux installation. [↩](#a1)

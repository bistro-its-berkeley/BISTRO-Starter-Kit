# How to run a simulation?


## Running via [Docker](https://www.docker.com/)

A wrapper library around BEAM, `BEAMCompetition` evaluates submissions via a [Docker](https://www.docker.com/) image that is currently on [Docker Hub](https://hub.docker.com/) with tag `beammodel/beam-competition:0.0.1-SNAPSHOT`.

### Running a Container Locally

For the first round, we expect users will be running containers locally.

To run the `beam-competition` container and evaluate your inputs, you will want to specify paths to the submission folder (which should be named `submission-inputs`) and
output folder (named `output`) using the following command:
` docker run -it --memory=4g --cpus=2  -v "$(pwd)"/submission-inputs:/submission-inputs:ro -v "$(pwd)"/output:/output:rw beammodel/beam-competition:0.0.1-SNAPSHOT --config /fixed-data/siouxfalls/siouxfalls-1k.conf`

If desired, users may pass Java Virtual Machine (JVM) attributes and add JAVA_OPTS `env` arguments to the `docker run` command:
`docker run -it --memory=4g --cpus=2  -v "$(pwd)"/submission-inputs:/submission-inputs:ro -v "$(pwd)"/output:/output:rw -e JAVA_OPTS='"-Xmx4g" "-Xms2g"' beammodel/beam-competition:0.0.1-SNAPSHOT --config /fixed-data/siouxfalls/siouxfalls-1k.conf`

### Shell Script

For convenience, the `docker run` command is wrapped by a bash script, which may be found in `./competition.sh`.

To run it, users enter `./competition.sh -m 4g -c 2 -s siouxfalls -sz 15k -i "$(pwd)"/submission-inputs/`, where

* `-m` is the memory limit
* `-c` is the number of cpus
* `-s` is the scenario name
* `-sz` is the sample size
* `-i` is the input folder path.

<b id="f1">1</b> See [www.get.docker.com](http://get.docker.com) for an automated Linux installation. [↩](#a1)

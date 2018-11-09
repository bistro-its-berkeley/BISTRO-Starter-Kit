#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -s|--scenario)
    SCENARIO="$2"
    shift # past argument
    shift # past value
    ;;
    -sz|--size)
    SIZE="$2"
    shift # past argument
    shift # past value
    ;;
    -m|--memory)
    MEMORY="$2"
    shift # past argument
    shift # past value
    ;;
    -c|--cpus)
    CPUS="$2"
    shift # past argument
    shift # past value
    ;;
    -i|--input)
    INPUT="$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

echo INPUT = "${INPUT}"

for image in $(docker volume ls | awk -F' +' '{print $2}') ; do
    if [ ${image} == "competition-output" ]; then
        echo "Volume already exist"
    fi
done

if [ -z $(docker volume ls | awk -F' +' '{print $2}' | grep "competition-output") ]; then
    docker volume create competition-output >> /dev/null
fi

docker run -it --memory="${MEMORY}" --cpus="${CPUS}"  -v "${INPUT}":/submission-inputs:ro -v $PWD/output:/output:rw beammodel/beam-competition:0.0.1-SNAPSHOT --scenario "${SCENARIO}" --sample-size "${SIZE}"

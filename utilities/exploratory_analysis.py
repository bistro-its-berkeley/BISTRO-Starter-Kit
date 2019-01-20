import logging
import os
import tempfile
from pathlib import Path

import docker
import numpy as np
import pandas as pd
import sys

import input_sampler as sampler
from cost_mapping_fixed_inputs import input_combinations

AGENCY = "sioux_faux_bus_lines"
SCENARIO_NAME = "sioux_faux"
DOCKER_IMAGE = "beammodel/beam-competition:0.0.1-SNAPSHOT"

CMD_TEMPLATE = "--scenario {0} --sample-size {1} --iters {2}"
DIR_DELIM = "-"

FREQ_FILE = "FrequencyAdjustment.csv"
SUB_FILE = "ModeIncentives.csv"
FLEET_FILE = "VehicleFleetMix.csv"
PT_FARE_FILE = "PtFares.csv"
SCORES_PATH = ("competition", "submissionScores.csv")

logger = logging.getLogger(__name__)


def abspath2(path):
    path = os.path.abspath(os.path.expanduser(path))  # expanduser() expands "~" into "/Users/username"
    return path


def only_subdir(path):
    subdir = os.listdir(path)[0]  # Validates only returned element
    path = os.path.join(path, subdir)
    return path


def docker_exists(container_id, client):
    try:
        client.containers.get(container_id)
    except docker.errors.NotFound:
        return False
    return True


def sample_settings(data_root, combination_number):
    max_bus_lines = 12
    max_num_records = 24
    # TODO pull out data GTFS stuff to make this pure function
    agency_dict = sampler.scenario_agencies(Path(data_root), SCENARIO_NAME)
    sf_gtfs_manager = sampler.AgencyGtfsDataManager(agency_dict[AGENCY])

    subsidies_combination, pt_fares_combination = input_combinations[combination_number]

    samples = [sampler.sample_frequency_adjustment_input(np.random.randint(0, max_num_records), sf_gtfs_manager),
               subsidies_combination,
               sampler.sample_vehicle_fleet_mix_input(np.random.randint(0, max_bus_lines), sf_gtfs_manager,
                                                      ["BUS-SMALL-HD", "BUS-STD-ART", "BUS-DEFAULT"]),
               pt_fares_combination]

    return tuple(samples)


def save_inputs(input_dir, freq_df=None, mode_subsidy_df=None, vehicle_fleet_mix_df=None, pt_fare_df=None):
    if freq_df is not None:
        freq_df.to_csv(os.path.join(input_dir, FREQ_FILE), header=True, index=False)
    if mode_subsidy_df is not None:
        mode_subsidy_df.to_csv(os.path.join(input_dir, SUB_FILE), header=True, index=False)
    if vehicle_fleet_mix_df is not None:
        vehicle_fleet_mix_df.to_csv(os.path.join(input_dir, FLEET_FILE), header=True, index=False)
    if pt_fare_df is None:
        pt_fare_df = pd.read_csv('../submission-inputs/{0}'.format(PT_FARE_FILE))
    pt_fare_df.to_csv(os.path.join(input_dir, PT_FARE_FILE), header=True, index=False)


def read_scores(output_dir):
    """Read scores from output directory as .csv file.
    """
    output_dir = only_subdir(only_subdir(output_dir))
    df = pd.read_csv(os.path.join(output_dir, *SCORES_PATH), index_col="Component Name")
    scores = df["Weighted Score"]
    return scores


def search_iteration(docker_cmd, data_root, input_root, output_root, combination_number, random_sample_number):
    client = docker.from_env()  # TODO consider if cleanest that this is in main?

    assert os.path.isabs(data_root)
    assert os.path.isabs(input_root)
    assert os.path.isabs(output_root)

    # Make temp dirs, race condition safe too
    input_dir = tempfile.mkdtemp(prefix="input_C{0}_RS{1}".format(combination_number +1, random_sample_number+1) + DIR_DELIM, dir=input_root)
    output_dir = tempfile.mkdtemp(prefix="output_C{0}_RS{1}".format(combination_number +1, random_sample_number+1) + DIR_DELIM, dir=output_root)

    # Should be unique name here since folder is unique, also checks only one instance of delim
    _, submission_name = os.path.basename(input_dir).split(DIR_DELIM)
    # Add 'bm_bc_' prefix due to docker's restriction on container names
    submission_name = "bm_bc_{}".format(submission_name)
    # Call random input sampler
    settings = sample_settings(data_root, combination_number)
    # Save all inputs
    save_inputs(input_dir, *settings)

    docker_dirs = {output_dir: {"bind": "/output", "mode": "rw"},
                   input_dir: {"bind": "/submission-inputs",
                                                             "mode": "ro"}}

    assert not docker_exists(submission_name, client)
    logger.info('%s start' % submission_name)
    logs = client.containers.run(DOCKER_IMAGE, command=docker_cmd, auto_remove=True, detach=False,
                                 name=submission_name, volumes=docker_dirs,
                                 stdout=True, stderr=True)

    logger.debug(logs)
    logger.info('%s end' % submission_name)

    paths = (input_dir, output_dir)
    return paths

def random_search(docker_cmd, n_iters, data_root, input_root, output_root, combination_number):
    for _ in range(n_iters):
        paths = search_iteration(docker_cmd, data_root, input_root, output_root, combination_number, _)
        logger.info("Iteration Number %s / %s" % (_ + 1, n_iters))

def main(combination_number, name_of_exploration):
    logging.basicConfig(level=logging.INFO)

    # TODO explain why this is different than SCENARIO_NAME

    # We can take these from cmd args later:
    sample_size = "15k"
    n_sim_iters = 20
    seed = 123

    n_search_iters = 100
    data_root = abspath2("../reference-data")
    input_root = abspath2("../search-input")
    output_root = abspath2("../search-output-%s"%name_of_exploration)

    os.makedirs(input_root, exist_ok=True)
    os.makedirs(output_root, exist_ok=True)

    # TODO also consider setting pyseed
    np.random.seed(seed)

    # Some prints
    docker_cmd = CMD_TEMPLATE.format(SCENARIO_NAME, sample_size, n_sim_iters)
    random_search(docker_cmd, n_search_iters, data_root, input_root, output_root, combination_number)

if __name__ == "__main__":
    combination_number = int(sys.argv[1])
    name_of_exploration = sys.argv[2]
    main(combination_number, name_of_exploration)

import logging
import os
import tempfile
from pathlib import Path
from os import path

import docker
import numpy as np
import pandas as pd
import sys
from glob import glob

import input_sampler as sampler
from cost_mapping_fixed_inputs import input_combinations
from exploratory_analysis_unittests_inputs import gather_fare_inputs, change_amount_transit_subsidies, \
                                                         change_amount_ride_hail_subsidies,\
                                                         change_vehicle_fleet_mix, change_headway_for_all_bus_routes_all_day, \
                                                         fares, transit_incentives, on_demand_incentives, \
                                                         headways


AGENCY = "sioux_faux_bus_lines"
SCENARIO_NAME = "sioux_faux"
DOCKER_IMAGE = "beammodel/beam-competition:0.0.1-SNAPSHOT"

CMD_TEMPLATE = "--scenario {0} --sample-size {1} --iters {2}"
DIR_DELIM = "-"

FREQ_FILE = "FrequencyAdjustment.csv"
SUB_FILE = "ModeIncentives.csv"
FLEET_FILE = "VehicleFleetMix.csv"
MASS_TRANSIT_FARE_FILE = "MassTransitFares.csv"
SCORES_PATH = ("competition", "submissionScores.csv")

# List the output folders names corresponding to the unit tests fixed inputs
bau_fares = ["{0}_bau".format(fare) for fare in fares] + ["bau_{0}".format(fare) for fare in fares]
other_fares = ["{0}_{1}".format(young_seniors_fare, adults_fare) for adults_fare in fares for young_seniors_fare in fares]
changes_fares = bau_fares + other_fares

changes_on_demand_incentives = ["{0}_{1}_{2}".format(low_income, medium_income, high_income)
           for medium_income in on_demand_incentives
           for high_income in on_demand_incentives
           for low_income in on_demand_incentives
           ]

changes_transit_incentives = ["{0}_{1}_{2}".format(low_income, medium_income, high_income)
           for medium_income in transit_incentives
           for high_income in transit_incentives
           for low_income in transit_incentives
           ]

bus_types = ["BUS_SMALL_HD", "BUS_STD_ART"]
changes_fleet_mix = ["{0}".format(bus) for bus in bus_types]

changes_frequency_adjustment = ["{0}".format(headway) for headway in headways]



##################

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


def sample_settings(data_root, combination_number, input_mode):
    max_bus_lines = 12
    max_num_records_frequency = 36
    max_num_records = 10

    # TODO pull out data GTFS stuff to make this pure function
    agency_dict = sampler.scenario_agencies(Path(data_root), SCENARIO_NAME)
    sf_gtfs_manager = sampler.AgencyGtfsDataManager(agency_dict[AGENCY])

    if input_mode == "random_inputs":
        samples = [sampler.sample_frequency_adjustment_input(np.random.randint(0, max_num_records_frequency), sf_gtfs_manager),
                   sampler.sample_mode_subsidies_input(np.random.randint(0, max_num_records), sf_gtfs_manager),
                   sampler.sample_vehicle_fleet_mix_input(np.random.randint(0, max_bus_lines), sf_gtfs_manager),
                   sampler.sample_mass_transit_fares_input(max_num_records, sf_gtfs_manager, max_fare_amount=10.0)]

    elif input_mode == "fixed_inputs":
        subsidies_combination, mass_transit_fares_combination = input_combinations[combination_number]

        samples = [sampler.sample_frequency_adjustment_input(np.random.randint(0, max_num_records), sf_gtfs_manager),
                   subsidies_combination,
                   sampler.sample_vehicle_fleet_mix_input(np.random.randint(0, max_bus_lines), sf_gtfs_manager,
                                                          ["BUS-SMALL-HD", "BUS-STD-ART", "BUS-DEFAULT"]),
                   mass_transit_fares_combination]

    elif input_mode == "unit_tests_inputs":
        if combination_number + 1 == 1:
            return gather_fare_inputs()

        elif combination_number + 1 == 2:
            return change_amount_ride_hail_subsidies()[:int(len(change_amount_ride_hail_subsidies())/2)]

        elif combination_number + 1 == 3:
            return change_amount_ride_hail_subsidies()[int(len(change_amount_ride_hail_subsidies())/2):int(len(change_amount_ride_hail_subsidies()))]

        elif combination_number + 1 == 4:
            return change_amount_transit_subsidies()[:int(len(change_amount_transit_subsidies())/2)]

        elif combination_number + 1 == 5:
            return change_amount_transit_subsidies()[int(len(changes_transit_incentives) / 2):len(changes_transit_incentives)]

        elif combination_number + 1 == 6:
            return change_vehicle_fleet_mix()

        elif combination_number + 1 == 7:
            return change_headway_for_all_bus_routes_all_day()

    return tuple(samples)


def save_inputs(input_dir, freq_df=None, mode_subsidy_df=None, vehicle_fleet_mix_df=None, mass_transit_fare_df=None):
    if freq_df is not None:
        freq_df.to_csv(os.path.join(input_dir, FREQ_FILE), header=True, index=False)
    if mode_subsidy_df is not None:
        mode_subsidy_df.to_csv(os.path.join(input_dir, SUB_FILE), header=True, index=False)
    if vehicle_fleet_mix_df is not None:
        vehicle_fleet_mix_df.to_csv(os.path.join(input_dir, FLEET_FILE), header=True, index=False)
    if mass_transit_fare_df is None:
        mass_transit_fare_df = pd.read_csv('../submission-inputs/{0}'.format(MASS_TRANSIT_FARE_FILE))
    mass_transit_fare_df.to_csv(os.path.join(input_dir, MASS_TRANSIT_FARE_FILE), header=True, index=False)


def save_input_dict(input_dictionary, input_root):

    list_inputs = ["VehicleFleetMix", "ModeIncentives", "FrequencyAdjustment", "MassTransitFares"]

    for input_name, input_dataframe in input_dictionary.items():
        if input_name not in list_inputs:
            raise KeyError("{0} is not a valid key for `input_dictionary`.".format(input_name))

        input_dataframe.to_csv(path.join(input_root, input_name +".csv"), index=False)


def read_scores(output_dir):
    """Read scores from output directory as .csv file.
    """
    output_dir = only_subdir(only_subdir(output_dir))
    df = pd.read_csv(os.path.join(output_dir, *SCORES_PATH), index_col="Component Name")
    scores = df["Weighted Score"]
    return scores


def search_iteration(docker_cmd, data_root, input_root, output_root, combination_number, random_sample_number, input_mode):
    client = docker.from_env()  # TODO consider if cleanest that this is in main?

    assert os.path.isabs(data_root)
    assert os.path.isabs(input_root)
    assert os.path.isabs(output_root)

    # Make temp dirs, race condition safe too
    if input_mode == "fixed_inputs":
        input_dir = tempfile.mkdtemp(prefix="input_C{0}_RS{1}".format(combination_number +1, random_sample_number+1) + DIR_DELIM, dir=input_root)
        output_dir = tempfile.mkdtemp(prefix="output_C{0}_RS{1}".format(combination_number +1, random_sample_number+1) + DIR_DELIM, dir=output_root)

    elif input_mode == "random_inputs":
        input_dir = tempfile.mkdtemp(prefix="input_C9_RS{0}".format(random_sample_number + 1) + DIR_DELIM, dir=input_root)
        output_dir = tempfile.mkdtemp(prefix="output_C9_RS{0}".format(random_sample_number + 1) + DIR_DELIM, dir=output_root)

    elif input_mode == "unit_tests_inputs":
        if combination_number + 1 == 1:
            # name of the input which varies
            changed_input = "fare"
            # values of this input
            changes = changes_fares

        elif combination_number + 1 == 2:
            # name of the input which varies
            changed_input = "on_demand_incentive"
            # values of this input
            changes = changes_on_demand_incentives[0:int(len(changes_on_demand_incentives)/2)]

        elif combination_number + 1 == 3:
            # name of the input which varies
            changed_input = "on_demand_incentive"
            # values of this input
            changes = changes_on_demand_incentives[int(len(changes_on_demand_incentives)/2):int(len(changes_on_demand_incentives))]

        elif combination_number + 1 == 4:
            # name of the input which varies
            changed_input = "transit_incentive"
            # values of this input
            changes = changes_transit_incentives[0:int(len(changes_transit_incentives)/2)]

        elif combination_number + 1 == 5:
            # name of the input which varies
            changed_input = "transit_incentive"
            # values of this input
            changes = changes_transit_incentives[int(len(changes_transit_incentives)/2):int(len(changes_transit_incentives))]

        elif combination_number + 1 == 6:
            # name of the input which varies
            changed_input = "fleet_mix"
            # values of this input
            changes = changes_fleet_mix

        elif combination_number + 1 == 7:
            # name of the input which varies
            changed_input = "frequency_adjustment"
            # values of this input
            changes = changes_frequency_adjustment

        input_dir = tempfile.mkdtemp(prefix="input_{0}_{1}".format(changed_input, changes[random_sample_number]) + DIR_DELIM, dir=input_root)
        output_dir = tempfile.mkdtemp(prefix="output_{0}_{1}".format(changed_input, changes[random_sample_number]) + DIR_DELIM, dir=output_root)

    # Should be unique name here since folder is unique, also checks only one instance of delim
    _, submission_name = os.path.basename(input_dir).split(DIR_DELIM)
    # Add 'bm_bc_' prefix due to docker's restriction on container names
    submission_name = "bm_bc_{}".format(submission_name)
    # Call random input sampler
    settings = sample_settings(data_root, combination_number, input_mode)

    # Save all inputs
    if input_mode == "fixed_inputs" or input_mode == "random_inputs":
        save_inputs(input_dir, *settings)

    elif input_mode == "unit_tests_inputs":
        save_input_dict(settings[random_sample_number], input_dir)

    docker_dirs = {output_dir: {"bind": "/output", "mode": "rw"},
                   input_dir: {"bind": "/submission-inputs", "mode": "ro"}}

    assert not docker_exists(submission_name, client)
    logger.info('%s start' % submission_name)
    logs = client.containers.run(DOCKER_IMAGE, command=docker_cmd, auto_remove=True, detach=False,
                                 name=submission_name, volumes=docker_dirs,
                                 stdout=True, stderr=True)

    logger.debug(logs)
    logger.info('%s end' % submission_name)

    paths = (input_dir, output_dir)
    return paths


def random_search(docker_cmd, n_iters, data_root, input_root, output_root, combination_number, input_mode):
    # Finding which simulations already exist:
    subScoreFiles = glob(path.join(output_root, "*", "*", "*", "competition", "submissionScores.csv"))
    if len(subScoreFiles) == 0:
        iterations_left = [i for i in range(n_iters)]
    else:
        iteration = [int(i[i.index("_RS"):i.index("_RS") + 10].split("-")[0].replace("_RS", "")) for i in subScoreFiles]
        iteration = set([x-1 for x in iteration])
        iterations_left = [i for i in range(n_iters) if i not in iteration]

    for i_left in iterations_left:
        for i in range(i_left):
            _ = sample_settings(data_root, combination_number, input_mode)
        paths = search_iteration(docker_cmd, data_root, input_root, output_root, combination_number, i_left, input_mode)
        logger.info("Iteration Number %s / %s" % (i_left + 1, n_iters))


def main(combination_number, name_of_exploration, input_mode):
    logging.basicConfig(level=logging.INFO)

    # TODO explain why this is different than SCENARIO_NAME

    # We can take these from cmd args later:
    sample_size = "15k"
    n_sim_iters = 20 #Number of iterations in Beam for 1 run
    # seed = 123

    if input_mode == "unit_tests_inputs":
        if combination_number + 1 == 1:
            n_search_iters = int(len(changes_fares))

        elif combination_number + 1 == 2 or combination_number + 1 == 3:
            n_search_iters = int(len(changes_on_demand_incentives)/2)

        elif combination_number + 1 == 4 or combination_number + 1 == 5:
            n_search_iters = int(len(changes_transit_incentives)/2)

        elif combination_number + 1 == 6:
            n_search_iters = int(len(changes_fleet_mix))

        elif combination_number + 1 == 7:
            n_search_iters = int(len(changes_frequency_adjustment))

    else:
        n_search_iters = 100 # Number

    data_root = abspath2("../reference-data")
    input_root = abspath2("../search-input-{0}-{1}".format(name_of_exploration, input_mode))
    output_root = abspath2("../search-output-{0}-{1}".format(name_of_exploration, input_mode))

    os.makedirs(input_root, exist_ok=True)
    os.makedirs(output_root, exist_ok=True)

    # # TODO also consider setting pyseed
    # np.random.seed(seed)

    # Some prints
    docker_cmd = CMD_TEMPLATE.format(SCENARIO_NAME, sample_size, n_sim_iters)
    random_search(docker_cmd, n_search_iters, data_root, input_root, output_root, combination_number, input_mode)

if __name__ == "__main__":
    combination_number = int(sys.argv[1])
    name_of_exploration = sys.argv[2]
    input_mode = sys.argv[3]

    main(combination_number, name_of_exploration, input_mode)

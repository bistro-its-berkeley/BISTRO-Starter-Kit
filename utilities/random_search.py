import logging
import os
from pathlib import Path
import tempfile
import docker
import numpy as np
import pandas as pd
import input_sampler as sampler

AGENCY = "sioux_faux_bus_lines"
SCENARIO_NAME = "sioux_faux"
DOCKER_IMAGE = "beammodel/beam-competition:0.0.1-SNAPSHOT"

CMD_TEMPLATE = "--scenario {0} --sample-size {1} --iters {2}"
DIR_DELIM = "-"

FREQ_FILE = "FrequencyAdjustment.csv"
SUB_FILE = "ModeSubsidies.csv"
FLEET_FILE = "VehicleFleetMix.csv"
SCORES_PATH = ("competition", "submissionScores.txt")

logger = logging.getLogger(__name__)


def abspath2(path):
    path = os.path.abspath(os.path.expanduser(path))
    return path


def only_subdir(path):
    subdir, = os.listdir(path)  # Validates only returned element
    path = os.path.join(path, subdir)
    return path


def docker_exists(container_id, client):
    try:
        client.containers.get(container_id)
    except docker.errors.NotFound:
        return False
    return True


def sample_settings(num_records, data_root):
    # TODO pull out data GTFS stuff to make this pure function
    agency_dict = sampler.scenario_agencies(Path(data_root), SCENARIO_NAME)
    sf_gtfs_manager = sampler.AgencyGtfsDataManager(agency_dict[AGENCY])

    freq_df = sampler.sample_frequency_adjustment_input(num_records, sf_gtfs_manager)
    mode_subsidy_df = sampler.sample_mode_subsidies_input(num_records)
    vehicle_fleet_mix_df = sampler.sample_vehicle_fleet_mix_input(num_records, sf_gtfs_manager)

    return freq_df, mode_subsidy_df, vehicle_fleet_mix_df


def save_inputs(input_dir, freq_df, mode_subsidy_df, vehicle_fleet_mix_df):
    freq_df.to_csv(os.path.join(input_dir, FREQ_FILE), header=True, index=False)
    mode_subsidy_df.to_csv(os.path.join(input_dir, SUB_FILE), header=True, index=False)
    vehicle_fleet_mix_df.to_csv(os.path.join(input_dir, FLEET_FILE), header=True, index=False)


def read_scores(output_dir):
    """This function will become much simpler once sim is configured to output std csv file.
    """
    # Need to go two levels deeper in useless nesting:
    output_dir = only_subdir(only_subdir(output_dir))

    with open(os.path.join(output_dir, *SCORES_PATH), "r") as f:
        lines = f.readlines()

        data = []
        for idx, l in enumerate(lines):
            if idx == 0:
                columns = l.rstrip("\n").split("|")
                columns = [i.strip() for i in columns]
                continue
            elif idx == 1:
                continue
            values = l.rstrip("\n").split("|")
            values = [i.strip() for i in values]
            values = [i if len(i) > 0 else "0" for i in values]
            data.append(values)

    df = pd.DataFrame(data, columns=columns)

    scores = []
    for score_type in ["Weight", "Raw Score", "Weighted Score"]:
        pivoted = pd.pivot_table(df, values=score_type, columns="Component Name", aggfunc="first").reset_index(drop=True)
        pivoted.columns = ["%s_%s" % (i, score_type) for i in pivoted.columns]
        scores.append(pivoted)
    scores = pd.concat(scores, 1).astype(float)

    return scores


def search_iteration(docker_cmd, data_root, input_root, output_root):
    num_records = 10  # TODO make this random as well

    client = docker.from_env()  # TODO consider if cleanest that this is in main?

    assert os.path.isabs(data_root)
    assert os.path.isabs(input_root)
    assert os.path.isabs(output_root)

    # Make temp dirs, race condition safe too
    input_dir = tempfile.mkdtemp(prefix="input" + DIR_DELIM, dir=input_root)
    output_dir = tempfile.mkdtemp(prefix="output" + DIR_DELIM, dir=output_root)

    # Should be unique name here since folder is unique, also checks only one instance of delim
    _, submission_name = os.path.basename(input_dir).split(DIR_DELIM)

    # Call random input sampler
    settings = sample_settings(num_records, data_root)
    # Save all inputs
    save_inputs(input_dir, *settings)

    docker_dirs = {input_dir: {"bind": "/submission-inputs", "mode": "ro"},
                   output_dir: {"bind": "/output", "mode": "rw"}}

    assert not docker_exists(submission_name, client)
    logger.info('%s start' % submission_name)
    logs = client.containers.run(DOCKER_IMAGE, command=docker_cmd, auto_remove=True, detach=False,
                                 name=submission_name, volumes=docker_dirs,
                                 stdout=True, stderr=True)
    logger.debug(logs)
    logger.info('%s end' % submission_name)
    assert not docker_exists(submission_name, client)  # Since we auto_removed it

    scores = read_scores(output_dir)
    score, = scores["Submission Score_Weighted Score"]
    score = float(score)  # verify simple float to keep simple

    paths = (input_dir, output_dir)
    return paths, score


def random_search(docker_cmd, n_iters, data_root, input_root, output_root):
    best_score = None
    best_setting = None
    for _ in range(n_iters):
        paths, score = search_iteration(docker_cmd, data_root, input_root, output_root)
        # Appears we are maximizing
        if best_score is None or score > best_score:
            best_score = score
            best_setting = paths

        result_str = 'paths: %s\nscore: %f' % (str(paths), score)
        logger.info(result_str)

    return best_setting, best_score


def main():
    logging.basicConfig(level=logging.INFO)

    # TODO explain why this is different than SCENARIO_NAME
    scenario_name = "siouxfalls"
    # We can take these from cmd args later:
    sample_size = "1k"
    n_sim_iters = 3
    seed = 123

    n_search_iters = 10
    data_root = abspath2("../reference-data")
    input_root = abspath2("../search-input")
    output_root = abspath2("../search-output")

    os.makedirs(input_root, exist_ok=True)
    os.makedirs(output_root, exist_ok=True)

    # TODO also consider setting pyseed
    np.random.seed(seed)

    # Some prints
    docker_cmd = CMD_TEMPLATE.format(scenario_name, sample_size, n_sim_iters)
    (input_dir, output_dir), best_score = random_search(docker_cmd, n_search_iters,
                                                        data_root, input_root, output_root)

    print('Best score: %f' % best_score)
    print('Input: %s' % input_dir)
    print('Output: %s' % output_dir)


if __name__ == "__main__":
    main()

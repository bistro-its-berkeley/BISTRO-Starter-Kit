"""Utility functions to sample random inputs for execution in Uber Prize.

Example
-------
Here's how to generate a sample of 5 records from each of the input samplers:

    {{
    SCENARIO_NAME = 'sioux_faux'

    DIR = Path('..')
    sys.path.append(str(DIR))
    DATA_DIR = DIR / 'reference-data/'

    freq_df = sample_frequency_adjustments(5, SCENARIO_NAME)
    mode_subsidy_df = sample_mode_subsidies(5)
    vehicle_fleet_mix_df = sample_vehicle_fleet_mix(5, SCENARIO_NAME)
    }}

Write each to file using <input_df>.to_csv(<filename>, index=None) if desired.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from . import lazyprop

# TODO:
# clearly document somewhere in repo which convention on doc strings we follow
#   require var name for returns??
# consider making all filenames and dirs global const
# also implement clear validation function for what are valid csvs
#    can be useful for user to know full domain of inputs

# Below are provided for convenience as we expect auxiliary data to remain in
# designated location.
DIR = Path('..')
# TODO best to right code in way that it doesn't require messing with path etc
sys.path.append(str(DIR))
DATA_DIR = DIR / 'reference-data/'


def scenario_agencies(data_dir, scenario_name):
    """Given root data directory and scenario name, computes a mapping
    of agency names to their respective paths.

    Parameters
    ----------
    data_dir : (Path)
        Absolute path to root of data directory
    scenario_name : (str)
        Name of scenario with GTFS data

    Returns
    -------
    (dict)
        Dictionary of agency names mapped to directories containing files comprising their GTFS data.
    """
    gtfs_root = (data_dir / scenario_name).absolute()
    return {p.stem: p for p in
            gtfs_root.iterdir()}


class AgencyGtfsDataManager(object):

    def __init__(self, agency_gtfs_path):
        """Used to cache an agency's GTFS data for sampling purposes

        Parameters
        ----------
        agency_gtfs_path : (Path)
            Directory containing the agency's gtfs data
        """

        self.agency_gtfs_path = agency_gtfs_path

    @lazyprop
    def routes(self):
        return pd.read_csv(self.agency_gtfs_path / "gtfs_data/routes.txt", header=0, index_col=1,
                           na_values=None,
                           delimiter=',')

    @lazyprop
    def vehicle_types(self):
        return pd.read_csv(self.agency_gtfs_path / "availableVehicleTypes.csv", header=0, index_col=0, na_values=None,
                           delimiter=',')

    @lazyprop
    def trips(self):
        return pd.read_csv(self.agency_gtfs_path / "gtfs_data/trips.txt", header=0, index_col=2, na_values=None,
                           delimiter=',')


def sample_vehicle_fleet_mix(num_records, scenario_name):
    """Generate random `VehicleFleetMix` input according to possible substitute
    vehicle trip ids available for each agency.

    Parameters
    ----------
    num_records : (int)
        Number of randomly sampled records to create.
    scenario_name : (str)
        Name of scenario (used for path resolution purposes).

    Returns
    -------
    `pd.DataFrame`
        `num_records` `VehicleFleetMix` records. These are unique by `routeId`
        for each `agencyId`.
    """
    gtfs_root = DATA_DIR / scenario_name
    agencies = gtfs_root.iterdir()

    # TODO pull this section out and accept this dfs as input to this function
    #   ==> allow as many functions to be pure as possible
    route_ids = []
    vehicle_type_ids = []
    agency_ids = []
    # TODO " vs '
    for agency_path in agencies:
        # TODO always be explicit about header, index_col, nan etc
        route_df = pd.read_csv(agency_path / "gtfs_data/routes.txt")
        route_ids.append(route_df.route_id.values.tolist())
        vehicle_df = pd.read_csv(agency_path / "availableVehicleTypes.csv")
        vehicle_type_ids.append(vehicle_df.vehicleTypeId.values.tolist())
        # TODO why [0]
        agency_ids.append(route_df['agency_id'].values[0])

    res = []
    # TODO maybe better to just use choice of product of agency and route_id
    # Then sample vehicle iid for each
    pairs = []  # TODO make a set
    while len(res) < num_records:
        agency_idx = np.random.choice(len(agency_ids))
        # TODO why are last two singleton lists?? why not unbox as int?
        agency_id, route_ids_for_agency_id, vehicle_type_ids_for_agency_id = \
            (agency_ids[agency_idx],
             np.random.choice(route_ids[agency_idx], 1),
             np.random.choice(vehicle_type_ids[agency_idx], 1))
        route_id = np.random.choice(route_ids_for_agency_id)

        if (agency_id, route_id) not in pairs:  # Rejection sampling
            pairs.append((agency_id, route_id))
            vehicle_type_id = np.random.choice(vehicle_type_ids_for_agency_id)
            res.append({'agencyId': agency_id, 'routeId': route_id,
                        'vehicleTypeId': vehicle_type_id})
    return pd.DataFrame(res)


def sample_frequency_adjustments(num_records, scenario_name):
    """Generate random `FrequencyAdjustment` inputs according to trips run by
    an agency.

    Creates `num_records` records where fields for each record where the
    `headway_secs` field is randomly chosen from a range of between 0 and 12000
    seconds at intervals of 60 seconds and the `min_time` and `max_time` field
    are sampled between the 0 and 86340 seconds, respectively (i.e.,
    the possible minimum and maximum number of seconds in a day of 86359
    seconds, given the headway interval).

    Parameters
    ----------
    num_records : (int)
        Number of randomly sampled records to create.
    scenario_name: (str)
        Name of scenario (used for path resolution purposes).

    Returns
    -------
    `pd.DataFrame`
        `num_records` `FrequencyAdjustmentInput` records.
    """
    gtfs_root = DATA_DIR / scenario_name
    agencies = gtfs_root.iterdir()

    # FIXME[saf}: implement for multiple agencies; taking one for now.
    agency_path = list(agencies)[0]
    trips_df = agency_path / 'gtfs_data/trips.txt'
    possible_trip_ids = pd.read_csv(trips_df).trip_id.values.tolist()

    res = []
    trip_ids = []
    # TODO can prob do this all in vectorized way without rejection sampling
    for _ in range(num_records):
        # TODO pull as these out as const, build as 24*60*60
        # TODO be consistent for s vs secs in var names
        min_s = 0
        max_s = 86340
        headway_secs = np.random.choice(range(0, 12000, 60))

        # TODO prob dont need this as inner func, can prob eliminate recursion
        def gen_trip_id():
            tid = np.random.choice(possible_trip_ids)
            if tid in trip_ids:
                return gen_trip_id()
            else:
                return tid

        trip_id = gen_trip_id()
        trip_ids.append(trip_id)

        # TODO prob dont need this as inner func, can prob eliminate recursion
        def get_valid_start_end_time():
            st, et = sorted(np.random.choice(list(range(min_s, max_s, 60)), 2))
            if (et - st) < headway_secs:
                return get_valid_start_end_time()
            else:
                return st, et

        start_time, end_time = get_valid_start_end_time()

        res.append({'trip_id': trip_id,
                    'start_time': start_time, 'end_time': end_time,
                    'headway_secs': headway_secs, 'exact_times': 0})

    # Specify or assert dtypes
    df = pd.DataFrame(res, columns=['trip_id', 'start_time', 'end_time',
                                    'headway_secs', 'exact_times'])
    return df


def sample_format_range(rng):
    """Randomly select range inclusivity (i.e., inclusive or exclusive on lower
    or upper bound of provided range).

    Parameters
    ----------
    rng : (tuple)
         Tuple of exactly two ints, where rng[0] < rng[1]

    Returns
    -------
    str
        The input range formatted as a string in mathematical notation with ':'
        setting off the lower and upper bound.
    """
    # TODO explain why need ( vs [ anyway??
    a, b = rng  # TODO better name than rng
    left_inc = np.random.choice(['(', '['])
    right_inc = np.random.choice([')', ']'])
    return "{}{}:{}{}".format(left_inc, a, b, right_inc)


def sample_mode_subsidies(num_records):
    """Generate random mode subsidies inputs based on modes available for
    subsidies.

    Creates `num_records` ModeSubsidyInput records where fields for each record
    are randomly sampled as follows:
        * `age` : uniformly from `range(0,120,1)`.
        * `mode` : uniformly from list of available modes for scenario.
        * `income` : uniformly from `range(0,300000,1000)`.
        * `amount` : uniformly from `range(0.1,20)`.

    The amount of subsidy is rounded to the nearest $0.10.

    Parameters
    ----------
    num_records : (int)
        Number of randomly sampled records to create.

    Returns
    -------
    `DataFrame`
        `num_records` `ModeSubsidyInput` records.
    """
    res = []
    for _ in range(num_records):
        # TODO[saf]: make possible modes configurable by scenario
        # TODO pull out to constant
        # TODO can vectorize
        possible_modes = ['walk_transit', 'ride_hail', 'walk_transit', 'walk',
                          'car', 'drive_transit']
        mode = np.random.choice(possible_modes)
        age = tuple(sorted(np.random.choice(120, 2)))
        income = tuple(sorted(np.random.choice(range(0, 300000, 1000), 2)))
        amount = np.round(np.random.uniform(0.1, 20), 1)

        # TODO would be much cleaner df if start end were different cols
        res.append({'mode': mode, 'age': sample_format_range(age),
                    'income': sample_format_range(income), 'amount': amount})
    return pd.DataFrame(res, columns=['mode', 'age', 'income', 'amount'])

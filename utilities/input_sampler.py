"""Utility functions provided to sample random inputs for execution in Uber Prize

Example
-------
Here's how to generate a sample of 5 records from each of the provided input samplers::

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

# Below are provided for convenience as we expect auxilliary data to remain in designated location.
DIR = Path('..')
sys.path.append(str(DIR))
DATA_DIR = DIR / 'reference-data/'


def sample_vehicle_fleet_mix(num_records, scenario_name):
    """Generate random VehicleFleetMix input according to possible substitute vehicle trip ids available for
    each agency.

    Parameters
    ----------
    num_records : (int)
        Number of randomly sampled records to create

    scenario_name : (str)
        Name of scenario (used for path resolution purposes)

    Returns
    -------
    `pd.DataFrame`
        `num_records` VehicleFleetMix records. These are unique by `routeId` for each `agencyId`.
    """
    gtfs_root = DATA_DIR / scenario_name
    agencies = gtfs_root.iterdir()
    route_ids = []
    vehicle_type_ids = []
    agency_ids = []
    for agency_path in agencies:
        route_df = pd.read_csv(agency_path / "gtfs_data/routes.txt")
        route_ids.append(route_df.route_id.values.tolist())
        vehicle_type_ids.append(pd.read_csv(agency_path / "availableVehicleTypes.csv").vehicleTypeId.values.tolist())
        agency_ids.append(route_df['agency_id'].values[0])

    res = []
    pairs = []
    while len(res) < num_records:
        agency_ind = np.random.choice(len(agency_ids), 1)[0]
        agency_id, route_ids_for_agency_id, vehicle_type_ids_for_agency_id = agency_ids[agency_ind], \
                                                                             np.random.choice(route_ids[agency_ind], 1), \
                                                                             np.random.choice(
                                                                                 vehicle_type_ids[agency_ind], 1)
        route_id = np.random.choice(route_ids_for_agency_id, 1)[0]
        if len(pairs) == 0:
            pairs.append((agency_id, route_id))
        elif (agency_id, route_id) in pairs:
            continue
        else:
            pairs.append((agency_id, route_id))
        vehicle_type_id = np.random.choice(vehicle_type_ids_for_agency_id, 1)[0]
        res.append({'agencyId': agency_id, 'routeId': route_id, 'vehicleTypeId': vehicle_type_id})
    return pd.DataFrame(res)


def sample_frequency_adjustments(num_records, scenario_name):
    """Generate random FrequencyAdjustment inputs according to trips run by an agency

    Creates `num_records` records where fields for each record where the `headway_secs` field is randomly chosen
    from a range of between 0 and 12000 seconds at intervals of 60 seconds and the `min_time` and `max_time`
    field are sampled between the 0 and 86340 seconds, respectively (i.e., the possible minimum and maximum number of
    seconds in a day of 86359 seconds, given the headway interval).

    Parameters
    ----------
    num_records : (int)
        Number of randomly sampled records to create
    scenario_name: (str)
        Name of scenario (used for path resolution purposes)
    Returns
    -------
    `pd.DataFrame`
        `num_records` FrequencyAdjustmentInput records
    """

    res = []
    trip_ids = []
    gtfs_root = DATA_DIR / scenario_name
    agencies = gtfs_root.iterdir()

    # FIXME[saf}: implement for multiple agencies; taking one for now.
    agency_path = list(agencies)[0]
    possible_trip_ids = pd.read_csv(agency_path / 'gtfs_data/trips.txt').trip_id.values.tolist()

    for _ in range(num_records):
        min_s = 0
        max_s = 86340
        headway_secs = np.random.choice(range(0, 12000, 60))

        def gen_trip_id():
            tid = np.random.choice(possible_trip_ids, 1)[0]
            if tid in trip_ids:
                return gen_trip_id()
            else:
                return tid

        trip_id = gen_trip_id()
        trip_ids.append(trip_id)

        def get_valid_start_end_time():
            st, et = sorted(np.random.choice(list(range(min_s, max_s, 60)), 2))
            if (et - st) < headway_secs:
                return get_valid_start_end_time()
            else:
                return st, et

        start_time, end_time = get_valid_start_end_time()

        res.append({'trip_id': trip_id, 'start_time': start_time, 'end_time': end_time, 'headway_secs': headway_secs,
                    'exact_times': 0})

    df = pd.DataFrame(res, columns=['trip_id', 'start_time', 'end_time', 'headway_secs', 'exact_times'])

    return df


def format_range_with_sampled_inclusivity(rng):
    """Randomly select range inclusivity (i.e., inclusive or exclusive on lower or upper bound of provided range).

    Parameters
    ----------
    rng : (tuple)
         Tuple of exactly two ints, where rng[0] < rng[1]

    Returns
    -------
    str
        The input range formatted as a string in mathematical notation with ':' setting off the lower and upper bound.
    """
    a, b = rng
    left_inc = np.random.choice(['(', '['])
    right_inc = np.random.choice([')', ']'])
    return "{}{}:{}{}".format(left_inc, a, b, right_inc)


def sample_mode_subsidies(num_records):
    """Generate random mode subsidies inputs based on modes available for subsidies.

    Creates `num_records` ModeSubsidyInput records where fields for each record
    are randomly sampled as follows::
        * `age` : uniformly from `range(0,120,1)`.
        * `mode` : uniformly from list of available modes for scenario
        * `income` : uniformly from `range(0,300000,1000)`.
        * `amount` : uniformly from `range(0.1,20)`

    The amount of subsidy is rounded to the nearest $0.10.

    Parameters
    ----------
    num_records : (int)
        Number of randomly sampled records to create

    Returns
    -------
    `DataFrame`
        `num_records` ModeSubsidyInput records
    """
    res = []
    for _ in range(num_records):
        # TODO[saf]: make possible modes configurable by scenario
        possible_modes = ['walk_transit', 'ride_hail', 'walk_transit', 'walk', 'car', 'drive_transit']
        mode = np.random.choice(possible_modes)
        age = tuple(sorted(np.random.choice(120, 2)))
        income = tuple(sorted(np.random.choice(range(0, 300000, 1000), 2)))
        amount = np.round(np.random.uniform(0.1, 20), 1)

        res.append({'mode': mode, 'age': format_range_with_sampled_inclusivity(age),
                    'income': format_range_with_sampled_inclusivity(income), 'amount': amount})
    return pd.DataFrame(res, columns=['mode', 'age', 'income', 'amount'])

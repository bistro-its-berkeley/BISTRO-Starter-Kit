"""Utility functions to sample random inputs for execution in Uber Prize.

Example
-------
Provide the root to the data directory and select a scenario:

{{
    # By default, this is /reference-data in the root of this repository
    ROOT_DATA_DIR = <path_to_data_dir_as_string>
}}

Get the mapping of agencies to paths for this :

{{
    SCENARIO_NAME = 'sioux_faux'
    agency_dict = scenario_agencies(DATA_DIR, SCENARIO_NAME)
}}

Here's how to generate a sample of 5 records from each of the input samplers for an agency as
separate Pandas `DataFrame`s. For illustrative purposes, we only one agency (the only one in
Sioux Faux), but you can just iterate through the agency mapping if more agencies are desired:

    {{
    agency = 'sioux_faux_bus_lines'
    agency_dict = scenario_agencies(DATA_DIR,"siouxfalls")
    # Create a lazy cache of GTFS data for the agency:
    sf_gtfs_manager = AgencyGtfsDataManager(agency_dict[agency])

    freq_df = sample_frequency_adjustments(num_records, sf_gtfs_manager)
    mode_subsidy_df = sample_mode_subsidies(num_records)
    vehicle_fleet_mix_df = sample_vehicle_fleet_mix(num_records, sf_gtfs_manager)
    }}

Write each dataframe of samples to file using <input_df>.to_csv(<filename>, index=None) if desired.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from random_search import PT_FARE_FILE
from utils import lazyprop


def scenario_agencies(data_dir, scenario_name):
    """Given root data directory and scenario name, computes a mapping
    of agency names to their respective paths.

    Parameters
    ----------
    data_dir : Path
        Absolute path to root of data directory
    scenario_name : str
        Name of scenario with GTFS data

    Returns
    -------
    dict
        Dictionary of agency names mapped to directories containing files comprising their GTFS
        data.
    """
    gtfs_root = (data_dir / scenario_name).absolute()
    return {p.stem: p for p in
            gtfs_root.iterdir()}


class AgencyGtfsDataManager(object):

    def __init__(self, agency_gtfs_path):
        """Used to cache an agency's GTFS data for sampling purposes

        Parameters
        ----------
        agency_gtfs_path : Path
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
        return pd.read_csv(self.agency_gtfs_path / "availableVehicleTypes.csv", header=0,
                           index_col=0, na_values=None,
                           delimiter=',')

    @lazyprop
    def trips(self):
        return pd.read_csv(self.agency_gtfs_path / "gtfs_data/trips.txt", header=0, index_col=2,
                           na_values=None,
                           delimiter=',')


def sample_vehicle_fleet_mix_input(num_records, gtfs_manager):
    """Generate random `VehicleFleetMix` input according to possible substitute
    vehicle trip ids available for an agency.

    Parameters
    ----------
    num_records : int
        Number of randomly sampled records to create.
    gtfs_manager : `AgencyGtfsDataManager`
        An instance of the `AgencyGtfsDataManager` for the target agency.

    Returns
    -------
    `pd.DataFrame`
        `num_records` `VehicleFleetMix` records. These are unique by `routeId`
        for the `agencyId` specified on the `gtfs_manager`

    Raises
    ------
    `ValueError`
        If the `num_records` is in excess of the number of routes that an agency schedules buses on.
    """
    df_columns = ["agencyId", "routeId", "vehicleTypeId"]
    if num_records == 0:
        return pd.DataFrame({k: [] for k in df_columns})

    max_num_routes = gtfs_manager.routes.shape[0]
    if num_records > max_num_routes:
        raise ValueError(
            "More samples requested than the number of routes available in agency; please enter a "
            "number less than {}".format(
                max_num_routes))
    route_agency_sample = gtfs_manager.routes.sample(num_records)
    routes = pd.Series(route_agency_sample.index.values)
    agency = pd.Series(route_agency_sample.agency_id.values)
    vehicles = pd.Series(
        (gtfs_manager.vehicle_types.filter(like="BUS", axis=0)).sample(num_records, replace=True).index)
    df = pd.concat([agency, routes, vehicles], axis=1, ignore_index=True)
    df.columns = df_columns
    return df


def _get_valid_start_end_time(min_secs, max_secs, headway_secs):
    st, et = sorted(np.random.choice(list(range(min_secs, max_secs, 60)), 2))
    if (et - st) < headway_secs:
        return _get_valid_start_end_time(min_secs, max_secs, headway_secs)
    else:
        return st, et


def sample_frequency_adjustment_input(num_records, gtfs_manager):
    """Generate random `FrequencyAdjustment` inputs according to trips run by
    an agency.

    Creates `num_records` frequency adjustment records where fields for each record where the
    `headway_secs` field is randomly chosen from a range of between `min_headway_seconds`
    (per the route.txt file in the corresponding gtfs data for the trip) and 7200
    seconds at intervals of 60 seconds and the `min_time` and `max_time` field
    are sampled between the 0 and 86340 seconds, respectively (i.e.,
    the possible minimum and maximum number of seconds in a day of 86359
    seconds, given the headway interval).

    Note that a frequency adjustment is really tied to a route based on a particular trip.
    The trip serves as a template for the frequency adjustment. See the documentation
    for further details.

    Parameters
    ----------
    num_records : int
        Number of randomly sampled records to create.
    gtfs_manager : `AgencyGtfsDataManager`
        An instance of the `AgencyGtfsDataManager` for the target agency.

    Returns
    -------
    `pd.DataFrame`
        `num_records` `FrequencyAdjustmentInput` records.
    """
    df_columns = ['trip_id', 'start_time', 'end_time', 'headway_secs']
    if num_records == 0:
        return pd.DataFrame({k: [] for k in df_columns})
    min_secs = 0
    max_secs = 86340

    min_headway_mins_by_trip = gtfs_manager.trips.join(gtfs_manager.routes.min_headway_minutes,
                                                       on='route_id').min_headway_minutes
    trip_ids = pd.Series(gtfs_manager.trips.sample(num_records).index.values)
    headway_secs_arr = [np.random.choice(range(m * 60, 7200, 60)) for m in
                        min_headway_mins_by_trip[trip_ids].values]
    times_df = pd.DataFrame(
        [_get_valid_start_end_time(min_secs, max_secs, headway_secs) for headway_secs in
         headway_secs_arr])
    res_df = pd.concat([trip_ids, times_df, pd.Series(headway_secs_arr)], axis=1, ignore_index=True)
    res_df.columns = df_columns
    res_df['exact_times'] = 0
    return res_df


def sample_format_range(tuple_range):
    """Randomly select range inclusivity (i.e., inclusive or exclusive on lower
    or upper bound of provided range).

    As is typical mathematical notation, '(' or ')' means exclusive and '[' or ']' means inclusive.

    Parameters
    ----------
    tuple_range : tuple
         Tuple of exactly two ints, where tuple_range[0] < tuple_range[1]

    Returns
    -------
    str
        The input range formatted as a string in mathematical notation with ':'
        setting off the lower and upper bound.
    """
    a, b = tuple_range
    left_inc = np.random.choice(['(', '['])
    right_inc = np.random.choice([')', ']'])
    return "{}{}:{}{}".format(left_inc, a, b, right_inc)


def sample_mode_subsidies_input(num_records, gtfs_manager=None):
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
    num_records : int
        Number of randomly sampled records to create.
    gtfs_manager : `AgencyGtfsDataManager`, optional
        An instance of the `AgencyGtfsDataManager` for the target agency.

    Notes
    -----
    `gtfs_manager` added to support duck-typing this field.

    Returns
    -------
    `DataFrame`
        `num_records` `ModeSubsidyInput` records.

    """
    df_columns = ['mode', 'age', 'income', 'amount']
    if num_records == 0:
        return pd.DataFrame({k: [] for k in df_columns})
    possible_modes = ['walk_transit', 'ride_hail', 'walk_transit', 'walk',
                      'car', 'drive_transit']
    modes = np.random.choice(possible_modes, num_records).tolist()
    ages = [sample_format_range(tuple(sorted(np.random.choice(120, 2)))) for _ in
            range(num_records)]
    incomes = [sample_format_range(tuple(sorted(np.random.choice(range(0, 300000, 1000), 2)))) for _
               in range(num_records)]
    amounts = [np.round(np.random.uniform(0.1, 20), 1) for _ in range(num_records)]
    return pd.DataFrame(np.array([modes, ages, incomes, amounts]).T,
                        columns=df_columns)


def sample_pt_fares_input(num_records, gtfs_manager, max_fare_amount=10.0):
    """Generate `num_records` random `PtFares` for an
    agency (specified within `gtfs_manager`) by randomly sampling age and fare amount.

    The fare amount will not exceed the maximum fare amount and cannot be less than $0.10 (else,
    there shouldn't have been a fare assigned in the first place).

    The age will be sampled from 0 to 120 (maximum age in scenario).

    Parameters
    ----------
    num_records : int
        Number of randomly sampled records to create.
    gtfs_manager : `AgencyGtfsDataManager`
        An instance of the `AgencyGtfsDataManager` for the target agency.
    max_fare_amount : float
        The maximum fare amount that should be charged.

    Returns
    -------
    `pd.DataFrame`
        `num_records` `PtFares` records. These are unique by `routeId`
        for the `agencyId` specified on the `gtfs_manager`

    Raises
    ------
    `ValueError`
        If the `num_records` is in excess of the number of routes that an agency schedules
        buses on.
    """
    df_columns = ['agency', 'routeId', 'age', 'amount']
    if num_records == 0:
        return pd.read_csv('../submission-inputs/{0}'.format(PT_FARE_FILE))
    max_num_routes = gtfs_manager.routes.shape[0]
    if num_records > max_num_routes:
        raise ValueError(
            "More samples requested than the number of routes available in agency; please enter a "
            "number less than {}".format(
                max_num_routes))
    route_agency_sample = gtfs_manager.routes.sample(num_records)
    routes = pd.Series(route_agency_sample.index.values)
    agency = pd.Series(route_agency_sample.agency_id.values)
    amounts = [np.round(np.random.uniform(0.1, max_fare_amount), 1) for _ in range(num_records)]
    ages = [sample_format_range(tuple(sorted(np.random.choice(120, 2)))) for _ in
            range(num_records)]
    return pd.DataFrame(np.array([agency, routes, ages, amounts]).T,
                        columns=df_columns)

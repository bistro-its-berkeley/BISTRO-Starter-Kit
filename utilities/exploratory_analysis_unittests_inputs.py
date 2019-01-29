import pandas as pd
from pathlib import Path
import numpy as np
from copy import copy


# Defining input features
# 0. Route IDs
route_id = np.arange(1340, 1352).tolist()

# 1. AVAILABLE BUSES
agency = 217
agencies = [217] * len(route_id)

BUS_DEFAULT = "BUS-DEFAULT"
BUS_SMALL_HD = "BUS-SMALL-HD"
BUS_STD_ART = "BUS-STD-ART"

# 2. MODES TO SUBSIDIZE
ON_DEMAND_RIDE = "ride_hail"
DRIVE_TO_TRANSIT = "drive_transit"
WALK_TO_TRANSIT = "walk_transit"

# 3. AGE GROUPS
YOUNG = "(0:25]"
ADULTS = "(25:65]"
SENIORS = "(65:120)"
ALL_AGES = "(0:120)"

# 4. INCOME GROUPS
LOW_INCOME = "[0:20000]"
MEDIUM_INCOME = "(20000:80000]"
HIGH_INCOME = "(80000:150000]"
ALL_INCOMES = "[0:150000]"


# 4. SUBSIDY AMOUNT
no_transit_subsidy = 0.00
very_low_transit_subsidy = 10.00
low_transit_subsidy = 12.00
medium_transit_subsidy = 24.00
high_transit_subsidy = 36.00
very_high_transit_subsidy = 50.00

no_ride_hail_subsidy = 0.00
very_low_ride_hail_subsidy = 10.00
low_ride_hail_subsidy = 12.00
medium_ride_hail_subsidy = 24.00
high_ride_hail_subsidy = 36.00
very_high_ride_hail_subsidy = 50.00

# 5. HEADWAY - START TIME - END TIME
short_headway = 180  # 3min
medium_headway = 600  # 10min
long_headway = 2580  # 43min

start_time_bus_service = 21600  # 6:00am
end_time_bus_service = 79200  # 10:00pm

# 6. TRIP IDs (created based on trips.txt of SiouxFaux)
route_id = np.arange(1340, 1352).tolist()
trip_id_1 = {
    "1340": "t_75335_b_219_tn_1",
    "1341": "t_75384_b_219_tn_1",
    "1342": "t_75371_b_219_tn_1",
    "1343": "t_75320_b_219_tn_1",
    "1344": "t_75362_b_219_tn_1",
    "1345": "t_75351_b_219_tn_1",
    "1346": "t_75329_b_219_tn_1",
    "1347": "t_75340_b_219_tn_1",
    "1348": "t_75374_b_219_tn_1",
    "1349": "t_75354_b_219_tn_1",
    "1350": "t_75325_b_219_tn_1",
    "1351": "t_75373_b_219_tn_1",
}
trip_id_2 = {
    "1340_2": "t_75335_b_219_tn_2",
    "1341_2": "t_75384_b_219_tn_2",
    "1342_2": "t_75371_b_219_tn_2",
    "1343_2": "t_75320_b_219_tn_2",
    "1344_2": "t_75362_b_219_tn_2",
    "1345_2": "t_75351_b_219_tn_2",
    "1346_2": "t_75329_b_219_tn_2",
    "1347_2": "t_75340_b_219_tn_2",
    "1348_2": "t_75374_b_219_tn_2",
    "1349_2": "t_75354_b_219_tn_2",
    "1350_2": "t_75325_b_219_tn_2",
    "1351_2": "t_75373_b_219_tn_2"
}
trip_id_3 = {
    "1340_3": "t_75335_b_219_tn_3",
    "1341_3": "t_75384_b_219_tn_3",
    "1342_3": "t_75371_b_219_tn_3",
    "1343_3": "t_75320_b_219_tn_3",
    "1344_3": "t_75362_b_219_tn_3",
    "1345_3": "t_75351_b_219_tn_3",
    "1346_3": "t_75329_b_219_tn_3",
    "1347_3": "t_75340_b_219_tn_3",
    "1348_3": "t_75374_b_219_tn_3",
    "1349_3": "t_75354_b_219_tn_3",
    "1350_3": "t_75325_b_219_tn_3",
    "1351_3": "t_75373_b_219_tn_3"
}

# 6. NUMBER OF BUS ROUTES ON WHICH TO CHANGE FREQUENCY OR BUSES
small_number_routes = 3
medium_number_routes = 6
all_routes = 12

# 7. PT FARES
no_fare = 0.01
very_low_fare = 10
low_fare = 12
medium_fare = 24
high_fare = 36
very_high_fare = 50


# 8. BAU DATA FRAMES (EMPTY DF TO BE FILLED UP WHEN TESTING OTHER INPUTS)
bau_vehicle_type_input = pd.DataFrame({"agencyId": agencies, "routeId": route_id,"vehicleTypeId": [BUS_DEFAULT] * len(route_id)})

bau_incentives_input = pd.DataFrame(columns=["mode", "age", "income", "amount"])

bau_bus_fare_input = pd.DataFrame(columns=["agencyId", "routeId", "age", "amount"])

bau_frequency_input = pd.DataFrame(columns=["trip_id", "start_time", "end_time", "headway_secs", "exact_times"])

#####################################
#####################################
#####################################

# 1. VEHICLE FLEET MIX


def change_vehicle_fleet_mix():
    """ Automatically generates a list of input dictionaries, differing from the vehicle fleet mix.

    Each of these inputs dictionary will be later saved into a csv file to be able to launch simulation for each
    of them so that their outputs can be compared.


    Returns
    -------
    List of input dictionaries
    """
    # Create the bus input file
    input_sets_list = []

    for transport_type, n_bus_lines in zip([BUS_SMALL_HD, BUS_STD_ART],
                                           [all_routes, all_routes]):

        vehicle_type_input = bau_vehicle_type_input.copy()
        vehicle_index = vehicle_type_input.index
        vehicle_type_input.loc[vehicle_index[:n_bus_lines], "vehicleTypeId"] = transport_type

        inputs_fleet_mix = {
            "VehicleFleetMix": vehicle_type_input,
            "ModeSubsidies": bau_incentives_input,
            "FrequencyAdjustment": bau_frequency_input,
            "PtFares": bau_bus_fare_input
        }

        input_sets_list.append(inputs_fleet_mix)

    return input_sets_list


# 2. SUBSIDIES

def change_subsidies_input(changed_column, initial_rows, input_variation):
    """ Automatically generates a list of input dictionaries, differing from one of the four parameters of the  transit
    subsidies inputs, i.e. mode, age, income or subsidy amount.
        to everyone.

        Each of these inputs dictionary will be later saved into a csv file to be able to launch a simulation for each
        of them so that their outputs can be compared.

        Parameters
        ----------
        changed_column: str
            Name of the column whose values are changed. The value can be: "mode", "age", "income" or "amount"

        initial_rows: list
            Defines the fixed values in the three columns which will not be changed and sets the value `None` in the
            varying column, e.g. ["transit", [0, 120], [0, 500000], None]


        input_variation: list
            Lists the different values that will take the varying parameter, i.e. the input values to be tested.

        Returns
        -------
        List of input dictionaries
        """
    # Create the subsidies input file
    input_sets_list = []

    subsidies_input = bau_incentives_input.copy()

    for i in range(len(initial_rows)):
        subsidies_input.loc[i] = initial_rows[i]

    for element in input_variation:
        subsidies_input.loc[:, changed_column] = element

        inputs_fleet_mix = {
            "VehicleFleetMix": bau_vehicle_type_input,
            "ModeSubsidies": subsidies_input.copy(),
            "FrequencyAdjustment": bau_frequency_input,
            "PtFares": bau_bus_fare_input
        }

        input_sets_list.append(inputs_fleet_mix)

    return input_sets_list


def change_amount_transit_subsidies_bau():
    """ Automatically generates a list of input dictionaries, differing from the transit subsidies amount and given
    to people with low incomes.

    Returns
    -------
    List of input dictionaries
    """
    transit_subsidies_inputs_bau = []
    for income in [LOW_INCOME, MEDIUM_INCOME, HIGH_INCOME]:
        subsidies = change_subsidies_input("amount",
                                  [[DRIVE_TO_TRANSIT, ALL_AGES, income, None],
                                   [WALK_TO_TRANSIT, ALL_AGES, income, None]],
                                  [no_transit_subsidy, medium_transit_subsidy, very_high_transit_subsidy])
        transit_subsidies_inputs_bau.append(subsidies)
    return transit_subsidies_inputs_bau


def change_amount_transit_subsidies():
    """ Automatically generates a list of input dictionaries, differing from the transit subsidies amount and given
    to people with low incomes.

    Returns
    -------
    List of input dictionaries
    """
    transit_subsidies_inputs = []
    for subsidy_medium_income in [no_transit_subsidy, low_transit_subsidy, medium_transit_subsidy, high_transit_subsidy]:
        for subbsidy_high_income in [no_transit_subsidy, low_transit_subsidy, medium_transit_subsidy, high_transit_subsidy]:
            subsidies = change_subsidies_input("amount",
                                   [[DRIVE_TO_TRANSIT, ALL_AGES, LOW_INCOME, None],
                                    [WALK_TO_TRANSIT, ALL_AGES, LOW_INCOME, None],
                                    [DRIVE_TO_TRANSIT, ALL_AGES, MEDIUM_INCOME, subsidy_medium_income],
                                    [WALK_TO_TRANSIT, ALL_AGES, MEDIUM_INCOME, subsidy_medium_income],
                                    [DRIVE_TO_TRANSIT, ALL_AGES, HIGH_INCOME, subbsidy_high_income],
                                    [WALK_TO_TRANSIT, ALL_AGES, HIGH_INCOME, subbsidy_high_income]],
                                   [no_transit_subsidy, low_transit_subsidy, medium_transit_subsidy, high_transit_subsidy])
            transit_subsidies_inputs.append(subsidies)

    return transit_subsidies_inputs


def change_amount_ride_hail_subsidies_bau():
    """ Automatically generates a list of input dictionaries, differing from the ride-hail subsidies amount and given
        to people with low incomes.

        Returns
        -------
        List of input dictionaries
        """
    ride_hail_subsidies_inputs_bau = []
    for income in [LOW_INCOME, MEDIUM_INCOME, HIGH_INCOME]:
        subsidies = change_subsidies_input("amount",
                                  [[ON_DEMAND_RIDE, ALL_AGES, income, None]],
                                  [no_ride_hail_subsidy, low_ride_hail_subsidy, medium_ride_hail_subsidy, high_ride_hail_subsidy])
        ride_hail_subsidies_inputs_bau.append(subsidies)

    return ride_hail_subsidies_inputs_bau


def change_amount_ride_hail_subsidies():
    """ Automatically generates a list of input dictionaries, differing from the ride-hail subsidies amount and given
        to people with medium incomes.

        Returns
        -------
        List of input dictionaries
        """
    ride_hail_subsidies_inputs = []
    for subsidy_medium_income in [no_ride_hail_subsidy, low_ride_hail_subsidy, medium_ride_hail_subsidy,
                                  high_ride_hail_subsidy]:
        for subbsidy_high_income in [no_ride_hail_subsidy, low_ride_hail_subsidy, medium_ride_hail_subsidy,
                                  high_ride_hail_subsidy]:
            subsidies =change_subsidies_input("amount",
                                  [[ON_DEMAND_RIDE, ALL_AGES, LOW_INCOME, None],
                                   [ON_DEMAND_RIDE, ALL_AGES, MEDIUM_INCOME, subsidy_medium_income],
                                   [ON_DEMAND_RIDE, ALL_AGES, HIGH_INCOME, subbsidy_high_income]],
                                  [no_ride_hail_subsidy, low_ride_hail_subsidy, medium_ride_hail_subsidy, high_ride_hail_subsidy])
            ride_hail_subsidies_inputs.append(subsidies)

    return ride_hail_subsidies_inputs


# 3. FREQUENCY ADJUSTMENT


def list_trip_ids_on_which_frequency_is_reajusted(number_modified_bus_routes, start_time, end_time, headway):
    """Creates the rows (format and values) of the future FrequencyAdjustment input DataFrame, with one row per trip_id
    (and thus per route) for which the frequency must be adjusted

    Parameters
    ----------
    number_modified_bus_routes: float
        Number of routes on which the frequency will be adjusted

    start_time: float
        specifies the time (in seconds) at which the first vehicle departs from the first stop of the bus route with the specified
        frequency. The time is measured from "noon minus 12h" (t = 0, effectively midnight) at the beginning of the
        service day. For times occurring after midnight, enter the time as a value greater than 24*3600 = 86400[sec]
        or the day on which the trip schedule begins. E.g. 1:30am = 91800[sec].

    end_time: float
        indicates the time (in seconds) at which service changes to a different frequency (or ceases) at the first
        stop of the bus route. The time is measured following the same method as the start_time.

    headway: float
        indicates the time (in seconds) between departures from the first stop (headway) for this bus route, during the
        time interval specified by start_time and end_time. The headway value must be entered in seconds.

    Returns
    -------
    initial_rows: list
        Defines the rows (format and values) of the future FrequencyAdjustment input DataFrame.
        e.g [[trip_id_1], start_time_1, end_time_1, headway_1],[trip_id_2], start_time_2, end_time_2, headway2]]


    """
    initial_rows = []
    for i in range(number_modified_bus_routes):
        input_list = [None, start_time, end_time, headway, 0]
        input_list[0] = trip_id_1["{0}".format(route_id[i])]
        initial_rows.append(input_list)
    return initial_rows


def change_frequency_input(changed_column, initial_rows, input_variation):
    """ Automatically generates a list of input dictionaries, differing from one of the four variable parameters of the
    frequency adjustment inputs, i.e. trip_id, start_time, end_time or headway_secs.
        to everyone.

        Each of these inputs dictionary will be later saved into a csv file to be able to launch a simulation for each
        of them so that their outputs can be compared.

        Parameters
        ----------
        changed_column: str
            Name of the column whose values are changed. The value can be: "trip_id", "start_time", "end_time" or
            "headway_secs"

        initial_rows: list
            Defines the fixed values in the three columns which will not be changed and sets the value `None` in the
            varying column, e.g. ["1340_1", 28800, 72000, None]: the carrying parameter is headway_secs


        input_variation: list
            Lists the different values that will take the varying parameter, i.e. the input values to be tested.

        Returns
        -------
        List of input dictionaries
        """
    # Create the subsidies input file
    input_sets_list = []

    frequency_input = bau_frequency_input.copy()

    for i in range(len(initial_rows)):
        frequency_input.loc[i] = initial_rows[i]

    for element in input_variation:
        frequency_input.loc[:, changed_column] = element

        inputs_fleet_mix = {
            "VehicleFleetMix": bau_vehicle_type_input,
            "ModeSubsidies": bau_incentives_input,
            "FrequencyAdjustment": frequency_input.copy(),
            "PtFares": bau_bus_fare_input
        }

        input_sets_list.append(inputs_fleet_mix)

    return input_sets_list


def change_headway_for_all_bus_routes_all_day():
    """Automatically generates a list of input dictionaries, differing from the headway on all bus routes for the whole
    day

        Returns
        -------
        List of input dictionaries

    """
    return change_frequency_input("headway_secs",
                                  list_trip_ids_on_which_frequency_is_reajusted(12, start_time_bus_service, end_time_bus_service, None),
                                  [short_headway, medium_headway, long_headway])


# 4. PUBLIC TRANSPORTATION FARES


def list_route_ids_on_which_the_bus_fare_is_changed(number_modified_bus_routes, age, amount):
    """Creates the initial rows (format and values) of the future PtFares input DataFrame, with one row per
    route for which the bus fare must be changed

    Parameters
    ----------
    number_modified_bus_routes: float
        Number of routes on which the frequency will be adjusted

    age: str
        age range concerned by the fare. The argument must be in mathematical notation where parentheses () indicate
        exclusive bounds and brackets [ ] indicate inclusive bounds.

    amount: float
        amount of the fare in [$]

    Returns
    -------
    initial_rows: list
        Defines the rows (format and values) of the future FrequencyAdjustment input DataFrame.
        e.g [[trip_id_1], start_time_1, end_time_1, headway_1],[trip_id_2], start_time_2, end_time_2, headway2]]


    """
    initial_rows = []
    input_list = [int(agency), None, age, amount]
    for i in range(number_modified_bus_routes):
        input_list[1] = int(route_id[i])
        initial_rows.append(input_list.copy())
    return initial_rows


def change_public_transportation_fare_input(changed_column, initial_rows, input_variation):
    """ Automatically generates a list of input dictionaries, differing from one of the three variable parameters of the
    public transportation fares inputs, i.e. route_id, age or amount.

        Each of these inputs dictionary will be later saved into a csv file to be able to launch a simulation for each
        of them so that their outputs can be compared.

        Parameters
        ----------
        changed_column: str
            Name of the column whose values are changed. The value can be: "trip_id", "start_time", "end_time" or
            "headway_secs"

        initial_rows: list
            Defines the fixed values in the three columns which will not be changed and sets the value `None` in the
            varying column, e.g. ["1340_1", 28800, 72000, None]: the carrying parameter is headway_secs

        input_variation: list
            Lists the different values that will take the varying parameter, i.e. the input values to be tested.

        Returns
        -------
        List of input dictionaries
        """
    # Create the subsidies input file
    input_sets_list = []

    pt_fare_input = pd.DataFrame(initial_rows, columns=bau_bus_fare_input.columns)

    for element in input_variation:
        pt_fare_input.loc[:, changed_column] = element

        inputs_fleet_mix = {
            "VehicleFleetMix": bau_vehicle_type_input,
            "ModeSubsidies": bau_incentives_input,
            "FrequencyAdjustment": bau_frequency_input,
            "PtFares": pt_fare_input.copy()
        }

        input_sets_list.append(inputs_fleet_mix)

    return input_sets_list


def change_amount_fare_for_all_routes_for_young_people_and_seniors_adults_bau():
    """Automatically generates a list of input dictionaries, differing from the fare amount on all bus routes and for
    young people and seniors.

       Returns
       -------
       List of input dictionaries

    """
    return change_public_transportation_fare_input("amount",
                                                   [list_route_ids_on_which_the_bus_fare_is_changed(all_routes, YOUNG, None),
                                                    list_route_ids_on_which_the_bus_fare_is_changed(all_routes, SENIORS,None)],
                                                   [no_fare, low_fare, medium_fare, high_fare])


def change_amount_fare_for_all_routes_for_middle_age_people_young_people_and_seniors_bau():
    """Automatically generates a list of input dictionaries, differing from the fare amount on all bus routes and for
    young people and seniors.

       Returns
       -------
       List of input dictionaries

    """
    return change_public_transportation_fare_input("amount",
                                                   [list_route_ids_on_which_the_bus_fare_is_changed(all_routes, ADULTS, None)],
                                                   [no_fare, low_fare, medium_fare, high_fare])


def change_amount_fare_for_all_routes_for_young_people_and_seniors_adults_free():
    """Automatically generates a list of input dictionaries, differing from the fare amount on all bus routes and for
    young people and seniors.

       Returns
       -------
       List of input dictionaries

    """
    return change_public_transportation_fare_input("amount",
                                                   [list_route_ids_on_which_the_bus_fare_is_changed(all_routes, YOUNG, None),
                                                    list_route_ids_on_which_the_bus_fare_is_changed(all_routes, SENIORS,None),
                                                    list_route_ids_on_which_the_bus_fare_is_changed(all_routes, ADULTS,no_fare)],
                                                   [no_fare, low_fare, medium_fare, high_fare])


def change_amount_fare_for_all_routes_for_young_people_and_seniors_adults_low_fare():
    """Automatically generates a list of input dictionaries, differing from the fare amount on all bus routes and for
    young people and seniors.

       Returns
       -------
       List of input dictionaries

    """
    return change_public_transportation_fare_input("amount",
                                                   [list_route_ids_on_which_the_bus_fare_is_changed(all_routes, YOUNG, None),
                                                    list_route_ids_on_which_the_bus_fare_is_changed(all_routes, SENIORS,None),
                                                    list_route_ids_on_which_the_bus_fare_is_changed(all_routes, ADULTS,low_fare)],
                                                   [no_fare, low_fare, medium_fare, high_fare])


def change_amount_fare_for_all_routes_for_young_people_and_seniors_adults_medium_fare():
    """Automatically generates a list of input dictionaries, differing from the fare amount on all bus routes and for
    young people and seniors.

       Returns
       -------
       List of input dictionaries

    """
    return change_public_transportation_fare_input("amount",
                                                   [list_route_ids_on_which_the_bus_fare_is_changed(all_routes, YOUNG, None),
                                                    list_route_ids_on_which_the_bus_fare_is_changed(all_routes, SENIORS,None),
                                                    list_route_ids_on_which_the_bus_fare_is_changed(all_routes, ADULTS,medium_fare)],
                                                   [no_fare, low_fare, medium_fare, high_fare])


def change_amount_fare_for_all_routes_for_young_people_and_seniors_adults_high_fare():
    """Automatically generates a list of input dictionaries, differing from the fare amount on all bus routes and for
    young people and seniors.

       Returns
       -------
       List of input dictionaries

    """
    return change_public_transportation_fare_input("amount",
                                                   [list_route_ids_on_which_the_bus_fare_is_changed(all_routes, YOUNG, None),
                                                    list_route_ids_on_which_the_bus_fare_is_changed(all_routes, SENIORS,None),
                                                    list_route_ids_on_which_the_bus_fare_is_changed(all_routes, ADULTS,high_fare)],
                                                   [no_fare, low_fare, medium_fare, high_fare])






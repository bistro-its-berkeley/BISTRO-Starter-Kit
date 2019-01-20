import pandas as pd
import numpy as np
import itertools

# Defining input features
# 0. Route IDs
route_id = np.arange(1340, 1352).tolist()

# 1. AVAILABLE BUSES
agencies = [217] * len(route_id)
agency = 217

BUS_SMALL_HD = "BUS-SMALL-HD"
BUS_STD_ART = "BUS-STD-ART"
BUS_DEFAULT = "BUS-DEFAULT"


# 2. MODES TO SUBSIDIZE
ON_DEMAND_RIDE = "OnDemand_ride"
DRIVE_TO_TRANSIT = "drive_transit"
WALK_TO_TRANSIT = "walk_transit"

# 3. AGE GROUPS
YOUNG = "(0:25]"
ADULTS = "(25:65]"
SENIORS = "(65:120)"
ALL_AGES = "(0:120)"

# 4. INCOME GROUPS
LOW_INCOME = "(0:25000]"
ALL_INCOMES = "(0:500000]"

# 4. INCENTIVE AMOUNT
transit_subsidy = 50
on_demand_ride_subsidy = 50

# MASS TRANSIT FARES
full_fare = 50
free = 0.01


# 6. BAU DATA FRAMES (EMPTY DF TO BE FILLED UP WHEN TESTING OTHER INPUTS)
bau_vehicle_type_input = pd.DataFrame({"agencyId": agencies, "routeId": route_id,"vehicleTypeId": [BUS_DEFAULT] * len(route_id)})

bau_incentives_input = pd.DataFrame(columns=["mode", "age", "income", "amount"])

bau_bus_fare_input = pd.DataFrame(columns=["agencyId", "routeId", "age", "amount"])

bau_frequency_input = pd.DataFrame(columns=["trip_id", "start_time", "end_time", "headway_secs", "exact_times"])


#######################################

incentive_1 = [[DRIVE_TO_TRANSIT, None, LOW_INCOME, transit_subsidy],
               [WALK_TO_TRANSIT, None, LOW_INCOME, transit_subsidy]]

incentive_2 = [[DRIVE_TO_TRANSIT, ALL_AGES, ALL_INCOMES, transit_subsidy],
               [WALK_TO_TRANSIT, ALL_AGES, ALL_INCOMES, transit_subsidy]]

incentive_3 = [[ON_DEMAND_RIDE, ALL_AGES, ALL_INCOMES, on_demand_ride_subsidy]]

incentive_4 = [[ON_DEMAND_RIDE, None, LOW_INCOME, on_demand_ride_subsidy]]

incentive = [incentive_1, incentive_2, incentive_3, incentive_4]

# Building the ModeIncentive input dataframes
input_incentives_list = []

for incentive_i in incentive:
    incentives_input = pd.DataFrame(incentive_i)
    incentives_input.columns = bau_incentives_input.columns

    input_incentives_list.append(incentives_input)

# Mass transit fare input
    # Combination 1
ages_1 = [YOUNG, SENIORS, ADULTS]
fares_1 = [free, free, full_fare]

pt_fare_1 = []
for agency, age, fare in zip(agencies, ages_1, fares_1):
        for route in route_id:
            policy = [agency, route, age, fare]
            pt_fare_1.append(policy)

    # Combination 2
ages_2 = [ALL_AGES]
fares_2 = [full_fare]

pt_fare_2 = []
for agency, age, fare in zip(agencies, ages_2, fares_2):
        for route in route_id:
            policy = [agency, route, age, fare]
            pt_fare_2.append(policy)

mass_transit_fare = [pt_fare_1, pt_fare_2]

# Building the PtFares input DataFrames

input_bus_fare_list = []

for mass_transit_fare_i in mass_transit_fare:
    bus_fare_input = pd.DataFrame(mass_transit_fare_i)
    bus_fare_input.columns = bau_bus_fare_input.columns
    input_bus_fare_list.append(bus_fare_input)

input_combinations = list(itertools.product(input_incentives_list, input_bus_fare_list))

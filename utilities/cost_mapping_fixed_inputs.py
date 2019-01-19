import pandas as pd
import numpy as np
import itertools

# Defining input features
# 0. Route IDs
route_id = np.arange(1340, 1352).tolist()

# 1. AVAILABLE BUSES
agencies = [217] * len(route_id)

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
SENIORS = "(65:120]"
ALL_AGES = "(0:120]"

# 4. INCOME GROUPS
LOW_INCOME = "[0:25000]"
ALL_INCOMES = "[0:500000]"

# 4. INCENTIVE AMOUNT
transit_subsidy = 1.0e6
on_demand_ride_subsidy = 1.0e6

# MASS TRANSIT FARES
full_fare = 1.0e6
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
pt_fare_1 = [[217, 1340, YOUNG, free],
             [217, 1341, YOUNG, free],
             [217, 1342, YOUNG, free],
             [217, 1343, YOUNG, free],
             [217, 1344, YOUNG, free],
             [217, 1345, YOUNG, free],
             [217, 1346, YOUNG, free],
             [217, 1347, YOUNG, free],
             [217, 1348, YOUNG, free],
             [217, 1349, YOUNG, free],
             [217, 1350, YOUNG, free],
             [217, 1351, YOUNG, free],
           [217, 1340, SENIORS, free],
           [217, 1341, SENIORS, free],
           [217, 1342, SENIORS, free],
           [217, 1343, SENIORS, free],
           [217, 1344, SENIORS, free],
           [217, 1345, SENIORS, free],
           [217, 1346, SENIORS, free],
           [217, 1347, SENIORS, free],
           [217, 1348, SENIORS, free],
           [217, 1349, SENIORS, free],
           [217, 1350, SENIORS, free],
           [217, 1351, SENIORS, free],
           [217, 1340, ADULTS, full_fare],
           [217, 1341, ADULTS, full_fare],
           [217, 1342, ADULTS, full_fare],
           [217, 1343, ADULTS, full_fare],
           [217, 1344, ADULTS, full_fare],
           [217, 1345, ADULTS, full_fare],
           [217, 1346, ADULTS, full_fare],
           [217, 1347, ADULTS, full_fare],
           [217, 1348, ADULTS, full_fare],
           [217, 1349, ADULTS, full_fare],
           [217, 1350, ADULTS, full_fare],
           [217, 1351, ADULTS, full_fare]]

pt_fare_2 = [[217, 1340, ALL_AGES, full_fare],
           [217, 1341, ALL_AGES, full_fare],
           [217, 1342, ALL_AGES, full_fare],
           [217, 1343, ALL_AGES, full_fare],
           [217, 1344, ALL_AGES, full_fare],
           [217, 1345, ALL_AGES, full_fare],
           [217, 1346, ALL_AGES, full_fare],
           [217, 1347, ALL_AGES, full_fare],
           [217, 1348, ALL_AGES, full_fare],
           [217, 1349, ALL_AGES, full_fare],
           [217, 1350, ALL_AGES, full_fare],
           [217, 1351, ALL_AGES, full_fare]]

mass_transit_fare = [pt_fare_1, pt_fare_2]

# Building the PtFares input DataFrames

input_bus_fare_list = []

for mass_transit_fare_i in mass_transit_fare:
    bus_fare_input = pd.DataFrame(mass_transit_fare_i)
    bus_fare_input.columns = bau_bus_fare_input.columns
    input_bus_fare_list.append(bus_fare_input)

input_combinations = list(itertools.product(input_incentives_list, input_bus_fare_list))

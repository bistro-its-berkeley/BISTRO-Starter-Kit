import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.cm import ScalarMappable


import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path
import math

# Defining matplolib parameters
plt.rcParams["axes.titlesize"] = 15
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.titlepad"] = 12
plt.rcParams["axes.labelsize"] = 11
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams["xtick.labelsize"] = 11
plt.rcParams["ytick.labelsize"] = 11


def unzip_file(element_path):
    """Checking if the path points to an existing folder or to its .zip format; if only the .zip format exists,
    it unzips the folder.

    Parameters
    ----------
    element_path: PosixPath
        Absolute path of the folder or file of interest.

    Returns
    -------
        Absolute path of the (unzipped) folder of interest.
    """
    import zipfile
    import gzip
    import shutil

    if element_path.exists():
        return element_path

    elif Path(str(element_path) + ".zip").exists():
        zip_folder = zipfile.ZipFile(str(element_path) + ".zip", 'r')
        zip_folder.extractall(element_path)
        zip_folder.close()
        return element_path

    elif Path(str(element_path) + ".gz").exists():
        with gzip.open(str(element_path) + ".gz", 'rb') as f_in:
            with open(str(element_path), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return element_path

    else:
        raise FileNotFoundError(f"{folder_path} does not exist")



########## PROCESS AND PLOT STATISTICS ##########

### 1- INPUTS ###

def splitting_min_max(df, name_column):
    """ Parsing and splitting the ranges in the "age" (or "income") columns into two new columns:
    "min_age" (or "min_income") with the bottom value of the range and "max_age" (or "max_income") with the top value
    of the range. Ex: [0:120] --> 0, 120

    Parameters
    ----------
    df: pandas dataframe
        ModeIncentives.csv or MassTransitFares.csv input file

    name_column: str
        Column containing the range values to parse

    Returns
    -------
    df: pandas dataframe
        New input dataframe with two "min" and "max" columns with floats int values instead of ranges values

    """
    # Parsing the ranges and creating two new columns with the min and max values of the range
    if df.empty:
        df["min_{0}".format(name_column)] = [0]
        df["max_{0}".format(name_column)] = [0]
    else:
        min_max = df[name_column].str.replace("[", "").str.replace("]", "").str.replace("(", "").str.replace(")", "")\
            .str.split(":", expand=True)
        df["min_{0}".format(name_column)] = min_max.iloc[:, 0].astype(int)
        df["max_{0}".format(name_column)] = min_max.iloc[:, 1].astype(int)

    return df


def process_incentives_data(incentives_data_path, max_incentive):
    """ Processing and reorganizing the data in an input dataframe to be ready for plotting

    Parameters
    ----------
    incentives_data_path: PosixPath
        Absolute path of the ModeIncentives.csv input file

    max_incentive: float
        Maximum amount allowed for an incentive as defined in the Starter Kit "Inputs Specifications" page

    Returns
    -------
    incentives: pandas dataframe
        Incentives input data that is ready for plotting
    """
    incentives = pd.read_csv(incentives_data_path)
    incentives["amount"] = incentives["amount"].astype(float)

    # Completing the dataframe with the missing subsidized modes (so that they appear in the plot)
    df = pd.DataFrame(["", "(0:0)", "(0:0)", 0.00]).T
    df.columns = ["mode", "age", "income", "amount"]

    modes = ["drive_transit", "walk_transit", "OnDemand_ride"]
    for mode in modes:
        if mode not in incentives["mode"].values:
            df["mode"] = mode
            incentives = incentives.append(df)

    # Splitting age and income columns
    splitting_min_max(incentives, "age")
    splitting_min_max(incentives, "income")

    # Creating a new column with normalized incentives amount for the colormap
    if np.max(incentives["amount"]) == 0:
        incentives["amount_normalized"] = 0
    else:
        incentives["amount_normalized"] = incentives["amount"] / max_incentive

    incentives["amount_normalized"] = incentives["amount_normalized"].astype('float')
    incentives = incentives.drop(labels=["age", "income"], axis=1)

    # Changing the type of the "mode" column to 'category' to reorder the modes
    incentives["mode"] = incentives["mode"].astype('category').cat.reorder_categories([
        'OnDemand_ride',
        'drive_transit',
        'walk_transit'])

    incentives = incentives.sort_values(by="mode")
    return incentives


def plot_incentives_inputs(incentives_data_path, max_incentive, max_age, max_income):
    """Plot the incentives input

    Parameters
    ----------
    incentives_data_path: PosixPath
        Absolute path of the ModeIncentives.csv input file

    max_incentive: float
        Maximum amount allowed for an incentive as defined in the Starter Kit "Inputs Specifications" page

    max_age: int
        Maximum age of any resident in Sioux Faux as defined in the Starter Kit "Inputs Specifications" page

    max_income: int
        Maximum income of any resident in Sioux Faux as defined in the Starter Kit "Inputs Specifications" page

    Returns
    -------
    ax: matplotlib axes object

    """
    incentives = process_incentives_data(incentives_data_path, max_incentive)

    fig, ax = plt.subplots(1, 2, figsize=(14, 5), sharey=True, gridspec_kw={'width_ratios': [4, 5]})

    # color map
    my_cmap = plt.cm.get_cmap('YlOrRd')
    colors = my_cmap(incentives["amount_normalized"])

    # plot
    ax[0].barh(incentives["mode"], incentives["max_age"] - incentives["min_age"], left=incentives["min_age"], color=colors)
    ax[1].barh(incentives["mode"], incentives["max_income"]-incentives["min_income"], left=incentives["min_income"], color=colors)

    ax[0].set_xlabel("age")
    ax[0].set_xlim((0, max_age))

    ax[1].set_xlabel("income")
    ax[1].set_xlim((0, max_income))

    plt.suptitle("Input - Incentives by age and income group")

    sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0, np.max(incentives["amount"])))
    sm.set_array([])
    sm.set_clim(0, max_incentive)
    cbar = fig.colorbar(sm, ticks=[i for i in range(0, max_incentive + 1, 10)])
    cbar.set_label('Incentive amount [$/person-trip]', rotation=270, labelpad=25)

    return ax


def process_bus_data(vehicle_fleet_mix_data_path, route_ids, buses_list, agency_ids):
    """Processing and reorganizing the data in an input dataframe to be ready for plotting

    Parameters
    ----------
    vehicle_fleet_mix_data_path: PosixPath
        Absolute path of the FleetMix.csv input file

    route_ids: list
        All routes ids where buses operate (from `routes.txt` file in the GTFS data)

    buses_list: list
        All available buses, ordered as follow: the DEFAULT bus first and then the buses ordered by ascending bus size
        (from availableVehicleTypes.csv in the `reference-data` folder of the Starter Kit)

    agency_ids: list
        All agencies operating buses in the city (from `agencies.txt` file in the GTFS data)

    Returns
    -------
    fleet_mic: pandas dataframe
        FleetMix input data that is ready for plotting

    """
    fleet_mix = pd.read_csv(vehicle_fleet_mix_data_path)

    if fleet_mix.empty:
        fleet_mix = pd.DataFrame([[agency_id, f"{route_id}", "BUS-DEFAULT"] for route_id in route_ids for agency_id in agency_ids],
                                 columns=["agencyId", "routeId", "vehicleTypeId"])

    df = pd.DataFrame([agency_ids[0], 1, buses_list[0]]).T
    df.columns = ["agencyId", "routeId", "vehicleTypeId"]

    # Adding the missing bus types in the dataframe so that they appear in the plot
    for bus in buses_list:
        if bus not in fleet_mix["vehicleTypeId"].values:
            df["vehicleTypeId"] = bus
            fleet_mix = fleet_mix.append(df)

    # Adding the missing bus routes in the dataframe so that they appear in the plot
    fleet_mix["routeId"] = fleet_mix["routeId"].astype(int)

    df = pd.DataFrame([agency_ids[0], "", buses_list[0]]).T
    df.columns = ["agencyId", "routeId", "vehicleTypeId"]

    for route in [i for i in route_ids]:
        if route not in fleet_mix["routeId"].values:
            df["routeId"] = route
            fleet_mix = fleet_mix.append(df)

    # Reodering bus types starting by "BUS-DEFAULT" and then by ascending bus size order
    fleet_mix["vehicleTypeId"] = fleet_mix["vehicleTypeId"].astype('category').cat.reorder_categories(
        buses_list)

    fleet_mix = fleet_mix.drop(labels="agencyId", axis=1)
    fleet_mix.sort_values(by="vehicleTypeId", inplace=True)
    fleet_mix.reset_index(inplace=True, drop=True)

    return fleet_mix


def plot_vehicle_fleet_mix_inputs(vehicle_fleet_mix_data_path, route_ids, buses_list, agency_ids):
    """Plot the vehicle fleet mix input

    Parameters
    ----------
   See `process_bus_data()`

    Returns
    -------
    ax: matplotlib axes object

    """
    buses = process_bus_data(vehicle_fleet_mix_data_path, route_ids, buses_list, agency_ids)

    fig, ax = plt.subplots(figsize=(6.5, 5))

    ax = sns.scatterplot(x="vehicleTypeId", y="routeId", data=buses, s=80)

    plt.xlabel("Bus type")
    plt.ylabel("Bus route")
    plt.ylim((1339.5, 1351.5))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))

    plt.title("Input - Bus fleet mix")

    return ax


def process_fares_data(fares_data_path, bau_fares_data_path, max_fare, route_ids):
    """Processing and reorganizing the data in an input dataframe to be ready for plotting


    Parameters
    ----------
    fares_data_path: PosixPath
        Absolute path of the MassTransitFares.csv input file

    bau_fares_data_path: PosixPath
        Absolute path of the BAUFleetMix.csv input file

    max_fare: float
        Maximum fare of a bus trip as defined in the Starter Kit "Inputs Specifications" page

    route_ids: list
        All routes ids where buses operate (from `routes.txt` file in the GTFS data)


    Returns
    -------
    fares: pandas DataFrame
        Mass Transit Fares input data that is ready for plotting
    """
    fares = pd.read_csv(fares_data_path)
    fares_bau = pd.read_csv(bau_fares_data_path)

    fares["age"] = fares["age"].astype(str)

    df = pd.DataFrame(columns=["agencyId", "routeId", "age", "amount"])

    # Replace RouteId = NaN values by all bus lines (12 rows)
    for row in range(len(fares)):
        if math.isnan(fares.iloc[row, 1]):
            df1 = pd.DataFrame(
                [[fares.iloc[row, 0], route, fares.iloc[row, 2], fares.iloc[row, 3]] for route in route_ids],
                columns=["agencyId", "routeId", "age", "amount"])
            df = df.append(df1)

        else:
            df = fares

    # Adding the missing bus types in the dataframe so that they appear in the plot
    for route_id in route_ids:
        if route_id not in df["routeId"].values:
            fares_bau["routeId"] = [route_id, route_id]
            df = df.append(fares_bau)

    # Splitting age ranges into 2 columns (min_age and max_age)
    fares = splitting_min_max(df, "age")
    fares["routeId"] = fares["routeId"].astype(int)
    fares["amount"] = fares["amount"].astype(float)

    fares = fares.drop(labels=["age"], axis=1)
    fares = fares.sort_values(by=["amount", "routeId"])
    fares["amount_normalized"] = fares["amount"] / max_fare

    return fares


def plot_mass_transit_fares_inputs(fares_data_path, bau_fares_data, max_fare, route_ids):
    """Plot the Mass Transit Fares input

        Parameters
        ----------
       See `process_fares_data()`

        Returns
        -------
        ax: matplotlib axes object

        """
    fares = process_fares_data(fares_data_path, bau_fares_data, max_fare, route_ids)

    fig, ax = plt.subplots(figsize = (7,5))

    #color map
    my_cmap = plt.cm.get_cmap('YlOrRd')
    colors = my_cmap(fares["amount_normalized"])

    plt.barh(fares["routeId"], fares["max_age"] - fares["min_age"], left=fares["min_age"], color=colors)

    plt.xlabel("Age")
    plt.ylabel("Bus route")
    plt.ylim((1339.5, 1351.5))
    plt.xlim((0, 120))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax.xaxis.set_major_locator(plt.MultipleLocator(10))

    sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0, np.max(fares["amount"])))
    sm.set_array([])
    sm.set_clim(0, max_fare)
    cbar = fig.colorbar(sm, ticks=[i for i in range(0, max_fare + 1)])
    cbar.set_label('Fare amount [$]', rotation=270, labelpad=25)

    # Replace the 0 by 0.01 in the color scale as fares must be greater than 0
    y_ticks_labels = ["{0}".format(i) for i in range(0, 10 + 1)]
    y_ticks_labels[0] = "0.01"
    cbar.ax.set_yticklabels(y_ticks_labels)

    plt.title("Input - Mass Transit Fares")
    return ax


def process_frequency_data(bus_frequencies_data_path, route_ids):
    """Processing and reorganizing the data in an input dataframe to be ready for plotting

    Parameters
    ----------
    bus_frequencies_data_path : PosixPath
        Absolute path of the `FrequencyAdjustment.csv` input file

    route_ids: list
        All routes ids where buses operate (from `routes.txt` file in the GTFS data)

    Returns
    -------
    frequency : pandas DataFrame
        Frequency Adjustment input data that is ready for plotting.

    """
    frequency = pd.read_csv(bus_frequencies_data_path)

    # Add all missing routes (the ones that were not changed) in the DF so that they appear int he plot
    df = pd.DataFrame([0, 0, 0, 1]).T
    df.columns = ["route_id", "start_time", "end_time", "headway_secs"]

    for route in route_ids:
        if route not in frequency["route_id"].values:
            df["route_id"] = route
            frequency = frequency.append(df)

    frequency["start_time"] = (frequency["start_time"].astype(int) / 3600).round(1)
    frequency["end_time"] = (frequency["end_time"].astype(int) / 3600).round(1)
    frequency["headway_secs"] = (frequency["headway_secs"].astype(int) / 3600).round(1)
    frequency["route_id"] = frequency["route_id"].astype(int)

    frequency = frequency.sort_values(by="route_id")
    frequency = frequency.set_index("route_id")

    return frequency


def plot_bus_frequency(bus_frequencies_data, route_ids):
    """Plotting the Frequency Adjustment input

    Parameters
    ----------
    See `process_frequency_data()`

    Returns
    -------
    ax: matplotlib axes object

    """

    frequencies = process_frequency_data(bus_frequencies_data, route_ids)

    fig, ax = plt.subplots(figsize=(15, 4))
    plotted_lines = []

    # Defines a set of 12 colors for the bus lines
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'pink', 'gold', 'lime', 'steelblue', 'm',
              'limegreen']
    color_dict = {frequencies.index.unique()[i]: colors[i] for i in range(12)}

    for idx in range(len(frequencies)):
        row_freq = frequencies.iloc[idx]
        height = row_freq.headway_secs
        height = height + np.random.normal(0, 0.03, 1)
        if row_freq.name not in plotted_lines:
            ax.plot([row_freq.start_time, row_freq.end_time], [height, height],
                    label=row_freq.name, linewidth=5, alpha=0.8, color=color_dict[row_freq.name])
            plotted_lines.append(row_freq.name)
        else:
            ax.plot([row_freq.start_time, row_freq.end_time], [height, height],
                    linewidth=5, alpha=0.8, color=color_dict[row_freq.name])

    plt.legend(bbox_to_anchor=(1.1, 1.0), title='Bus line')
    plt.ylim(0.0, 2.0)
    plt.xticks(np.arange(0, 25, 1))
    ax.set_xlim(0, 24)
    plt.ylabel("Headway [h]")
    plt.xlabel("Hours of the day")
    plt.title("Input - Frequency Adjustment")

    return ax

### 2 - OUTPUTS ###

def process_overall_mode_choice(mode_choice_data_path):
    """Processing and reorganizing the data in a dataframe ready for plotting

    Parameters
    ----------
    mode_choice_data_path:  PosixPath
        Absolute path of the `modeChoice.csv` input file (located in the output directory of the simulation)

    Returns
    -------
    mode_choice: pandas DataFrame
        Mode choice data that is ready for plotting.

    """
    mode_choice = pd.read_csv(mode_choice_data_path)
    # Select columns w/ modes
    mode_choice = mode_choice.iloc[-1,:]
    mode_choice = mode_choice.drop(["iterations"])
    # Replace "ride_hail" by "on_demand ride"
    mode_choice.rename({"ride_hail":"on-demand ride"}, inplace = True)
    return mode_choice


def plot_overall_mode_choice(mode_choice_data_path):
    """Plotting the Overall Mode choice output

    Parameters
    ----------
    see process_overall_mode_choice()

    Returns
    -------
    ax: matplotlib axes object

    """
    mode_choice = process_overall_mode_choice(mode_choice_data_path)
    fig, ax = plt.subplots(figsize=(7, 5))
    mode_choice.plot(kind="pie", startangle=90, labels=None, autopct='%1.1f%%', pctdistance=0.8)
    plt.axis("image")
    plt.ylabel("")

    labels = mode_choice.index.values
    ax.legend(labels, bbox_to_anchor=(1.1, 0.5), loc="center right", fontsize=11, bbox_transform=plt.gcf().transFigure,
               title="Mode", palette="Set2")

    ax.set_title("Output - Overall mode choice")
    return ax


def process_mode_choice_by_hour(mode_choice_by_hour_data_path):
    """Processing and reorganizing the data in a dataframe ready for plotting

    Parameters
    ----------
    mode_choice_by_hour_data_path:  PosixPath
        Absolute path of the `{ITER_NUMBER}modeChoice.csv` input file (located in the
        <output directory>/ITERS/it.<ITER_NUMBER>/ directory of the simulation)

    Returns
    -------
    mode_choice_by_hour: pandas DataFrame
        Mode choice by hour data ready for plotting.

        """
    mode_choice_by_hour = pd.read_csv(mode_choice_by_hour_data_path, index_col=0).T
    mode_choice_by_hour.reset_index(inplace=True)
    mode_choice_by_hour.dropna(inplace=True)
    mode_choice_by_hour.loc[:, "hours"] = mode_choice_by_hour["index"].apply(lambda x: x.split("_")[1])
    mode_choice_by_hour = mode_choice_by_hour.set_index("hours")
    mode_choice_by_hour.rename({"ride_hail": "on-demand ride"}, inplace=True)
    mode_choice_by_hour = mode_choice_by_hour.drop(labels="index", axis=1)

    return mode_choice_by_hour


def plot_mode_choice_by_hour(mode_choice_by_hour_data_path):
    """Plotting the Overall Mode choice By Hour output

    Parameters
    ----------
    see process_mode_choice_by_hour()

    Returns
    -------
    ax: matplotlib axes object
    """
    mode_choice_per_hour = process_mode_choice_by_hour(mode_choice_by_hour_data_path)

    fig, ax = plt.subplots(figsize=(7, 5))
    mode_choice_per_hour.plot.bar(stacked=True, figsize=(15, 5))
    ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", title="Mode")
    plt.xlabel("Hours")
    plt.ylabel("Number of trips chosing the mode")
    plt.grid(alpha=0.9)

    ax.set_title("Output - Mode choice over the agent's day \n (goes past midnight)")
    return ax


def plot_mode_choice_by_income_group(person_df, trips_df):
    """Plotting the Overall Mode choice By Income Group output

    Parameters
    ----------
    person_df: pandas DataFrame
        parsed and processed xml.files

    trips_df: pandas DataFrame
        parsed and processed xml.files

    Returns
    -------
    ax: matplotlib axes object
    """
    person_df = person_df[['PID', 'Age', 'income']]
    mode_df = trips_df[['PID', 'Mode']]
    people_age_income_mode = person_df.merge(mode_df, on=['PID'])
    people_age_income_mode['income_group'] = pd.cut(people_age_income_mode.income,
                                                    [0, 10000, 25000, 50000, 75000, 100000, float('inf')],
                                                    right=False)
    people_income_mode_grouped = people_age_income_mode.groupby(by=['Mode', 'income_group']).agg('count').reset_index()

    # rename df column to num_people due to grouping
    people_income_mode_grouped = people_income_mode_grouped.rename(
        index=str, columns={'PID': 'num_people'})

    # plot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=people_income_mode_grouped, x="Mode", y="num_people", hue="income_group", ax=ax)
    ax.legend(title="Income group")
    ax.set_title("Output - Mode choice by income group")
    return ax


def plot_mode_choice_by_age_group(person_df, trips_df):
    """Plotting the Overall Mode choice By Age Group output

    Parameters
    ----------
    person_df: pandas DataFrame
        parsed and processed xml.files

    trips_df: pandas DataFrame
        parsed and processed xml.files

    Returns
    -------
    ax: matplotlib axes object
    """
    person_df = person_df[['PID', 'Age', 'income']]
    mode_df = trips_df[['PID', 'Mode']]
    people_age_mode = person_df.merge(mode_df, on=['PID'])

    people_age_mode['age_group'] = pd.cut(people_age_mode.Age,
                                                 [0, 18, 30, 40, 50, 60, float('inf')],
                                                 right=False)

    # group the data and reset index to keep as consistent dataframe
    people_age_mode_grouped = people_age_mode.groupby(
        by=['Mode', 'age_group']).agg('count').reset_index()

    # rename df column to num_people due to grouping
    people_age_mode_grouped = people_age_mode_grouped.rename(index=str, columns={'PID': 'num_people'})
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.barplot(data=people_age_mode_grouped, x="Mode", y="num_people", hue="age_group")
    ax.legend(title="Age group")
    plt.title("Output - Mode choice by age group")

    return ax


def plot_average_travel_expenditure_per_trip_per_mode_over_day(legs_df):
    """Plotting the Averge Travel Expenditure Per Trip and By MOde Over THe Day output

    Parameters
    ----------
    legs_df: pandas DataFrame
        parsed and processed xml.files

    Returns
    -------
    ax: matplotlib axes object
    """
    legs_df.loc[:, "trip_cost"] = legs_df.FuelCost.values + legs_df.Fare.values + legs_df.Cost.values - legs_df.Incentive
    legs_df.loc[:, "hour_of_day"] = np.floor(legs_df.Start_time/3600)
    grouped_data = legs_df.groupby(by=["Mode", "hour_of_day"]).agg("mean")["trip_cost"].reset_index()
    fig, ax = plt.subplots(figsize=(18, 8))
    sns.barplot(data=grouped_data, x="hour_of_day", y="trip_cost", hue="Mode", ax=ax, palette="Set2")
    ax.set_xlabel("Hour of the day")
    ax.set_ylabel("Average Cost [$]")
    ax.legend(loc="upper left", title="Mode")
    ax.set_title("Output - Average Travel Expenditure per Trip and by mode over the day")
    return ax


def plot_average_bus_crowding_by_bus_route_by_period_of_day(path_df, trip_to_route, seating_capacities, transit_scale_factor):
    """Plotting the Average hours of bus crowding output

    Parameters
    ----------
    path_df: pandas DataFrame
        parsed and processed xml.files

    trip_to_route: dictionary
        Correspondance between trip_ids and route_ids

    seating_capacities: dictionary
        Correspondance between each bus type and its seating capacity

    transit_scale_factor: float
        Downsizing factor defined in the config file (=0.1 for Sioux Faux)

    Returns
    -------
    ax: matplotlib axes object
        """
    bus_slice_df = path_df.loc[lambda df: df["mode"] == "bus"][["vehicle", "numPassengers",
                                                                "capacity", "departureTime",
                                                                "arrivalTime", "fuel", "vehicleType"]]
    bus_slice_df.loc[:, "route_id"] = bus_slice_df.vehicle.apply(lambda x: trip_to_route[x.split(":")[1]])
    bus_slice_df.loc[:, "serviceTime"] = (bus_slice_df.arrivalTime - bus_slice_df.departureTime) / 3600
    bus_slice_df.loc[:, "seatingCapacity"] = bus_slice_df.vehicleType.apply(lambda x: transit_scale_factor * seating_capacities[x])
    bus_slice_df.loc[:, "passengerOverflow"] = bus_slice_df.numPassengers > bus_slice_df.seatingCapacity
    # AM peak = 7am-10am, PM Peak = 5pm-8pm, Early Morning, Midday, Late Evening = in between
    bus_slice_df.loc[:, "servicePeriod"] = pd.cut(bus_slice_df.departureTime, [0, 25200, 36000, 61200, 72000, 86400],
                                                  labels=["Early Morning", "AM Peak", "Midday", "PM Peak",
                                                          "Late Evening"])

    fig, ax = plt.subplots(figsize=(10, 6))
    grouped_data = \
    bus_slice_df[bus_slice_df.passengerOverflow == True].groupby(["route_id", "servicePeriod"]).agg("sum")[
        "serviceTime"].fillna(0).reset_index()
    sns.barplot(data=grouped_data, x="route_id", y="serviceTime", hue="servicePeriod", ax=ax)
    ax.set_xlabel("Bus Route")
    ax.set_ylabel("Hours of bus crowding")
    ax.legend(loc=(1.02, 0.71), title="Service Period")
    ax.grid(True, which="both")
    ax.set_title("Output - Average Hours of bus crowding by bus route and period of day")
    return ax


def process_travel_time(travel_time_data_path):
    """Processing and reorganizing the data in a dataframe ready for plotting

    Parameters
    ----------
    travel_time_data_path:  PosixPath
        Absolute path of the `{ITER_NUMBER}.averageTravelTimes.csv` input file (located in the
        <output directory>/ITERS/it.<ITER_NUMBER>/ directory of the simulation)

    Returns
    -------
    travel_time: pandas DataFrame
        Average travel_time by mode data that is ready for plotting.

        """
    travel_time = pd.read_csv(travel_time_data_path)
    travel_time = travel_time.set_index("TravelTimeMode\Hour")
    travel_time.rename({"ride_hail": "on_demand ride"}, inplace=True)
    travel_time["mean"] = travel_time.mean(axis=1)
    travel_time["mode"] = travel_time.index
    travel_time = travel_time.drop(labels="others", axis=0)

    return travel_time


def plot_travel_time_by_mode(travel_time_data_path):
    """Plotting the Average Travel Time by Mode output

    Parameters
    ----------
    see process_travel_time()

    Returns
    -------
    ax: matplotlib axes object
    """
    travel_time = process_travel_time(travel_time_data_path)

    fig, ax = plt.subplots()

    fig.set_size_inches(7, 5)
    sns.barplot(x="mode", y="mean", data=travel_time, palette="Set2")
    plt.xlabel("Mode")
    plt.ylabel("Travel time [min]")
    plt.title("Output - Average travel time per trip and by mode")

    return ax


def process_travel_time_over_the_day(travel_time_data_path):
    """Processing and reorganizing the data in a dataframe ready for plotting

    Parameters
    ----------
    travel_time_data_path:  PosixPath
        Absolute path of the `{ITER_NUMBER}.averageTravelTimes.csv` input file (located in the
        <output directory>/ITERS/it.<ITER_NUMBER>/ directory of the simulation)

    Returns
    -------
    travel_time: pandas DataFrame
        Average travel_time by mode and over the day data that is ready for plotting.

        """

    travel_time = pd.read_csv(travel_time_data_path)
    travel_time = travel_time.set_index("TravelTimeMode\Hour")
    travel_time.rename({"ride_hail": "on_demand ride"}, inplace=True)
    travel_time = travel_time.drop(labels="others", axis=0)
    travel_time.reset_index(inplace=True)

    melted_travel_time = pd.melt(travel_time, id_vars="TravelTimeMode\Hour")
    melted_travel_time.columns = ["mode", "hours", "travel time"]
    melted_travel_time = melted_travel_time.sort_values(by="hours")

    melted_travel_time["hours"] = pd.to_numeric(melted_travel_time["hours"])

    return melted_travel_time


def plot_travel_time_over_the_day(travel_time_data_path):
    """Plotting the Average Travel Time by Mode and by Hour of the Day output

    Parameters
    ----------
    see process_travel_time_over_the_day()

    Returns
    -------
    ax: matplotlib axes object
    """
    melted_travel_time = process_travel_time_over_the_day(travel_time_data_path)

    fig, ax = plt.subplots()

    fig.set_size_inches(20, 8.27)
    sns.barplot(ax=ax, x="hours", y="travel time", hue="mode", data=melted_travel_time.sort_values(by="hours"),  palette="Set2")
    plt.legend(loc="upper left", title="Mode")
    plt.xlabel("Hours")
    plt.ylabel("Travel time [min]")
    plt.xlim((0, 30))
    plt.ylim((0, 150))
    plt.yticks(np.arange(0, 151, 10), np.arange(0, 151, 10), fontsize=11)
    plt.xticks(np.arange(0, 31, 1), np.arange(0, 31, 1), fontsize=11)

    plt.title("Output - Average travel time per passenger-trip over the day")

    return ax


def plot_cost_benefits(path_df, legs_df, operational_costs, trip_to_route):
    """Plotting the Costs and Benefits by bus route output

    Parameters
    ----------
    path_df: pandas DataFrame
        parsed and processed xml.files

    legs_df: pandas DataFrame
        parsed and processed xml.files

    operational_costs: dictionary
        Operational costs for each bus vehicle type as defined under "operational_costs" in the
        availableVehicleTypes.csv in the`reference-data` folder of the Starter Kit

    trip_to_route: dictionary
        Correspondance between trip_ids and route_ids

    Returns
    -------
    ax: matplotlib axes object
        """
    bus_slice_df = path_df.loc[lambda df: df["mode"] == "bus"][
        ["vehicle", "numPassengers", "capacity", "departureTime", "arrivalTime", "fuel", "vehicleType"]]
    bus_slice_df.loc[:, "route_id"] = bus_slice_df.vehicle.apply(lambda x: trip_to_route[x.split(":")[1]])
    bus_slice_df.loc[:, "Trip_ID"] = bus_slice_df.vehicle.apply(lambda x: x.split(":")[1])
    bus_slice_df.loc[:, "operational_costs_per_bus"] = bus_slice_df.vehicleType.apply(
        lambda x: operational_costs[x])
    bus_slice_df.loc[:, "serviceTime"] = (bus_slice_df.arrivalTime - bus_slice_df.departureTime) / 3600
    bus_slice_df.loc[:, "operational_costs"] = bus_slice_df.operational_costs_per_bus * bus_slice_df.serviceTime
    bus_slice_df.loc[:, "fuelCosts"] = bus_slice_df.fuel * 0.02


    # return pd.merge(bus_slice_df, trips_df[["Trip_ID", "Fare"]], on="Trip_ID")
    grouped_data = bus_slice_df.groupby(by="route_id").agg("sum")[["operational_costs", "fuelCosts"]]

    fig, ax = plt.subplots(figsize=(8, 6))
    grouped_data.plot.bar(stacked=True, ax=ax)
    plt.title("Costs and Benefits by bus route")
    plt.xlabel("Bus route")
    plt.ylabel("Amount [$]")
    ax.legend(title="Costs and Benefits")
    return ax



####### PROCESS AND PLOT SPATIAL DATA ######

# Defining matsim_network_to_graph(``)

class TravelTimeAccessibilityAnalysis(object):

    def __init__(self,
                 network_file,
                 linkstats_file,
                 population_file,
                 utm_zone):
        self.network_file = network_file
        self.linkstats_file = linkstats_file
        self.population_file = population_file
        self.utm_zone_number = re.match("\d*", utm_zone)
        self.utm_zone_letter = re.match("[N|S]", utm_zone)
        self.poi_dict = self._make_poi_dict()

    def _convert_crs(self, c):
        return utm.to_latlon(c[0], c[1],
                             self.utm_zone_number,
                             self.utm_zone_letter)

    def make_net_for_timerange(self, timerange):
        traveltime_df = self.make_traveltime_df(timerange)
        node_df = make_node_df(self.network_file)
        return create_pandana_net(node_df, traveltime_df)

    def make_pandana_nets(self, poi_types, timeranges, max_time):
        nets = {}
        for label, timerange in timeranges.items():
            net = self.make_net_for_timerange(timerange)
            for poi_type in poi_types:
                net.precompute(max_time)
                poi_locs = np.array(self.poi_dict[poi_type])
                x, y = poi_locs[:, 1], poi_locs[:, 0]
                net.set_pois(poi_type, max_time, 10, x, y)
                nets[label] = net
        return nets

    def make_node_df(self):
        matsimnet = open_xml(self.network_file).getroot()
        nodes = matsimnet[1]
        links = matsimnet[3]
        node_data = []

        # populate node dataframes
        for node in nodes:
            coords = convert_crs((float(node.get('x')), float(node.get('y'))))
            node_data.append([int(node.get('id')), coords[1], coords[0]])
        node_data = np.array(node_data)

        node_df = pd.DataFrame({'x': node_data[:, 1], 'y': node_data[:, 2]}, index=node_data[:, 0].astype(int))
        node_df.index.name = 'id'
        return node_df

    def make_traveltime_df(self, timerange):
        link_df = pd.read_csv(self.linkstats_file, compression='gzip')
        link_df = link_df[link_df.stat == 'AVG']
        link_df.drop(link_df.hour[link_df.hour == '0.0 - 30.0'].index, inplace=True)
        link_df.hour = link_df.hour.astype(float).astype(int)
        traveltime_link_df = link_df[link_df.hour.map(lambda x: x in timerange)].groupby('link').mean()[
            ['from', 'to', 'traveltime']]
        return traveltime_link_df

    def _make_poi_dict(self):
        population_xml = open_xml(self.population_file).getroot()
        persons = population_xml.findall('person')
        poi_dict = defaultdict(list)
        for person in persons:
            for activity in person[1]:
                actType = activity.get('type').lower()
                coords = convert_crs([float(activity.get('x')), float(activity.get('y'))])
                poi_dict[actType].append(coords)
        return poi_dict


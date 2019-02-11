import matplotlib.pyplot as plt


import pandas as pd
import numpy as np
from matplotlib import cm
from matplotlib.cm import ScalarMappable

import seaborn as sns
from pathlib import Path
import tqdm
from time import time
from lxml import etree


def unzip_file(folder_path):
    """Checking if the path points to an existing folder or to its .zip format; if only the .zip format exists,
    it unzips the folder.

    Parameters
    ----------
    folder_path: PosixPath
        Absolute path of the folder of interest.

    Returns
    -------
        Absolute path of the (unzipped) folder of interest.
    """
    import zipfile
    if folder_path.exists():
        return folder_path

    elif Path(str(folder_path) + ".zip").exists():
        zip_folder = zipfile.ZipFile(str(folder_path) + ".zip", 'r')
        zip_folder.extractall(folder_path)
        zip_folder.close()
        return folder_path

    else:
        raise FileNotFoundError(f"{folder_path} does not exist")


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
    min_max = df[name_column].str.replace("[", "").str.replace("]", "").str.replace("(", "").str.replace(")", "").str.split(":", expand=True)
    df["min_{0}".format(name_column)] = min_max.iloc[:, 0].astype(int)
    df["max_{0}".format(name_column)] = min_max.iloc[:, 1].astype(int)

    return df


def process_incentives_data(input_file_path, max_incentive):
    """ Processing and reorganizing the data in an input dataframe to be ready for plotting

    Parameters
    ----------
    input_file_path: PosixPath
        Absolute path of the ModeIncentives.csv input file

    max_incentive: float
        Maximum amount allowed for an incentive as defined in the Starter Kit "Inputs Specifications" page

    Returns
    -------
    incentives: pandas dataframe
        Incentives input data that is ready for plotting
    """
    incentives = pd.read_csv(input_file_path)
    incentives["amount"] = incentives["amount"].astype(float)

    # Completing the dataframe with the missing incentivized modes (so that they appear in the plot)
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


def plot_incentives_inputs(input_file_path, max_incentive, max_age, max_income ):
    """Plot the incentives input

    Parameters
    ----------
    input_file_path: PosixPath
        Absolute path of the ModeIncentives.csv input file

    max_incentive: float
        Maximum amount allowed for an incentive as defined in the Starter Kit "Inputs Specifications" page

    Returns
    -------
    ax: matplotlib axes object

    """
    incentives = process_incentives_data(input_file_path, max_incentive)

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

    plt.yticks(fontsize=11)
    plt.suptitle("Input - Incentives by age and income group", fontweight="bold", fontsize=15)

    sm = ScalarMappable(cmap=my_cmap, norm=plt.Normalize(0, np.max(incentives["amount"])))
    sm.set_array([])
    sm.set_clim(0, max_incentive)
    cbar = fig.colorbar(sm, ticks=[i for i in range(0, max_incentive+1, 10)])
    cbar.set_label('Incentive amount [$]', rotation=270, labelpad=25)

    return ax


def process_bus_data(input_file_path, route_ids, buses_list, agency_ids):
    """Processing and reorganizing the data in an input dataframe to be ready for plotting

    Parameters
    ----------
    input_file_path: PosixPath
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
    fleet_mix = pd.read_csv(input_file_path)

    if fleet_mix.empty:
        fleet_mix = pd.DataFrame([[agency_id, f"{route_id}", "BUS-DEFAULT"] for route_id in route_ids for agency_id in agency_ids],
                                 columns=["agencyId", "routeId", "vehicleTypeId"])
    else:
        df = pd.DataFrame([217, "1", "BUS-DEFAULT"]).T
        df.columns = ["agencyId", "routeId", "vehicleTypeId"]

    # Adding the missing bus types in the dataframe so that they appear in the plot
    for bus in buses_list:
        if bus not in fleet_mix["vehicleTypeId"].values:
            df["vehicleTypeId"] = bus
            fleet_mix = fleet_mix.append(df)

    # Adding the missing bus routes in the dataframe so that they appear in the plot
    fleet_mix["routeId"] = fleet_mix["routeId"].astype(int)

    df = pd.DataFrame([217, "", "BUS-DEFAULT"]).T
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



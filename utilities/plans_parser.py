import pandas as pd
import numpy as np

from lxml import etree
from data_parsing import extract_dataframe

import gzip
from collections import defaultdict


def open_xml(path):
    # Open xml and xml.gz files into ElementTree
    if str(path).endswith('.gz'):
        return etree.parse(gzip.open(str(path)))
    else:
        return etree.parse(str(path))


def unzip_file(path):
    if path.endswith('.gz'):
        return gzip.open(path)
    else:
        return path


def parse_bus_fare_input(bus_fare_datas, route_ids):
    # bus_fare_data is the path to the submission input csv: "submission-inputs/MassTransitFares.csv"
    # route_ids is the list of routeIds produced in the Viz notebook

    bus_fare_data = pd.read_csv(bus_fare_datas)
    # returns bus_fare_dict: a dataframe with rows = ages and columns = routes
    bus_fare_dict = pd.DataFrame(np.zeros((120, len(route_ids))), columns=route_ids)
    routes = bus_fare_data['route_id'].unique()
    for r in routes:
        if np.isnan(r):
            cols = route_ids
        else:
            cols = int(r)
        # get all fare rows for this route:
        r_fares = bus_fare_data.loc[np.isnan(bus_fare_data['routeId']),]
        for i, row in r_fares.iterrows():
            print(row)
            age_group = row['age']
            left = age_group[0]
            ages = age_group[1:-1].split(':')
            right = age_group[-1]
            if left == '(':
                min_a = int(ages[0]) + 1
            else:
                min_a = int(ages[0])
            if right == ')':
                max_a = int(ages[1]) - 1
            else:
                max_a = int(ages[1])
            bus_fare_dict.loc[min_a:max_a, cols] = float(row['amount'])

    return bus_fare_dict


def calc_fuel_costs(legs_df, fuel_cost_dict):
    # legs_df: legs_dataframe
    # fuel_cost_dict: {fuel_type: $/MJoule}
    # returns: legs_df augmented with an additional column of estimated fuel costs

    legs_df.loc[:, "FuelCost"] = np.zeros(legs_df.shape[0])
    for f in ['Gasoline', 'Diesel']:
        legs_df.loc[legs_df["fuelType"] == f, "FuelCost"] = (pd.to_numeric(
            legs_df.loc[legs_df["fuelType"] == f, "FuelCost"]) * float(fuel_cost_dict[f])) / 1000000
    return legs_df


def calc_transit_fares(row,bus_fare_dict,person_df,trip_to_route):
    pid = row['PID']
    age = person_df.loc[person_df['PID']==pid,'Age']
    vehicle = row['Veh']
    route = trip_to_route[vehicle.split(':')[1]]
    fare = bus_fare_dict.loc[age,route]
    return fare


def calc_fares(legs_df, ride_hail_fares):
    # legs_df: legs_dataframe
    # ride_hail_fares: {'base': $, 'duration': $/hour, 'distance': $/km}
    # transit_fares isnt being used currently - would need to be updated to compute fare based on age
    # returns: legs_df augmented with an additional column of estimated transit and on-demand ride fares

    legs_df["Fare"] = np.zeros(legs_df.shape[0])
    legs_df.loc[legs_df["Mode"] == 'walk_transit', "Fare"] = 1.5
    legs_df.loc[legs_df["Mode"] == 'drive_transit', "Fare"] = 1.5
    legs_df.loc[legs_df["Mode"] == 'OnDemand_ride', "Fare"] = ride_hail_fares['base'] + (
                pd.to_timedelta(legs_df['Duration']).dt.seconds / 60) * float(ride_hail_fares['duration']) + (                                                           pd.to_numeric(legs_df['Distance']) / 1000) * (
                                                                  0.621371) * float(ride_hail_fares['distance'])
    return legs_df


def one_path(path_trav, leg_id, pid, trip_id):
    # extracts leg data from path traversal
    # returns a leg_dataframe row

    l_row = path_trav
    leg_id_this = leg_id + l_row.name
    leg_id_full = trip_id + "_l-" + str(leg_id)
    veh_id = l_row["vehicle"]
    leg_start_time = l_row['departureTime']
    veh_type = l_row['vehicleType']
    distance = l_row['length']
    leg_end_time = l_row['arrivalTime']
    leg_duration = int(leg_end_time) - int(leg_start_time)
    leg_path = l_row['links']
    leg_mode = l_row['mode']
    leg_fuel = l_row['fuel']
    leg_fuel_type = l_row['fuelType']

    # return the leg record
    return [pid, trip_id, leg_id_full, leg_mode, veh_id, veh_type, leg_start_time, leg_end_time, leg_duration, distance,
            leg_path, leg_fuel, leg_fuel_type]


def parse_transit_trips(row, path_traversal_events, bus_path_traversal_events, enter_veh_events):
    # inputs:
    # row: a row from transit_trips_df
    # path_traversal_events: non-transit path traversal df
    # bus_path_traversal_events: transit path traversal df
    # enter_veh_events: enter vehicle events

    leg_array = []
    pid = row['PID']
    trip_id = row['Trip_ID']
    start_time = row['Start_time']
    duration = row['Duration']
    end_time = row['End_time']
    mode = row['Mode']
    # initiate the leg ID counter
    leg_id = 0
    # get all path traversals occuring within the time frame of this trip in which the driver is the person making this trip
    path_trav = path_traversal_events.loc[
        (path_traversal_events['driver'] == pid) & (path_traversal_events['arrivalTime'] <= end_time) & (
                    path_traversal_events['departureTime'] >= start_time.total_seconds()),]
    path_trav = path_trav.reset_index(drop=True)
    # get the vehicle entry events corresponding to this person during the time frame of this trip
    veh_entries = enter_veh_events.loc[
        (enter_veh_events['person'] == pid) & (enter_veh_events['time'] >= start_time.total_seconds()) & (
                    enter_veh_events['time'] <= end_time),]
    # get bus entry events for this person & trip
    bus_entries = veh_entries[veh_entries['vehicle'].str.startswith('siouxareametro-sd-us:', na=False)]

    if len(bus_entries) > 0:
        for indx, bus_entry in bus_entries.iterrows():
            # get all path traversals occuring before the bus entry
            prev_path_trav = path_trav.loc[(path_trav['arrivalTime'] <= bus_entry['time']),]
            # get all path traversals occuring after the bus entry
            post_path_trav = path_trav.loc[(path_trav['arrivalTime'] > bus_entry['time']),]
            prev_path_trav = prev_path_trav.reset_index(drop=True)
            post_path_trav = post_path_trav.reset_index(drop=True)
            # iterate through the path traversals prior to the bus entry
            these_legs = prev_path_trav.apply(lambda row1: one_path(row1, leg_id, pid, trip_id), axis=1)
            leg_array.extend(these_legs)

            # record transit leg
            leg_id += 1
            leg_id_full = trip_id + "_l-" + str(leg_id)
            veh_id = bus_entry['vehicle']
            leg_start_time = int(bus_entry['time'])
            leg_end_time = int(post_path_trav['departureTime'].values[0])
            leg_duration = int(leg_end_time - bus_entry['time'])
            # find the path traversals of the bus corresponding to the bus entry for this trip, occuring between the last prev_path_traversal and the first post_path_traversal
            bus_path_trav = bus_path_traversal_events.loc[(bus_path_traversal_events['vehicle'] == veh_id) & (
                        bus_path_traversal_events['arrivalTime'] <= leg_end_time) & (bus_path_traversal_events[
                                                                                         'departureTime'] >= leg_start_time),]

            if len(bus_path_trav) > 0:
                veh_type = bus_path_trav['vehicleType'].values[0]
                distance = bus_path_trav['length'].sum()
                leg_path = [path['links'] for p, path in bus_path_trav.iterrows()]
                leg_mode = bus_path_trav['mode'].values[0]
                leg_fuel = 0
                leg_fuel_type = 'Diesel'
                leg_array.append(
                    [pid, trip_id, leg_id_full, leg_mode, veh_id, veh_type, leg_start_time, leg_end_time, leg_duration,
                     distance, leg_path, leg_fuel, leg_fuel_type])

            # iterate through the path traversals after the bus entry
            these_legs = post_path_trav.apply(lambda row1: one_path(row1, leg_id, pid, trip_id), axis=1)
            leg_array.extend(these_legs)

    # if the agent underwent replanning, there will be no bus entry
    else:
        leg_array = parse_walk_car_trips(row, path_traversal_events, enter_veh_events)

    return leg_array


def parse_walk_car_trips(row, path_traversal_events, enter_veh_events):
    # inputs:
    # row: a row from transit_trips_df
    # path_traversal_events: non-transit path traversal df
    # person_costs: person cost events df
    # enter_veh_events: enter vehicle events

    leg_array = []
    pid = row['PID']
    trip_id = row['Trip_ID']
    start_time = row['Start_time']
    duration = row['Duration']
    end_time = row['End_time']
    mode = row['Mode']
    # initiate the leg ID counter
    leg_id = 0

    # get all path traversals occuring within the time frame of this trip in which the driver is the person making this trip

    path_trav = path_traversal_events.loc[
        (path_traversal_events['driver'] == pid) & (path_traversal_events['arrivalTime'] <= end_time) & (
                    path_traversal_events['departureTime'] >= start_time.total_seconds()),]
    path_trav.reset_index(drop=True, inplace=True)
    # iterate through the path traversals
    if len(path_trav > 0):
        these_legs = path_trav.apply(lambda row: one_path(row, leg_id, pid, trip_id), axis=1)
        leg_array.extend(these_legs)
    return leg_array


def parse_ridehail_trips(row, path_traversal_events, enter_veh_events):
    # inputs:
    # row: a row from transit_trips_df
    # path_traversal_events: non-transit path traversal df
    # person_costs: person cost events df
    # enter_veh_events: enter vehicle events

    leg_array = []
    pid = row['PID']
    trip_id = row['Trip_ID']
    start_time = row['Start_time']
    duration = row['Duration']
    end_time = row['End_time']
    mode = row['Mode']
    # initiate the leg ID counter
    leg_id = 0

    # get all vehicle entry events corresponding to this person during the time frame of this trip, not including those corresponding to a walking leg
    veh_entry = enter_veh_events.loc[
        (enter_veh_events['person'] == pid) & (enter_veh_events['time'] >= start_time.total_seconds()) & (
                    enter_veh_events['time'] <= end_time),]
    veh_entry2 = veh_entry.loc[(veh_entry['vehicle'] != 'body-' + pid),]
    veh_id = veh_entry2['vehicle'].item()
    leg_start_time = veh_entry2['time'].item()
    # get the path traversal corresponding to this ridehail trip
    path_trav = path_traversal_events.loc[(path_traversal_events['vehicle'] == veh_id) & (
                path_traversal_events['departureTime'] == int(leg_start_time)) & (
                                                      path_traversal_events['numPassengers'] > 0),]
    leg_id += 1
    # create leg ID
    leg_id_full = trip_id + "_l-" + str(leg_id)
    if len(path_trav) > 0:
        veh_type = path_trav['vehicleType'].values[0]
        distance = path_trav['length'].item()
        leg_end_time = path_trav['arrivalTime'].item()
        leg_duration = int(leg_end_time) - int(leg_start_time)
        leg_path = path_trav['links'].item()
        leg_mode = 'OnDemand_ride'
        leg_fuel = path_trav['fuel'].item()
        leg_fuel_type = path_trav['fuelType'].item()
        leg_array.append(
            [pid, trip_id, leg_id_full, leg_mode, veh_id, veh_type, leg_start_time, leg_end_time, leg_duration,
             distance, leg_path, leg_fuel, leg_fuel_type])
    return leg_array


def get_person_output(out_plans, persons, hhds, output_folder):
    # parses the outputPlans, outputPersonAttributes and the outputHouseholds
    # to create the households and persons tables (hhd_dataframe and persons_dataframe)
    # saves the household dataframe to csv
    # outputs the augmented persons dataframe, including all individual and household attributes for each person

    # get roots of all xmls
    persons_root = persons.getroot()
    out_plans_root = out_plans.getroot()
    hhds_root = hhds.getroot()
    hhd_array = []
    person_array = []
    net = []

    # iterate through households
    for hhd in hhds_root.getchildren():
        hhd_id = hhd.get('id').strip()
        hhd_children = hhd.getchildren()
        # check for vehicles; record household attributes
        if len(hhd_children) == 3:
            members = hhd_children[0]
            vehicles = hhd_children[1]
            income = hhd_children[2]
            vehs = vehicles.getchildren()
            num_veh = len(vehs)
        else:
            members = hhd_children[0]
            vehicles = []
            income = hhd_children[1]
            num_veh = 0
        hhd_income = income.text.strip()
        # get list of persons in household and make a record of each person
        mems = members.getchildren()
        for person in mems:
            pid = person.attrib['refId'].strip()
            hhd_array.append([pid, hhd_id, num_veh, hhd_income])
    # convert array to dataframe and save
    hhd_df = pd.DataFrame(hhd_array, columns=['PID', 'hhd_ID', 'Num_vehicles', 'Hhd_income'])
    hhd_df.to_csv(str(output_folder) + "/hhd_dataframe.csv")

    # iterate through persons in outputPlans and make a record of each person
    for person in out_plans_root.findall('./person'):
        pid = person.get('id')
        attributes = person.findall('./attributes')[0]
        age = int(attributes.findall('./attribute[@name="age"]')[0].text)
        sex = attributes.findall('./attribute[@name="sex"]')[0].text
        plan = person.findall('./plan')[0]
        home = plan.findall('./activity')[0]
        act_x = home.get('x')
        act_y = home.get('y')
        person_array.append([pid, age, sex, act_x, act_y])
    # convert person array to dataframe
    person_df = pd.DataFrame(person_array, columns=['PID', 'Age', 'Sex', 'X', 'Y'])

    # iterate through persons in personAttributes
    pop = persons_root.getchildren()
    for person in pop:
        pid = person.get('id')
        attributes = person.findall("./attribute")
        res = {}
        res['PID'] = pid
        for attribute in attributes:
            res[attribute.attrib['name']] = attribute.text
        net.append(res)
    # convert attribute array to dataframe
    net_df = pd.DataFrame(net)
    # set the index of all dataframes to PID (person ID)
    person_df.set_index('PID', inplace=True)
    net_df.set_index('PID', inplace=True)
    hhd_df.set_index('PID', inplace=True)
    # join attribute info to persons
    person_df_full = person_df.join(net_df)
    # join household info to persons
    person_df_full_new = person_df_full.join(hhd_df)
    return person_df_full_new


def get_activity_trip_output(exp_plans):
    # parses the experiencedPlans to create the trips and activities dataframes (trips_dataframe and activities_dataframe)
    # outputs the trips and activities dataframes

    # get root of experiencedPlans xml
    plans_root = exp_plans.getroot()
    acts_array = []
    trip_array = []

    # iterate through persons, recording activities and trips for each person
    for person in plans_root.findall('./person'):
        # we use the person ID from the raw output
        pid = person.get('id')
        plan = person.getchildren()[0]
        activities = plan.findall('./activity')
        legs = plan.findall('./leg')

        # initialize activity and trip ID counters (we create activity and trip IDs using these)
        act_id = 0
        trip_id = 0
        purposes = []

        # iterate through activities and make record of each activity
        for activity in activities:
            act_id += 1
            # create activity ID
            activity_id = pid + "_a-" + str(act_id)
            act_type = activity.get('type')
            if activity.get('start_time') is None:
                act_start_time = None
            else:
                act_start_time = activity.get('start_time')
            if activity.get('end_time') is None:
                act_end_time = None
            else:
                act_end_time = activity.get('end_time')
            # record all activity types to determine trip purposes
            purposes.append([act_type])
            acts_array.append([pid, activity_id, act_type, act_start_time, act_end_time])

        # iterate through trips (called legs in the Plans) and make record of each trip
        for trip in legs:
            trip_id += 1
            # create trip ID
            trip_id_full = pid + "_t-" + str(trip_id)
            # record activity IDs for origin and destination activities of the trip
            o_act_id = pid + "_a-" + str(trip_id)
            d_act_id = pid + "_a-" + str(trip_id + 1)
            # identify the activity type of the trip destination to record as the trip purpose
            purpose = purposes[trip_id][0]
            mode = trip.get('mode')
            dep_time = trip.get('dep_time')
            duration = trip.get('trav_time')
            route = trip.find('./route')
            distance = route.get('distance')
            path = route.text
            trip_array.append(
                [pid, trip_id_full, o_act_id, d_act_id, purpose, mode, dep_time, duration, distance, path])
    # convert the activity and trip arrays to dataframes
    acts_df = pd.DataFrame(acts_array, columns=['PID', 'Act_ID', 'Type', 'Start_time', 'End_time'])
    trips_df = pd.DataFrame(trip_array,
                            columns=['PID', 'Trip_ID', 'O_Act_ID', 'D_Act_ID', 'Purpose', 'Mode', 'Start_time',
                                     'Duration', 'Distance', 'Path'])
    return acts_df, trips_df


def get_events_output(events):
    # parses the outputEvents xml to a datframe
    event_data = {}
    root = events.getroot()
    for event in root.getchildren():
        add_event_data_to_library(event, event_data)
    return pd.DataFrame(event_data)


def add_event_data_to_library(event, event_data):
    attrib = event.attrib
    event_type = attrib['type']
    if event_type not in event_data:
        dd = defaultdict(list)
        event_data[event_type] = dd
    else:
        dd = event_data[event_type]
    for k, v in attrib.items():
        dd[k].append(v)


def get_legs_output(events_df, trips_df):
    # creates a dataframe of trip legs using the events dataframe; creates and saves a pathTraversal dataframe to csv
    # outputs the legs dataframe

    # convert trip times to timedelta; calculate end time of trips
    trips_df['Start_time'] = pd.to_timedelta(trips_df['Start_time'])
    trips_df['Duration'] = pd.to_timedelta(trips_df['Duration'])
    trips_df['End_time'] = trips_df['Start_time'].dt.seconds + trips_df['Duration'].dt.seconds + (
                3600 * 24 * trips_df['Start_time'].dt.days)
    # get all relevant personEntersVehicle events (those occuring at time ==0 are all ridehail/bus drivers)
    enter_veh_events = events_df.loc[(events_df['type'] == 'PersonEntersVehicle') & (events_df['time'] > 0),]
    # get all path traversal events (all vehicle movements, and all person walk movements)
    path_traversal_events_full = events_df.loc[(events_df['type'] == 'PathTraversal') & (events_df['length'] > 0),]
    path_traversal_events_full = path_traversal_events_full.reset_index(drop=True)
    path_traversal_events_full = path_traversal_events_full[
        ['time', 'type', 'person', 'vehicle', 'driver', 'vehicleType', 'length',
         'numPassengers', 'departureTime', 'arrivalTime', 'mode', 'links',
         'fuelType', 'fuel', 'capacity', 'startX', 'startY', 'endX', 'endY',
         'endLegFuelLevel', 'seatingCapacity']]

    # filter for bus path traversals only
    bus_path_traversal_events = path_traversal_events_full.loc[
        path_traversal_events_full['vehicleType'] == "BUS-DEFAULT",]
    # filter for car & body path traversals only
    path_traversal_events = path_traversal_events_full.loc[path_traversal_events_full['vehicleType'] != "BUS-DEFAULT",]
    # get all PersonCost events (record the expenditures of persons during a trip)
    # person_costs = events_df.loc[events_df['type']=='PersonCost',]
    legs_array = []

    # record all legs correspondng to transit trips
    transit_trips_df = trips_df.loc[(trips_df['Mode'] == 'drive_transit') | (trips_df['Mode'] == 'walk_transit'),]
    transit_legs_array = transit_trips_df.apply(
        lambda row: parse_transit_trips(row, path_traversal_events, bus_path_traversal_events, enter_veh_events),
        axis=1)
    for bit in transit_legs_array.tolist():
        legs_array.extend(tid for tid in bit)
    # record all legs correspondng to walk and car trips
    walk_car_trips_df = trips_df.loc[(trips_df['Mode'] == 'car') | (trips_df['Mode'] == 'walk'),]
    walk_car_legs_array = walk_car_trips_df.apply(
        lambda row: parse_walk_car_trips(row, path_traversal_events, enter_veh_events), axis=1)
    for bit in walk_car_legs_array.tolist():
        legs_array.extend(tid for tid in bit)
        # record all legs correspondng to ridehail trips
    ridehail_trips_df = trips_df.loc[(trips_df['Mode'] == 'ride_hail'),]
    ridehail_legs_array = ridehail_trips_df.apply(
        lambda row: parse_ridehail_trips(row, path_traversal_events, enter_veh_events), axis=1)
    for bit in ridehail_legs_array.tolist():
        legs_array.extend(tid for tid in bit)
    # convert the leg array to a dataframe
    legs_df = pd.DataFrame(legs_array,
                           columns=['PID', 'Trip_ID', 'Leg_ID', 'Mode', 'Veh', 'Veh_type', 'Start_time', 'End_time',
                                    'Duration', 'Distance', 'Path', 'Fuel', 'fuelType'])

    return legs_df, path_traversal_events_full


def extract_person_dataframes(out_plans_path, persons_path, hhd_path, output_folder):
    # opens the outputPlans, outputPersons, and outputHouseholds and passes the xml files to get_person_output
    # returns the persons_dataframe

    out_plans_xml = open_xml(out_plans_path)
    persons_xml = open_xml(persons_path)
    hhd_xml = open_xml(hhd_path)
    persons_df = get_person_output(out_plans_xml, persons_xml, hhd_xml,output_folder)
    persons_df.to_csv(str(output_folder) + "/persons_dataframe.csv")
    return persons_df


def extract_plans_dataframes(plans_path, output_folder):
    # opens the experiencedPlans and passes the xml file to get_activity_trip_output
    # returns the actitivities_dataframe and trips_dataframe

    plans_xml = open_xml(plans_path)
    acts_df, trips_df = get_activity_trip_output(plans_xml)
    acts_df.to_csv(str(output_folder) + "/activities_dataframe.csv")
    return acts_df, trips_df


def extract_legs_dataframes(events_path, trips_df, bus_fare_dict, person_df, trip_to_route, output_folder):
    # opens the outputevents and passes the xml file to get_legs_output
    # augments the legs dataframe with estimates of the fuelcosts and fares for each leg
    # returns the legs_dataframe

    all_events_df = extract_dataframe(str(events_path))
    fuel_cost_dict = {'Gasoline': 0.03, 'Diesel': 0.02, 'Electricity': 0.01, 'Food': 0}
    legs_df, path_traversal_df = get_legs_output(all_events_df, trips_df)
    path_traversal_df_new = calc_fuel_costs(path_traversal_df, fuel_cost_dict)
    path_traversal_df_new.to_csv(str(output_folder) + '/path_traversals_dataframe.csv')
    print("path_traversals_dataframe.csv generated")
    legs_df_new = calc_fuel_costs(legs_df, fuel_cost_dict)
    ride_hail_fares = {'base': 0.0, 'distance': 1.0, 'duration': 0.5}
    legs_df_new.to_csv(str(output_folder) + '/legs_df_WIP2.csv')

    legs_df_new_new = calc_fares(legs_df_new, ride_hail_fares)
    legs_df.to_csv(str(output_folder) + '/legs_dataframe.csv')
    return legs_df_new_new


def label_trip_mode(modes):
    if ('walk' in modes) and ('car' in modes) and ('bus' in modes):
        return 'drive_transit'
    elif ('car' in modes) and ('bus' in modes):
        return 'drive_transit'
    elif ('walk' in modes) and ('bus' in modes):
        return 'walk_transit'
    elif ('walk' in modes) and ('car' in modes):
        return 'drive'
    elif ('car' == modes):
        return 'car'
    elif ('OnDemand_ride' in modes):
        return 'OnDemand_ride'
    elif ('walk' == modes):
        return 'walk'
    else:
        print(modes)


def merge_legs_trips(legs_df,trips_df):
    trips_df = trips_df[ ['PID', 'Trip_ID', 'O_Act_ID', 'D_Act_ID', 'Purpose',
       'Mode']]
    trips_df.columns = ['PID', 'Trip_ID', 'O_Act_ID', 'D_Act_ID', 'Purpose',
       'plannedTripMode']
    legs_grouped = legs_df.groupby("Trip_ID")
    unique_modes = legs_grouped['Mode'].unique()
    unique_modes_df = pd.DataFrame(unique_modes)
    unique_modes_df.columns = ['legModes']
    merged_trips = trips_df.merge(legs_grouped['Duration','Distance','Fuel','FuelCost','Fare'].sum(),on='Trip_ID')
    merged_trips = merged_trips.merge(unique_modes_df,on='Trip_ID')
    legs_grouped_start_min = pd.DataFrame(legs_grouped['Start_time'].min())
    legs_grouped_end_max = pd.DataFrame(legs_grouped['End_time'].max())
    merged_trips= merged_trips.merge(legs_grouped_start_min,on='Trip_ID')
    merged_trips= merged_trips.merge(legs_grouped_end_max,on='Trip_ID')
    merged_trips['realizedTripMode'] = merged_trips['legModes'].apply(lambda row: label_trip_mode(row))
    return merged_trips


def output_parse(output_plans_data, persons_data, hhd_data, plans_data, events_data, bus_fares_data, route_ids, trip_to_route, output_folder):
    person_df = extract_person_dataframes(output_plans_data, persons_data, hhd_data, output_folder)
    print("person_dataframe.csv generated")
    activities_df, trips_df = extract_plans_dataframes(plans_data, output_folder)
    bus_fare_dict = parse_bus_fare_input(bus_fares_data, route_ids)
    print("activities_dataframe.csv generated")
    legs_df = extract_legs_dataframes(events_data,trips_df,bus_fare_dict, person_df, trip_to_route, output_folder)
    print("legs_dataframe.csv generated")
    final_trips_df = merge_legs_trips(legs_df, trips_df)
    final_trips_df.to_csv(str(output_folder) +'/trips_dataframe.csv')
    print("trips_dataframe.csv generated")
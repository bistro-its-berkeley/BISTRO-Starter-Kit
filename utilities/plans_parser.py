import datetime
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


def calc_fuel_costs(legs_df, fuel_cost_dict):
    # legs_df: legs_dataframe
    # fuel_cost_dict: {fuel_type: $/MJoule}
    # returns: legs_df augmented with an additional column of estimated fuel costs

    legs_df["FuelCost"] = np.zeros(legs_df.shape[0])
    for f in ['Gasoline', 'Diesel']:
        legs_df.loc[legs_df["FuelType"] == f, "FuelCost"] = (pd.to_numeric(
            legs_df.loc[legs_df["FuelType"] == f, "Fuel"]) * float(fuel_cost_dict[f])) / 1000000
    return legs_df


def calc_fares(legs_df, ride_hail_fares):
    # legs_df: legs_dataframe
    # ride_hail_fares: {'base': $, 'duration': $/hour, 'distance': $/km}
    # transit_fares isnt being used currently - would need to be updated to compute fare based on age
    # returns: legs_df augmented with an additional column of estimated transit and on-demand ride fares

    legs_df["Fare"] = np.zeros(legs_df.shape[0])
    legs_df.loc[legs_df["Mode"] == 'walk_transit', "Fare"] = 1.5
    legs_df.loc[legs_df["Mode"] == 'drive_transit', "Fare"] = 1.5
    legs_df.loc[legs_df["Mode"] == 'OnDemand_ride', "Fare"] = ride_hail_fares['base'] + (
                pd.to_timedelta(legs_df['Duration']).dt.seconds / 60) * float(ride_hail_fares['duration']) + (
                                                                          pd.to_numeric(legs_df['Distance']) / 1000) * (
                                                                  0.621371) * float(ride_hail_fares['distance'])
    return legs_df


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


def get_legs_output(events_df, trips_df, output_folder):
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
    path_traversal_events = events_df.loc[events_df['type'] == 'PathTraversal',]
    path_traversal_events.to_csv(str(output_folder) + "/path_traversals_dataframe.csv")
    # get all non-transit path traversals
    path_traversal_events = path_traversal_events.loc[path_traversal_events['vehicleType'] != "BUS-DEFAULT",]
    # get all PersonCost events (record the expenditures of persons during a trip)
    person_costs = events_df.loc[events_df['type'] == 'PersonCost',]

    legs_array = []

    # iterate through all trips and make a record of each leg within the trip
    for index, row in trips_df.iterrows():
        # if index % 1000 == 0:
        #     print(index)
        #     print(datetime.datetime.now())
        pid = row['PID']
        trip_id = row['Trip_ID']
        start_time = row['Start_time']
        duration = row['Duration']
        end_time = row['End_time']
        mode = row['Mode']
        # initiate the leg ID counter
        leg_id = 0

        # trips using walk or car can be linked directly to pathTraversals with driver==PID (transit is more tricky; better handling TBD)
        if (mode == 'car') or (mode == 'walk') or (mode == 'drive_transit') or (mode == 'walk_transit'):
            # get all path traversals occuring within the time frame of this trip in which the driver is the person making this trip
            path_trav = path_traversal_events.loc[
                (path_traversal_events['driver'] == pid) & (path_traversal_events['arrivalTime'] <= end_time) & (
                            path_traversal_events['departureTime'] >= start_time.total_seconds()) & (
                            path_traversal_events['length'] > 0),]
            # get all person costs corresponding to this person during the time frame of this trip
            person_cost = person_costs.loc[
                (person_costs['person'] == pid) & (person_costs['time'] >= start_time.total_seconds()) & (
                            person_costs['time'] <= end_time),]
            # iterate through the path traversals
            for x, l_row in path_trav.iterrows():
                leg_id += 1
                # create leg ID
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
                p_cost = person_cost.loc[(person_cost['time'] == float(l_row['arrivalTime'])),]
                # record the person cost values for car legs
                if (leg_mode != 'walk') & (len(p_cost) > 0):
                    cost = p_cost['netCost'].values[0]
                    incentive = p_cost['incentive'].values[0]
                else:
                    cost = 0
                    incentive = 0
                # record the leg
                legs_array.append(
                    [pid, trip_id, leg_id_full, leg_mode, veh_id, veh_type, leg_start_time, leg_end_time, leg_duration,
                     distance, leg_path, leg_fuel, leg_fuel_type, cost, incentive])
            # check for non-car costs (i.e., for transit)
            non_car_cost = person_cost.loc[(person_cost['mode'] != 'car'),]
            if len(non_car_cost) > 0:
                # get the vehicle entry events corresponding to this person during the time frame of this trip
                veh_entries = enter_veh_events.loc[
                    (enter_veh_events['person'] == pid) & (enter_veh_events['time'] >= start_time.total_seconds()) & (
                                enter_veh_events['time'] <= end_time),]
                # iterate through any non-car costs
                for indx, c in non_car_cost.iterrows():
                    # get bus vehicle entry events corresponding to the personCost (if bus_entry is 0, the non_car_cost would be for walking and produces 0 values)
                    bus_entry = veh_entries[veh_entries['time'] == c['time']]
                    # for bus entry events, record the person cost, the vehicle id of the bus, etc.
                    if len(bus_entry) > 0:
                        # (bus_entry['vehicle'] != "body-"+pid).item():
                        leg_id = 'transit'
                        leg_id_full = trip_id + "_l-" + str(leg_id)
                        veh_id = bus_entry['vehicle'].item()
                        leg_start_time = c['time']
                        veh_type = 'BUS'
                        distance = 0
                        leg_duration = 0
                        leg_end_time = 0
                        leg_path = 'unknown'
                        leg_mode = c['mode']
                        leg_fuel = 0
                        leg_fuel_type = 'unknown'
                        cost = c['netCost']
                        incentive = c['incentive']
                        legs_array.append(
                            [pid, trip_id, leg_id_full, leg_mode, veh_id, veh_type, leg_start_time, leg_end_time,
                             leg_duration, distance, leg_path, leg_fuel, leg_fuel_type, cost, incentive])
        # trips using ride_hail
        elif (mode == 'ride_hail'):
            # get all vehicle entry events corresponding to this person during the time frame of this trip, not including those corresponding to a walking leg
            veh_entry = enter_veh_events.loc[
                (enter_veh_events['person'] == pid) & (enter_veh_events['time'] >= start_time.total_seconds()) & (
                            enter_veh_events['time'] <= end_time),]
            veh_entry2 = veh_entry.loc[(veh_entry['vehicle'] != 'body-' + pid),]
            veh_id = veh_entry2['vehicle'].item()
            leg_start_time = veh_entry2['time'].item()
            # get the personCost corresponding to this ridehail trip
            person_cost = person_costs.loc[(person_costs['person'] == pid) & (person_costs['time'] == leg_start_time),]
            # get the path traversal corresponding to this ridehail trip
            path_trav = path_traversal_events.loc[(path_traversal_events['vehicle'] == veh_id) & (
                        path_traversal_events['departureTime'] == int(leg_start_time)) & (
                                                              path_traversal_events['numPassengers'] > 0),]
            leg_id += 1
            # create leg ID
            leg_id_full = trip_id + "_l-" + str(leg_id)
            veh_type = path_trav['vehicleType'].item()
            distance = path_trav['length'].item()
            leg_end_time = path_trav['arrivalTime'].item()
            leg_duration = int(leg_end_time) - int(leg_start_time)
            leg_path = path_trav['links'].item()
            leg_mode = 'OnDemand_ride'
            leg_fuel = path_trav['fuel'].item()
            leg_fuel_type = path_trav['fuelType'].item()
            cost = person_cost['netCost'].values[0]
            incentive = person_cost['incentive'].values[0]
            legs_array.append(
                [pid, trip_id, leg_id_full, leg_mode, veh_id, veh_type, leg_start_time, leg_end_time, leg_duration,
                 distance, leg_path, leg_fuel, leg_fuel_type, cost, incentive])
    # convert the leg array to a dataframe
    legs_df = pd.DataFrame(legs_array,
                           columns=['PID', 'Trip_ID', 'Leg_ID', 'Mode', 'Veh', 'Veh_type', 'Start_time', 'End_time',
                                    'Duration', 'Distance', 'Path', 'Fuel', 'FuelType', 'Cost', 'Incentive'])

    return legs_df


def extract_person_dataframes(out_plans_path, persons_path, hhd_path, output_folder):
    # opens the outputPlans, outputPersons, and outputHouseholds and passes the xml files to get_person_output
    # returns the persons_dataframe

    out_plans_xml = open_xml(out_plans_path)
    persons_xml = open_xml(persons_path)
    hhd_xml = open_xml(hhd_path)
    persons_df = get_person_output(out_plans_xml, persons_xml, hhd_xml, output_folder)
    persons_df.to_csv(str(output_folder) + "/persons_dataframe.csv")
    print("persons_dataframe.csv complete")
    return persons_df


def extract_plans_dataframes(plans_path, output_folder):
    # opens the experiencedPlans and passes the xml file to get_activity_trip_output
    # returns the actitivities_dataframe and trips_dataframe

    plans_xml = open_xml(plans_path)
    acts_df, trips_df = get_activity_trip_output(plans_xml)
    acts_df.to_csv(str(output_folder) + "/activities_dataframe.csv")
    print("activities_dataframe.csv complete")
    trips_df.to_csv(str(output_folder) + "/trips_dataframe.csv")
    print("trips_dataframe.csv complete")
    return acts_df, trips_df


def extract_legs_dataframes(events_path, trips_df, output_folder):
    # opens the outputevents and passes the xml file to get_legs_output
    # augments the legs dataframe with estimates of the fuelcosts and fares for each leg
    # returns the legs_dataframe

    all_events_df = extract_dataframe(str(events_path))
    legs_df = get_legs_output(all_events_df, trips_df, output_folder)
    fuel_cost_dict = {'Gasoline': 0.03, 'Diesel': 0.02, 'Electricity': 0.01, 'Food': 0}
    legs_df_new = calc_fuel_costs(legs_df, fuel_cost_dict)
    ride_hail_fares = {'base': 0.0, 'distance': 1.0, 'duration': 0.5}
    legs_df_new_new = calc_fares(legs_df_new, ride_hail_fares)
    legs_df.to_csv(str(output_folder) + "/legs_dataframe.csv")
    print("legs_dataframe.csv complete")
    return legs_df_new_new


def output_parse(output_plans_data, persons_data, hhd_data, plans_data, events_data, output_folder):
    print(datetime.datetime.now())
    person_df = extract_person_dataframes(output_plans_data,persons_data, hhd_data, output_folder)
    print(datetime.datetime.now())
    activities_df, trips_df = extract_plans_dataframes(plans_data, output_folder)
    print(datetime.datetime.now())
    legs_df = extract_legs_dataframes(events_data, trips_df, output_folder)
    print(datetime.datetime.now())
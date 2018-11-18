from datetime import datetime

import numpy as np
import pandas as pd


def time_to_seconds_since_midnight(t):
    td = datetime.combine(datetime.min, t) - datetime.min
    return td.total_seconds()


def sample_frequency_adjustments(num_samples, feed):
    res = []
    trip_ids = []
    for _ in range(num_samples):
        min_time = pd._libs.tslibs.parsing.parse_time_string(feed.stop_times['arrival_time'].values[0])[0]
        max_time = pd._libs.tslibs.parsing.parse_time_string(feed.stop_times['arrival_time'].values[-1])[0]
        min_s = int(time_to_seconds_since_midnight(min_time.time()))
        max_s = int(time_to_seconds_since_midnight(max_time.time()))
        headway_secs = np.random.choice(range(0, 12000, 60))

        def gen_trip_id():
            tid = np.random.choice(feed.trips.trip_id.values.tolist(), 1)[0]
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
    a, b = rng
    left_inc = np.random.choice(['(', '['])
    right_inc = np.random.choice([')', ']'])
    return "{}{}:{}{}".format(left_inc, a, b, right_inc)


def sample_mode_subsidies(num_samples):
    res = []
    for _ in range(num_samples):
        possible_modes = ['walk_transit', 'ride_hail', 'walk_transit', 'walk', 'car', 'drive_transit']
        mode = np.random.choice(possible_modes)
        age = sorted(np.random.choice(range(0, 100), 2))
        income = sorted(np.random.choice(range(0, 300000, 1000), 2))
        amount = np.round(np.random.uniform(0.1, 20), 1)

        res.append({'mode': mode, 'age': format_range_with_sampled_inclusivity(age),
                    'income': format_range_with_sampled_inclusivity(income), 'amount': amount})
    return pd.DataFrame(res, columns=['mode', 'age', 'income', 'amount'])



if __name__ == '__main__':
    import sys
    from pathlib import Path
    import gtfstk as gt

    DIR = Path('..')
    sys.path.append(str(DIR))
    DATA_DIR = DIR / 'reference-data/'

    gtfs_path = DATA_DIR / 'sioux_faux_gtfs_data'
    feed = gt.read_gtfs(gtfs_path, dist_units='mi')

    freq_df = sample_frequency_adjustments(5,feed)
    mode_subsidy_df = sample_mode_subsidies(5)



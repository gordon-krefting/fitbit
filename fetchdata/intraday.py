import argparse
import connect
import datetime
import dateutil.parser
import pandas as pd


def check_date(value):
    """ Helper for command line dates """
    try:
        dateutil.parser.parse(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Invalid date: %s" % value)
    return value


# Parsing the command line
default_date = datetime.datetime.now().strftime("%Y-%m-%d")

parser = argparse.ArgumentParser(
    description='Gets intraday series data from the Fitbit API.')
parser.add_argument(
    'date', nargs='*', default=[default_date], type=check_date,
    help='Date to grab data for. Default: ' + default_date)

dates_to_process = parser.parse_args().date

fitbit = connect.get_client()


def get_intraday_df(target_date, label, endpoint, json_element):
    """
    calls the correct fitbit endpoint and returns the results as
    a DataFrame
    """
    res = fitbit.intraday_time_series(
            endpoint,
            base_date=target_date,
            detail_level='1min')

    time_values = []
    values = []
    for entry in res[json_element]['dataset']:
        time_values.append(
            dateutil.parser.parse(target_date + ' ' + entry['time']))
        values.append(entry['value'])

    df = pd.DataFrame({label: values, 'Time': time_values})
    df.set_index('Time', inplace=True)
    return df


# label, endpoint, json_element
params = [
    ['Heart Rate',
     'activities/heart',
     'activities-heart-intraday'],
    ['Fairly Active Minutes',
     'activities/minutesFairlyActive',
     'activities-minutesFairlyActive-intraday'],
    ['Very Active Minutes',
     'activities/minutesVeryActive',
     'activities-minutesVeryActive-intraday']
]

for date in dates_to_process:
    combined_df = pd.DataFrame()
    for param in params:
        res = get_intraday_df(date, param[0], param[1], param[2])
        if (combined_df.size == 0):
            combined_df = res
        else:
            combined_df = pd.merge(combined_df, res, on='Time')

    ofilename = "../data/intraday-" + date + ".csv"
    print('Saving: ' + ofilename)
    combined_df.to_csv(ofilename)

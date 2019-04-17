"""
Util for getting an authorized fitbit client
TODO: logging instead of printing
"""
import json
import fitbit


def get_client():
    """Returns a usable fitbit client"""
    with open("keys.json", "r") as read_file:
        keys = json.load(read_file)

    with open("credentials.json", "r") as read_file:
        credentials = json.load(read_file)

    print("Using credentials from credentials.json")

    client = fitbit.Fitbit(keys['client_id'],
                           keys['client_secret'],
                           oauth2=True,
                           access_token=credentials['access_token'],
                           refresh_token=credentials['refresh_token'],
                           refresh_cb=refresh_callback)
    return client


def refresh_callback(tokens):
    """Called when the FitBit API returns refreshed credentials"""
    print("Got new credentials from fitbit API and refreshed credentials.json")
    with open("credentials.json", "w") as write_file:
        json.dump(tokens,
                  write_file,
                  indent=2,
                  sort_keys=True)

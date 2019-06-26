import requests
import datetime
import pandas as pd


# go back 1 year from the current date
last_year = datetime.datetime.now() - datetime.timedelta(days=365)

# s_date = last_year.strftime('%Y-%m-%d')
# e_date = datetime.datetime.now().strftime('%Y-%m-%d')

dataset_id = "GHCND"

weathers_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data/"

stations_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations/"


# convert fahrenheit to celsius
def fahrenheit_to_celsius(f):
    c = (f - 32)*5/9
    return float(c)


# get stations in location
def get_all_stations_in_location(dataset, location, token):

    noaa_token = {'token': token}

    params = 'datasetid=' + str(dataset) + '&' + 'locationid=' + str(
        location) + '&sortfield=name&sortorder=asc&limit=1000&offset=1'

    req = requests.get(stations_url, params=params, headers=noaa_token)
    print("Request status code: " + str(req.status_code))

    try:
        df = pd.DataFrame.from_dict(req.json()['results'])
        df = df.drop(['datacoverage', 'elevation', 'elevationUnit', 'maxdate', 'mindate'], axis=1)
        return df
    except ValueError:
        print("Error converting stations data to data frame.")


# get station weather between two datetime
def get_bulk_weather_in_station(dataset, location, start_date, end_date, token):

    noaa_token = {'token': token}

    # passing as string instead of dict because NOAA API does not like percent encoding
    params = 'stationid=' + str(location) + '&' 'datasetid=' + str(dataset) + '&' + 'startdate=' + str(
        start_date) + '&' + 'enddate=' + str(end_date) + '&' + 'limit=1000' + '&' + 'units=standard'

    req = requests.get(weathers_url, params=params, headers=noaa_token)
    print("Request status code: " + str(req.status_code))

    try:
        # results comes in json form. Convert to data frame
        df = pd.DataFrame.from_dict(req.json()['results'])

        df['celsius_value'] = df['value'].apply(fahrenheit_to_celsius)
        print("Successfully retrieved " + str(len(df['station'].unique())) + " stations")

        dates = pd.to_datetime(df['date'])
        print("Last date retrieved: " + str(dates.iloc[-1]))
        return df

    # Catch all exceptions for a bad request or missing data
    except ValueError:
        print("Error converting weather data to data frame.")
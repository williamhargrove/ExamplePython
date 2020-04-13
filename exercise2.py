import requests
import datetime
import argparse
import re


def get_highest_temperature_holiday(location, holiday):
    """

    :param location: str
    :param holiday: str
    :return: temperatures: dict
    """

    def get_woeid(location):
        """

        :param location: str
        :return: where on earth location id: str
        """
        # 3. could separate the url config into a properties file parsed with configparser
        uri_woeid = 'https://www.metaweather.com/api/location/search/?query='
        try:
            response = requests.get(uri_woeid + location)
            response.raise_for_status()

            # check for empty json array being returned
            if len(response.json()) == 0:
                raise Exception('Metaweather unable to find location {}'.format(location))
            else:
                return response.json()[0]['woeid']

        except requests.exceptions.HTTPError as errh:
            # include the original error response below
            print("Http Error:", errh.response.text)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Unable to determine WOTID", err)

    def get_bankholiday_dates(holiday):
        """

        :param holiday: str
        :return: array of date objects
        """

        uri_govuk = 'https://www.gov.uk/bank-holidays.json'
        try:
            resp = requests.get(uri_govuk)
            resp.raise_for_status()

            response = resp.json()
            # 1. also could have used a dictionary comprehension to search through the response
            # 2. will take first holiday match found, even if location is in a region other than 'england-and-wales'
            #    and that holiday had a different date. Need to match WOEID to region.

            date_list = []
            for region in response.keys():
                for event in response[region].keys():
                    # skip the 'division'
                    if event == 'events':
                        for value in response[region][event]:
                            if (re.search(holiday, value['title'], re.IGNORECASE)) and (region == 'england-and-wales'):
                                date = datetime.datetime.strptime(value['date'], "%Y-%m-%d")
                                date_list.append(date)

            assert (len(date_list) > 0), 'Unable to find dates for bank holiday'

            return date_list

        except requests.exceptions.HTTPError as errh:
            # include the original error response below
            print("Http Error:", errh.response.text)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Unable to determine WOTID", err)

    def get_max_year(woeid, holiday_dates):
        """

        :param location: str
        :param woeid: str
        :param holiday_date: date object
        :return: year/temperature: dict
        """
        uri_temperatures = 'https://www.metaweather.com/api/location'

        max_temperatures = []

        for date in holiday_dates:

            year = str(date.year)

            # skip dates for bank holidays in future time periods
            if date > date.now():
                continue
            month = str(date.month)
            day = str(date.day)

            try:
                call = uri_temperatures + '/' + str(woeid) + '/' + year + '/' + month + '/' + day + '/'
                response = requests.get(call)
                weather = response.json()

            except requests.exceptions.HTTPError as errh:
                # include the original error response below
                print("Http Error:", errh.response.text)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("Unable to obtain weather data", err)

            else:
                # for each year get the max_temp and append to array of year/max temp
                max_temp_per_year = sorted(weather, key=lambda key: key['max_temp'], reverse=True)
                max_temperatures.append({ 'year': date.year, 'maximum_temp': max_temp_per_year[0]['max_temp']})

        return sorted(max_temperatures, key=lambda key: key['maximum_temp'], reverse=True)[0]



    woeid = get_woeid(location)
    holiday_dates = get_bankholiday_dates(holiday)

    year_temperature = get_max_year(woeid, holiday_dates)
    return year_temperature


if __name__ == "__main__":
    """Take commandline args and parse into location and holiday.

    Calls get_bankholiday_temperatures function and returns a dict with temperature details

    """
    arg_parser = argparse.ArgumentParser(prog='exercise2',
                                         usage='usage: \n%(prog)s location "holiday"',
                                         description='Retrieve the highest recorded temperature for a specific holiday',
                                         add_help=True
                                         )
    arg_parser.add_argument('location', action='store', type=str, help='eg Liverpool')
    arg_parser.add_argument('holiday', action='store', type=str, help='eg "Good Friday"')

    args = arg_parser.parse_args()

    results = get_highest_temperature_holiday(args.location, args.holiday)

    print("{} recorded the highest temperature for {} in {}".format(results['year'], args.holiday, args.location))


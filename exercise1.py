import requests
import datetime
import argparse
import re


def get_bankholiday_temperatures(location, holiday, year):
    """

    :param location: str
    :param holiday: str
    :param year: str
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
            response = requests.get(uri_woeid+location)
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

    def get_bankholiday_date(holiday, year):
        """

        :param holiday: str
        :param year: str
        :return: date object
        """

        uri_govuk = 'https://www.gov.uk/bank-holidays.json'
        try:
            resp = requests.get(uri_govuk)
            resp.raise_for_status()

            response=resp.json()
            # 1. also could have used a dictionary comprehension to search through the response
            # 2. will take first holiday match found, even if location is in a region other than 'england-and-wales'
            #    and that holiday had a different date. Need to match WOEID to region.
            for region in response.keys():
                for event in response[region].keys():
                    # skip the 'division'
                    if event == 'events':
                        for value in response[region][event]:
                            if (re.search(holiday, value['title'], re.IGNORECASE)):
                                # convert string representation into a date object
                                date = datetime.datetime.strptime(value['date'], "%Y-%m-%d")
                                if date.year == year:
                                    return date

            raise Exception('Unable to find date for {} bank holiday'.format(holiday))

        except requests.exceptions.HTTPError as errh:
            # include the original error response below
            print("Http Error:", errh.response.text)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Unable to determine WOTID", err)

    def get_temperatures(woeid, holiday_date):
        """

        :param location: str
        :param woeid: str
        :param holiday_date: date object
        :return: temperatures: dict
        """
        uri_temperatures = 'https://www.metaweather.com/api/location'
        year=str(holiday_date.year)
        month=str(holiday_date.month)
        day=str(holiday_date.day)

        try:
            temperatures = {}

            call = uri_temperatures+'/'+str(woeid)+'/'+year+'/'+month+'/'+day+'/'
            response = requests.get(call)

            weather=response.json()

            # sort the array of dictionaries (weather) keyed off min_temp and max_temp
            min_temp=sorted(weather, key=lambda key: key['min_temp'])
            temperatures['min']=min_temp[0]['min_temp']

            max_temp=sorted(weather, key=lambda key: key['max_temp'], reverse=True)
            temperatures['max'] = max_temp[0]['max_temp']

            return temperatures

        except requests.exceptions.HTTPError as errh:
            # include the original error response below
            print("Http Error:", errh.response.text)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Unable to determine WOTID", err)


    woeid=get_woeid(location)
    holiday_date=get_bankholiday_date(holiday, year)

    temperatures = get_temperatures(woeid, holiday_date)
    return temperatures

if __name__ == "__main__":
    """Take commandline args and parse into location, holiday and year.
    
    Calls get_bankholiday_temperatures function and returns a dict with temperature details
      
    """
    arg_parser = argparse.ArgumentParser(prog='exercise1',
                                usage='usage: \n%(prog)s location "holiday" year',
                                description='Retrieve the highest/lowest temperature recorded on a specific holiday',
                                add_help=True
                                )
    arg_parser.add_argument('location', action='store', type=str, help='eg Liverpool')
    arg_parser.add_argument('holiday', action='store', type=str, help='eg "Good Friday"')
    arg_parser.add_argument('year', action='store', type=int, help='eg 2019')

    args = arg_parser.parse_args()

    results = get_bankholiday_temperatures(args.location, args.holiday, args.year)

    print("The highest temperature in {} on {} {} was {:.2f} Celsius".format(args.location, args.holiday, args.year, results['max']))
    print("The lowest temperature in {} on {} {} was {:.2f} Celsius".format(args.location, args.holiday, args.year, results['min']))

import requests
import json
import time

URL = 'https://testnet.bitmex.com'
#global

open_position = False


def get_funding_rate():
    payload = {'symbol': 'XBTUSD', 'columns': ['fundingRate','indicativeFundingRate']}
    resp = requests.get(URL+"/api/v1/instrument/", params=payload)
    if resp.status_code != 200:
        # This means something went wrong.
        #raise ApiError('GET /bist/XBT/GBP/balance/ {}'.format(resp.status_code))
        pass
    print(resp.json())

    # assign json response to a variable
    response=resp.json()
    # print (response[0]['symbol'])
    # print (response[0]['fundingRate'])
    # print (response[0]['indicativeFundingRate'])
    # iterate through response, using .items to return a tuple.
    # for k, v in response.items()[0]:
    #     print(k,v)
    # for key in response.items[0]():
    #     print(response["key"])
    return {'symbol': response[0]['symbol'], 'fundRate': response[0]['fundingRate'], 'forwardfundRate': response[0]['indicativeFundingRate']}

def open_limit_order(open_position):
    print("in open_limit_order boolean is:",open_position)
    if open_position == True:
        print("Position open already - will not open another one.")
    else:
        print("Opening a limit order to short. Make sure limit price is higher than current trading price.")
        open_position = True
    return open_position


def main():
    #x = {}
    print("in main boolean is:",open_position)
    rates = get_funding_rate()
    for key,value in rates.items():
        #print("{}: {0:.5f}".format(key,value))
        if (type(value)) == str:
            print("{}: {}".format(key,value))
        else:
            print("{}: {:.4%}".format(key,value))
    # if x['fundingRate'] < 0:
    #     print ('Funding rate is negative')
    #
    # if x['indicativeFundingRate'] < 0:
    #     print ('Forward funding rate is negative')


    if rates['fundRate'] <= 0 and rates['forwardfundRate'] <= 0:
        print("Skipping... both funding rate and foward funding rate are negative")
    elif rates['fundRate'] > 0 and rates['forwardfundRate'] <= 0:
        print("SkillpingCurrent period funding rate is positive, forward period is negative")
    elif rates['fundRate'] > 0 and rates['forwardfundRate'] > 0:
        print ("Current and forward period rates are positive")
        open_limit_order(open_position)
    else:
        print ("Negative rates in current period, but forward period is positive")

if __name__ == '__main__':

    print ("Welcome to Lending Bot on BitMEX ")

    try:

        while True:
            try:
                main()
                time.sleep(300)
            except KeyboardInterrupt:
                # allow exiting the main bot loop
                raise

    except KeyboardInterrupt:
        print ("bye")

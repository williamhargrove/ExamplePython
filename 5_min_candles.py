import requests
import time
from datetime import datetime

URL = "https://api.pro.coinbase.com"

def get_data():
    #query = {granularity: 300 }
    #URI = URL + "/products/BTC-GBP/candles?granularity=300"
    URI = URL + "/products/BTC-GBP/candles"
    print("using URI: {}".format(URI))

    try:
        resp = requests.get(URI, params={"granularity": "300"})
        #resp = requests.get(URI)
    except:
        print('There was a connection issue')
        print(error)

    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /bist/XBT/GBP/balance/ {}'.format(resp.status_code))
    #print(resp.json())

    # assign json response to a variable
    # [ time, low, high, open, close, volume ],
    response = resp.json()

    for item in response:
        #print(item[0])
        #print(datetime.utcfromtimestamp(item[0]).strftime('%Y-%m-%d %H:%M:%S'), "Open {}", 'High', 'Low', 'Close'.format(item[1]))
        print("{}, Low {}, High {}, Open {}, Close {}".format(datetime.utcfromtimestamp(item[0]).strftime('%Y-%m-%d %H:%M:%S'), item[1], item[2], item[3], item[4]))



def main():

    try:
        while True:
            try:
                get_data()
                # ticker(ASSETS['XBT'], ASSETS['USDT'])
                # balance(ASSETS['XBT'])
                # balance(ASSETS['USDT'])
                # price = get_coinbase_price()

                # negative quantity for sell order
                #  -100 corresponds to $T 0.0100
                # -1000 corresponds to $T 0.1000
                # multiply price by 10000
                # delete_orders()
                # for p in range(1, 20):
                #     ask = (price - p)*10000
                #     #print(price)
                #     orders(ASSETS['XBT'], ASSETS['USDT'], ask, -100)
                time.sleep(60)
            except KeyboardInterrupt:
                # allow exiting main loop
                # delete_orders()
                raise
    except KeyboardInterrupt:
        print("bye")

if __name__ == '__main__':
    main()
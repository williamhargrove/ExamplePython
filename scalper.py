mport requests
import time

USER = 'REPLACE'
PASSWORD = 'REPLACE'
URL = 'REPLACE'

ASSETS = {'XBT' : 63488,
          'BCH' : 63496,
          'ETH' : 63520,
          'USDC': 65282,
          'USDT': 65283
          }


def place_order(base, counter, quantity):
    #params = {"base": base, "counter": counter, "price": price, "quantity": quantity}
    params = {"base": base, "counter": counter, "quantity": quantity}
    #print(params)
    URI=URL+"/orders/"
    print("using URI: {}".format(URI))

    try:
        resp = requests.post(URI, data=params, auth=(USER, PASSWORD))
    except:
        print ('There was a connection issue')
        print (error)
        #print(resp.status_code)

    print(resp.status_code)

    #print(resp.json())

    # if resp.status_code != 201:
    #     raise
    # assign json response to a variable
    print(resp.json())
    #
    # # iterate through response, using .items to return a tuple.
    # for k, v in response.items():
    #     print(k,v)


def main():

    try:
        order = place_order(ASSETS['USDT'], ASSETS['XBT'])
        price=
        id=
        while True:
            try:
                market_price = get_price
                if market price + sell_fee > purchase_price:
                    place_sell_order()
                # ticker(ASSETS['XBT'], ASSETS['USDT'])
                # balance(ASSETS['XBT'])
                # balance(ASSETS['USDT'])
                # price = get_coinbase_price()
                #
                # # negative quantity for sell order
                # #  -100 corresponds to $T 0.0100
                # # -1000 corresponds to $T 0.1000
                # # multiply price by 10000
                # delete_orders()
                # for p in range(1, 20):
                #     ask = (price - p)*10000
                #     #print(price)
                #     orders(ASSETS['XBT'], ASSETS['USDT'], ask, -100)
                time.sleep(5)
                #place_buy_order()
            except KeyboardInterrupt:
                # allow exiting main loop
                #delete_orders()
                raise
    except KeyboardInterrupt:
        print("bye")

if __name__ == '__main__':
    main()
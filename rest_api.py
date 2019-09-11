import requests
import time

USER = '3/yOOwLj/sGXVocRUksl8qp9YjSn8='
PASSWORD = 'coinflex123'
URL = 'https://applewebapi.coinflex.com'

ASSETS = {'XBT' : 63488,
          'BCH' : 63496,
          'ETH' : 63520,
          'USDC': 65282,
          'USDT': 65283
          }

def balance(base):
    URI=URL+"/balances/"+str(base)
    print("using URI: {}".format(URI))

    try:
        resp = requests.get(URI, auth=(USER,PASSWORD))
    except:
        print('There was a connection issue')
        print(error)


    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /bist/XBT/GBP/balance/ {}'.format(resp.status_code))
    print(resp.json())

    # assign json response to a variable
    response=resp.json()
    # iterate through response, using .items to return a tuple.
    for k, v in response.items():
        print(k,v)

def ticker(base,counter):
    URI=URL+"/tickers/"+str(base)+":"+str(counter)
    print("using URI: {}".format(URI))

    try:
        resp = requests.get(URI)
    except:
        print ('There was a connection issue')
        print (error)

    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /bist/XBT/GBP/ticker/ {}'.format(resp.status_code))
    print(resp.json())

    # assign json response to a variable
    response=resp.json()

    # iterate through response, using .items to return a tuple.
    for k, v in response.items():
        print(k,v)

    #print('Ask price: {}'.format(resp.json()['ask']))
    #print('Bid price: {}'.format(resp.json()['bid']))
    # ask = float(resp.json()['ask'])
    # bid = float(resp.json()['bid'])
    #
    # spread=((ask-bid)/ask)
    # print('Spread: {:.3%}'.format(spread))

def orders(base,counter,price,quantity):
    params = {"base": base, "counter": counter, "price": price, "quantity": quantity}
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

def delete_orders():

    URI=URL+"/orders/"
    print("using URI: {}".format(URI))

    try:
        resp = requests.delete(URI, auth=(USER, PASSWORD))
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

def get_coinbase_price():
    return 7749

def main():

    try:
        while True:
            try:
                ticker(ASSETS['XBT'], ASSETS['USDT'])
                balance(ASSETS['XBT'])
                balance(ASSETS['USDT'])
                price = get_coinbase_price()

                # negative quantity for sell order
                #  -100 corresponds to $T 0.0100
                # -1000 corresponds to $T 0.1000
                # multiply price by 10000
                delete_orders()
                for p in range(1, 20):
                    ask = (price - p)*10000
                    #print(price)
                    orders(ASSETS['XBT'], ASSETS['USDT'], ask, -100)
                time.sleep(5)
            except KeyboardInterrupt:
                # allow exiting main loop
                delete_orders()
                raise
    except KeyboardInterrupt:
        print("bye")

if __name__ == '__main__':
    main()

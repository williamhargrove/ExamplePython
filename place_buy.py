import requests

USER = 'REPLACE'
PASSWORD = 'REPLACE'
URL = 'https://webapi.coinflex.com'

def place_buy():
    base = 65283 # USDR
    counter = 63488 # XBT
    quantity =
    price = 

    params = {"base": base, "counter": counter, "quantity": quantity}

    URI=URL+"/orders/"
    print("using URI: {}".format(URI))

    try:
        resp = requests.post(URI, data=params, auth=(USER, PASSWORD))
    except:
        print ('There was a connection issue')
        print (error)
    print(resp.json())



def main():
    place_buy()


if __name__ == '__main__':
    main()
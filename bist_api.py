import requests
import credentials

USER = credentials.USER
PASSWORD = credentials.PASSWORD
URL = credentials.URL

BOOK = 'ETH'

# resp = requests.get(CALL, auth=(USER,PASSWORD))
# if resp.status_code != 200:
#     # This means something went wrong.
#     raise ApiError('GET /bist/XBT/GBP/ticker/ {}'.format(resp.status_code))
#
# print(resp.json())
# print ('XBT balance: {}'.format(resp.json()["xbt_balance"]))
# print ('GBP balance: {}'.format(resp.json()["gbp_balance"]))

def withdrawal():
    params = {"amount": "0.005"}
    try:
        resp = requests.post(URL+"/bist/"+BOOK+"/GBP/bitcoin_withdrawal/", data=params, auth=(USER,PASSWORD))
    except:
        print('There was a connection issue. Error code: {}'.format(resp.status_code))
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /bist/XBT/GBP/bitcoin_withdrawal/ {}'.format(resp.status_code))
    print(resp.json())

    # assign json response to a variable
    response=resp.json()

    # iterate through response, using .items to return a tuple.
    for k, v in response.items():
        print(k,v)


def ticker():
    try:
        resp = requests.get(URL+"/bist/"+BOOK+"/GBP/ticker/")
    except:
        print ('There was a connection issue')

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
    ask = float(resp.json()['ask'])
    bid = float(resp.json()['bid'])

    spread=((ask-bid)/ask)
    print('Spread: {:.3%}'.format(spread))


def order_book():
    resp = requests.get(URL+"/bist/"+BOOK+"/GBP/order_book/")
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /bist/XBT/GBP/order_book/ {}'.format(resp.status_code))
    print(resp.json())

#    print('Ask price: {}'.format(resp.json()['ask']))

def user_transactions():
    resp = requests.get(URL+"/bist/"+BOOK+"/GBP/user_transactions/", auth=(USER,PASSWORD))
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /bist/ETH/GBP/user_transactions/ {}'.format(resp.status_code))
    print(resp.json())
    # assign json response to a variable
    response=resp.json()
    #
    # # iterate through response, using .items to return a tuple.
    # for k, v in response.items():
    #     print(k,v)



def balance():
    resp = requests.get(URL+"/bist/"+BOOK+"/GBP/balance/", auth=(USER,PASSWORD))
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /bist/XBT/GBP/balance/ {}'.format(resp.status_code))
    #print(resp.json())

    # assign json response to a variable
    response=resp.json()
    # iterate through response, using .items to return a tuple.
    for k, v in response.items():
        print(k,v)

def estimate_buy_market():
    params = { "quantity" : "0.01" }
    resp = requests.post(URL+"/bist/"+BOOK+"/GBP/estimate_buy_market/", data=params, auth=(USER,PASSWORD))
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('POST /bist/XBT/GBP/estimate_buy_market/ {}'.format(resp.status_code))
    # assign json response to a variable
    response=resp.json()
    # iterate through response, using .items to return a tuple.
    for k, v in response.items():
        print(k,v)

def buy_market():
    params = { "quantity" : "0.01" }
    resp = requests.post(URL+"/bist/"+BOOK+"/GBP/buy_market/", data=params, auth=(USER,PASSWORD))
    print(resp.status_code)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('POST /bist/XBT/GBP/buy_market/ {}'.format(resp.status_code))
    # assign json response to a variable
    response=resp.json()

    # iterate through response, using .items to return a tuple.
    for k, v in response.items():
        print(k,v)
        if k == 'remaining' and v != 0:
            print("Buy order not matched as quantity is remaining")

def buy_limit(amount,price):
    params = { "amount" : amount, "price": price }
    resp = requests.post(URL+"/bist/"+BOOK+"/GBP/buy/", data=params, auth=(USER,PASSWORD))
    print(resp.status_code)
    if resp.status_code == 403:
        # Insufficient funds
        raise ApiError('Insufficient funds POST /bist/XBT/GBP/buy/ {}'.format(resp.status_code))
    elif resp.status_code != 200:
        raise ApiError('POST /bist/XBT/GBP/buy/ {}'.format(resp.status_code))
    # assign json response to a variable
    response=resp.json()

    # iterate through response, using .items to return a tuple.
    for k, v in response.items():
        print(k,v)

def sell_limit(amount,price,nonce,ttl):
    params = {"amount" : amount, "price": price}
    resp = requests.post(URL + "/bist/" + BOOK + "/GBP/sell/", data=params, auth=(USER, PASSWORD))
    print(resp.status_code)
    if resp.status_code != 200:
        raise ApiError('POST /bist/XBT/GBP/sell/ {}'.format(resp.status_code))
    # assign json response to a variable
    response=resp.json()

    # iterate through response, using .items to return a tuple.
    for k, v in response.items():
        print(k,v)


def main():
    balance()
    #withdrawal()
    order_book()
    #user_transactions()
    ticker()
    #balance()


if __name__ == '__main__':
    main()

# buy the bid, sell the offer
# what is the bid/offer on other exchanges?
# as there are no market prices, sell at the offer

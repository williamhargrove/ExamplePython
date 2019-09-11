# pip install requests deribit_api
# also pip install "websocket-client<0.49.0" ecdsa
# see instructions on https://github.com/coinflex-exchange/python-library

import threading
import datetime, time, random, math, sys
import requests, json
import websocket
import logging, os
from deribit_api import RestClient

from coinflex import Assets
from coinflex import WSClient

# test account on deribit
client = RestClient("reference", "token")

# COINFLEX SECRETS -- enter something here!
USERID = 'core_id'
COOKIE = 'cookie'
PASSWD = 'password'

# SETUP LOGGER
##############
# add logging.StreamHandler() to handlers list if needed
logger = logging.getLogger("Coinflex")
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('simplemm.log')
fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# DERIBIT WEBSOCKETS
####################
def deribit_on_message(ws, message):
    global bestbid, bestask, bestbidq, bestaskq
    global lasttrade, lasttradeq, newtradeflag
    
    message = json.loads(message)

    if 'notifications' in message:
        for i in message['notifications']:
            if i['message'] == 'order_book_event':
                with lock:
                    bestbid = i['result']['bids'][0]['price']
                    bestask = i['result']['asks'][0]['price']
                    bestbidq = i['result']['bids'][0]['quantity']
                    bestaskq = i['result']['asks'][0]['quantity']

def deribit_on_error(ws, error):
    global coinflex_global_stop_flag
    print(error)
    try:
        logbuffer.append('xbtaug: deribit websocket error:\n'+str(sys.exc_info()[0]))
        with lock:
            coinflex_global_stop_flag = True
    except:
        pass
    
def deribit_on_close(ws):
    print("### closed ###")
    try:
        logbuffer.append('xbtaug: deribit websocket closed:\n'+str(sys.exc_info()[0]))
    except:
        pass

def deribit_on_open(ws):
    print('opening deribit connection...')
    data = {
        "id": 5533,
        "action": "/api/v1/private/subscribe",  
        "arguments": {
            "instrument": ["BTC-PERPETUAL"],
            "event": ["order_book"] 
        }
    }
    data['sig'] = client.generate_signature(data['action'], data['arguments'])
    ws.send(json.dumps(data))

# COINFLEX FUNCTIONS
####################

# Helper for sending message
def coinflex_closer():
    global coinflex, coinflex_tonce, coinflex_api_counter
    with lock:
        coinflex.CancelAllOrders()
        coinflex_api_counter.append(time.time())
        coinflex_tonce = TONCE_STARTER
    
# Thread for coinflex orderbook (not launched here but by coinflex library code)
def coinflex_flow(ws, msg):
    global coinflex_orderbook, coinflex_last_tick
    global coinflex_ticker_bid, coinflex_ticker_ask
    global coinflex_position, coinflex_trade_occurred_flag
    global coinflex_out_of_tonce_flag, coinflex_fair_value
    global coinflex_currentbuyprice, coinflex_currentsellprice, coinflex_tonce
    global coinflex_currentbuyordertonce, coinflex_currentsellordertonce
    global coinflex_global_stop_flag
    
    msg = json.loads(msg)

    # check for errors
    if 'error_code' in msg:
        if msg['error_code'] != 0:
            print(msg)

        if msg['error_code'] == 1:
            with lock:
                # hack for missing trade!
                coinflex_trade_occurred_flag = True
        if msg['error_code'] == 4:
            logbuffer.append('xbtaug: run out of funds:\n'+str(msg))
            with lock:
                coinflex_global_stop_flag = True
                # hack to cancel all
                coinflex_trade_occurred_flag = True

    # check for cancelall
    if 'orders' in msg and 'tag' in msg:
        with lock:
            coinflex_currentbuyprice = 0
            coinflex_currentsellprice = 0
            coinflex_tonce = TONCE_STARTER
        
    if 'orders' in msg and msg['orders'] != []:
        with lock:
            coinflex_orderbook = msg['orders']
            coinflex_orderbook.sort(key=lambda k: k['price'])
        
    if 'notice' in msg:
        if msg['notice'] == 'OrdersMatched':
            with lock:
                coinflex_last_tick = msg['price']/10000.0
            # check for my own trades
            if 'bid_tonce' in msg and msg['bid_tonce'] == coinflex_currentbuyordertonce:
                with lock:
                    coinflex_position += msg['quantity']/10000.0
                    coinflex_position = round(coinflex_position, 4)
                    coinflex_trade_occurred_flag = True
                if msg['quantity'] >= coinflex_quantity*random.random():
                    coinflex_fair_value += 1

            if 'ask_tonce' in msg and msg['ask_tonce'] == coinflex_currentsellordertonce:
                with lock:
                    coinflex_position -= msg['quantity']/10000.0
                    coinflex_position = round(coinflex_position, 4)
                    coinflex_trade_occurred_flag = True
                if msg['quantity'] >= coinflex_quantity*random.random():
                    coinflex_fair_value -= 1
                    
        if msg['notice'] == 'TickerChanged':
            if 'ask' in msg:
                with lock:
                    coinflex_ticker_ask = msg['ask']/10000.0
            if 'bid' in msg:
                with lock:
                    coinflex_ticker_bid = msg['bid']/10000.0

        if msg['notice'] == 'OrderClosed':
            old_order = {'id': msg['id'],
                         'price': msg['price'],
                         'quantity': msg['quantity']}
            with lock:
                coinflex_orderbook = [d for d in coinflex_orderbook if d.get('id') != old_order['id']]
                coinflex_orderbook.sort(key=lambda k: k['price'])
                
        if msg['notice'] == 'OrderOpened':
            new_order = {'id': msg['id'],
                         'price': msg['price'],
                         'quantity': msg['quantity']}
            with lock:
                coinflex_orderbook.append(new_order)
                coinflex_orderbook.sort(key=lambda k: k['price'])

        if msg['notice'] == 'OrderModified':
            mod_order = {'id': msg['id'],
                         'price': msg['price'],
                         'quantity':msg['quantity']}
            with lock:
                coinflex_orderbook = [d for d in coinflex_orderbook if d.get('id') != mod_order['id']]
                coinflex_orderbook.append(mod_order)
                coinflex_orderbook.sort(key=lambda k: k['price'])

def start_coinflex_websocket():
    global coinflex, coinflex_position, coinflex_api_counter

    start_flag = False

    while not start_flag:
        with lock:
            try:
                coinflex= WSClient(
                    "wss://stgapi.coinflex.com/v1",
                    msg_handler   = coinflex_flow,
                    close_handler = coinflex_closer
                )

                coinflex.WatchOrders(
                    base    = Assets[coinflex_xbt_string],
                    counter = Assets[coinflex_usdt_string],
                    watch   = True,
                    tag = 1
                )
                coinflex.WatchTicker(
                    base    = Assets[coinflex_xbt_string],
                    counter = Assets[coinflex_usdt_string],
                    watch   = True
                )
                start_flag = True
            except:
                logbuffer.append('xbtaug: could not restart websockets:\n'+str(sys.exc_info()[0]))
            time.sleep(1)
    try:
        coinflex.set_auth_data(int(USERID), COOKIE, PASSWD)
        coinflex.authenticate()
    except:
        logbuffer.append('xbtaug: could not authenticate on restart:\n'+str(sys.exc_info()[0]))
        

    # rest api for initial position
    temp_flag = True
    while temp_flag:
        try:
            r = requests.get('https://stgwebapi.coinflex.com/positions/', auth=requests.auth.HTTPBasicAuth(USERID+'/'+COOKIE, PASSWD))
            for i in json.loads(r.text):
                if i['asset'] == coinflex_xbt_code:
                    with lock:
                        coinflex_position = i['position']/10000.0 + POSITION_ADJUSTMENT
                        coinflex.CancelAllOrders(
                            tag = 99999999
                        )
                        coinflex_api_counter.append(time.time())
            temp_flag = False
        except:
            pass
        if temp_flag:
            time.sleep(1)

# LOGGER THREAD
###############

def slowlogger():
    global logbuffer
    while True:
        while logbuffer:
            with lock:
                a = logbuffer.pop()
            logger.info(a)
        time.sleep(1)


# MM VARS
############
lock = threading.Lock()

coinflex_bid, coinflex_ask = 0,0
coinflex_bidq, coinflex_askq = 0,0
coinflex_orderbook = []
coinflex_last_tick = 0
coinflex_position = 0

coinflex_ticker_bid = 0
coinflex_ticker_ask = 0

# "XBTJUN18" : 51205,
# "USDTJUN18" : 51885,
# coinflex_xbt_code = 51207
# coinflex_usdt_code = 51887
# coinflex_xbt_string = "XBTAUG18"
# coinflex_usdt_string = "USDTAUG18"

coinflex_xbt_code = 63488
coinflex_usdt_code = 65283
coinflex_xbt_string = "XBT"
coinflex_usdt_string = "USDT"

coinflex_fair_value = -70

MAX_FAIR_VALUE = 100
MIN_FAIR_VALUE = -200

TONCE_STARTER = 1

NORMAL_SPREAD = 2.5 # in bips from mid
FASTMARKET_SPREAD = 5 # in bips from mid

PRICE_CHANGE_BOUNDS = 30

POSITION_ADJUSTMENT = 0

coinflex_working_bid, coinflex_working_ask = 0,0
coinflex_working_spread = NORMAL_SPREAD # in bips from mid
coinflex_quantity = 10000
COINFLEX_MAX_POSITION = 11 # in xbt units
coinflex_max_flag = False
coinflex_max_flag_timer = 0

coinflex_tonce = TONCE_STARTER
coinflex_out_of_tonce_flag = False

coinflex_currentsellordertonce, coinflex_currentsellprice = TONCE_STARTER,0
coinflex_currentbuyordertonce, coinflex_currentbuyprice = TONCE_STARTER,0
coinflex_time_since_last_placeorder = 0
coinflex_trade_occurred_flag = False

coinflex_buy_taking_count, coinflex_sell_taking_count = 0,0
coinflex_global_stop_flag = False
coinflex_global_stop_flag_done = False

# 200 per second
COINFLEX_API_THRESHOLD = 150
coinflex_api_counter = []

deribit_perpetual_mid = 0
deribit_implied_mid = 0
deribit_front_month_mid = 0
deribit_index = 0

deribit_fast_market_flag = False
deribit_fast_market_timer = 0

deribit_min_depth = 50

bestbid, bestask, bestbidq, bestaskq = 0,0,0,0
oldbestbid, oldbestask = 0,0
lasttick = 0
lasttick_timer = 0

bidaskbalance = 0
bidaskbalance_multiplier = 10
lasttrade, lasttradeq, newtradeflag = 0,0,False

logbuffer = []

flag_for_operations = True
flag_for_deribit_trading = True

start_coinflex_websocket()

# START THREADS
###############

# start a deribit thread
ws = websocket.WebSocketApp("wss://www.deribit.com/ws/api/v1/",
                          on_message = deribit_on_message,
                          on_error = deribit_on_error,
                          on_close = deribit_on_close)
ws.on_open = deribit_on_open
ws.keep_running = True
t2 = threading.Thread(target=ws.run_forever, kwargs={'ping_interval': 30})
t2.start()

# start a slow logger thread
t4 = threading.Thread(target=slowlogger)
t4.start()
                      
while coinflex_orderbook == []:
    pass

printtimer = time.time()

delay_quote_timer = time.time()
delay_quote_timer_flag = False

while True:
    with lock:
        deribit_perpetual_mid = (bestbid+bestask)/2.0

    # kludge for quoting prices after estimates settle
    if not delay_quote_timer_flag and time.time() - delay_quote_timer > 15:
        delay_quote_timer_flag = True
        
    # check for deribit fast market; use timer to delay flipping back to false
    if time.time() - deribit_fast_market_timer > 0.1:
        deribit_fast_market_flag = False
    if bestask - bestbid > 0.5:
        deribit_fast_market_flag = True
        deribit_fast_market_timer = time.time()
        
    try:
        with lock:
            if len(coinflex_orderbook)>1:
                sorted_bids = [i for i in coinflex_orderbook if i['quantity']>0][::-1]
                sorted_asks = [i for i in coinflex_orderbook if i['quantity']<0]

                coinflex_bid = sorted_bids[0]['price']/10000.0
                coinflex_bidq = sorted_bids[0]['quantity']/10000.0
                coinflex_ask = sorted_asks[0]['price']/10000.0
                coinflex_askq = sorted_asks[0]['quantity']/10000.0
    except:
        deribit_fast_market_flag = True
        deribit_fast_market_timer = time.time()

    # floor and ceiling for fair value
    if coinflex_fair_value > MAX_FAIR_VALUE:
        with lock:
            coinflex_fair_value = MAX_FAIR_VALUE
            logbuffer.append('xbtaug: max fair value reached: '+str(MAX_FAIR_VALUE))
    if coinflex_fair_value < MIN_FAIR_VALUE:
        with lock:
            coinflex_fair_value = MIN_FAIR_VALUE
            logbuffer.append('xbtaug: min fair value reached: '+str(MIN_FAIR_VALUE))
            
    bidaskbalance = round((random.random()-0.5)*10)
        
    temp_mid = deribit_perpetual_mid - coinflex_fair_value
    temp = temp_mid * coinflex_working_spread / 10000.0
    with lock:
        coinflex_working_bid = int(math.floor(temp_mid - temp)) + bidaskbalance
        coinflex_working_ask = int(math.ceil(temp_mid + temp)) + bidaskbalance

    # bounds check for massive misprints on price changes
    if coinflex_currentbuyprice != 0 and coinflex_working_bid - coinflex_currentbuyprice > PRICE_CHANGE_BOUNDS:
        with lock:
            coinflex_working_bid = coinflex_currentbuyprice + PRICE_CHANGE_BOUNDS
            logbuffer.append('Hit a price change bound on increasing bid. Current price '+str(coinflex_currentbuyprice)+'. Working '+str(coinflex_working_bid))
    if coinflex_currentsellprice != 0 and coinflex_currentsellprice - coinflex_working_ask > PRICE_CHANGE_BOUNDS:
        with lock:
            coinflex_working_ask = coinflex_currentsellprice - PRICE_CHANGE_BOUNDS
            logbuffer.append('Hit a price change bound on decreasing ask. Current price '+str(coinflex_currentsellprice)+'. Working '+str(coinflex_working_ask))
            
    # COINFLEX ORDERS
    # place orders
    if coinflex_currentbuyprice == 0 and coinflex_bid != 0 and delay_quote_timer_flag and not deribit_fast_market_flag and \
       coinflex_position < COINFLEX_MAX_POSITION and time.time()-coinflex_time_since_last_placeorder > 0.1 and not coinflex_global_stop_flag:
        try:
            if len(coinflex_api_counter)<COINFLEX_API_THRESHOLD:
                coinflex.PlaceOrder(
                    base = Assets[coinflex_xbt_string],
                    counter = Assets[coinflex_usdt_string],
                    tonce = coinflex_tonce,
                    quantity = coinflex_quantity,
                    price = coinflex_working_bid*10000,
                    persist = False
                )
            with lock:
                logbuffer.append('PlaceOrder: '+str(coinflex_working_bid)+' '+str(coinflex_quantity))
                coinflex_api_counter.append(time.time())
                coinflex_currentbuyprice = coinflex_working_bid
                coinflex_currentbuyordertonce = coinflex_tonce
                coinflex_tonce += 1
        except:
            logbuffer.append('xbtaug: could not placeorder on coinflex:\n'+str(sys.exc_info()[0]))
            start_coinflex_websocket()

    if coinflex_currentsellprice == 0 and coinflex_ask != 0 and delay_quote_timer_flag and not deribit_fast_market_flag and \
       coinflex_position > -1*COINFLEX_MAX_POSITION and time.time()-coinflex_time_since_last_placeorder > 0.1 and not coinflex_global_stop_flag:
        try:
            if len(coinflex_api_counter)<COINFLEX_API_THRESHOLD:
                coinflex.PlaceOrder(
                    base = Assets[coinflex_xbt_string],
                    counter = Assets[coinflex_usdt_string],
                    tonce = coinflex_tonce,
                    quantity = -1*coinflex_quantity,
                    price = coinflex_working_ask*10000,
                    persist = False
                )
            with lock:
                logbuffer.append('PlaceOrder: '+str(coinflex_working_ask)+' '+str(-1*coinflex_quantity))
                coinflex_api_counter.append(time.time())
                coinflex_currentsellprice = coinflex_working_ask
                coinflex_currentsellordertonce = coinflex_tonce
                coinflex_tonce += 1
        except:
            logbuffer.append('xbtaug: could not placeorder on coinflex:\n'+str(sys.exc_info()[0]))
            start_coinflex_websocket()
            
    # modify orders; but the order matters or we might get a crossed trade against ourselves
    if coinflex_currentbuyprice != 0 and (coinflex_working_bid < coinflex_currentbuyprice or coinflex_currentsellprice - coinflex_working_bid > 0 or coinflex_currentsellprice == 0):
        if coinflex_currentbuyprice != 0 and coinflex_working_bid != coinflex_currentbuyprice and delay_quote_timer_flag:
            try:
                if len(coinflex_api_counter)<COINFLEX_API_THRESHOLD:
                    coinflex.ModifyOrder(
                        tonce = coinflex_currentbuyordertonce,
                        price = int(coinflex_working_bid*10000)
                    )
                with lock:
                    logbuffer.append('ModifyOrder: '+str(coinflex_working_bid)+' '+str(coinflex_quantity))
                    coinflex_api_counter.append(time.time())
            except:
                logbuffer.append('xbtaug: could not modifyorder on coinflex:\n'+str(sys.exc_info()[0]))
                start_coinflex_websocket()
            with lock:
                coinflex_currentbuyprice = coinflex_working_bid

        if coinflex_currentsellprice != 0 and coinflex_working_ask != coinflex_currentsellprice and delay_quote_timer_flag:
            try:
                if len(coinflex_api_counter)<COINFLEX_API_THRESHOLD:
                    coinflex.ModifyOrder(
                        tonce = coinflex_currentsellordertonce,
                        price = int(coinflex_working_ask*10000)
                    )
                with lock:
                    logbuffer.append('ModifyOrder: '+str(coinflex_working_ask)+' '+str(-1*coinflex_quantity))
                    coinflex_api_counter.append(time.time())
            except:
                logbuffer.append('xbtaug: could not modifyorder on coinflex:\n'+str(sys.exc_info()[0]))
                start_coinflex_websocket()
            with lock:
                coinflex_currentsellprice = coinflex_working_ask

    if coinflex_currentsellprice != 0 and (coinflex_working_ask > coinflex_currentsellprice or coinflex_working_ask - coinflex_currentbuyprice > 0):
        if coinflex_currentsellprice != 0 and coinflex_working_ask != coinflex_currentsellprice and delay_quote_timer_flag:
            try:
                if len(coinflex_api_counter)<COINFLEX_API_THRESHOLD:
                    coinflex.ModifyOrder(
                        tonce = coinflex_currentsellordertonce,
                        price = int(coinflex_working_ask*10000)
                    )
                with lock:
                    logbuffer.append('ModifyOrder: '+str(coinflex_working_bid)+' '+str(coinflex_quantity))
                    coinflex_api_counter.append(time.time())
            except:
                logbuffer.append('xbtaug: could not modifyorder on coinflex:\n'+str(sys.exc_info()[0]))
                start_coinflex_websocket()
            with lock:
                coinflex_currentsellprice = coinflex_working_ask
                
        if coinflex_currentbuyprice != 0 and coinflex_working_bid != coinflex_currentbuyprice and delay_quote_timer_flag:
            try:
                if len(coinflex_api_counter)<COINFLEX_API_THRESHOLD:
                    coinflex.ModifyOrder(
                        tonce = coinflex_currentbuyordertonce,
                        price = int(coinflex_working_bid*10000)
                    )
                with lock:
                    logbuffer.append('ModifyOrder: '+str(coinflex_working_ask)+' '+str(-1*coinflex_quantity))
                    coinflex_api_counter.append(time.time())
            except:
                logbuffer.append('xbtaug: could not modifyorder on coinflex:\n'+str(sys.exc_info()[0]))
                start_coinflex_websocket()
            with lock:
                coinflex_currentbuyprice = coinflex_working_bid

    # if a trade happens cancelall and reset timer
    if coinflex_trade_occurred_flag:
        with lock:
            coinflex_trade_occurred_flag = False
            coinflex_time_since_last_placeorder = time.time()
        try:
            coinflex.CancelAllOrders(
                tag = 99999999
            )
            with lock:
                coinflex_api_counter.append(time.time())
        except:
            logbuffer.append('xbtaug: could not cancelall on coinflex:\n'+str(sys.exc_info()[0]))
            start_coinflex_websocket()
            

    # if deribit is in fast market
    if deribit_fast_market_flag:
        coinflex_working_spread = FASTMARKET_SPREAD
    else:
        coinflex_working_spread = NORMAL_SPREAD
        
    # coinflex global stop triggered (but only once)
    if coinflex_global_stop_flag and not coinflex_global_stop_flag_done:
        coinflex_global_stop_flag_done = True
        try:
            coinflex.CancelAllOrders(
                tag = 99999999
            )
            with lock:
                coinflex_api_counter.append(time.time())
            logbuffer.append('xbtaug: stopped all trading')
        except:
            logbuffer.append('xbtaug: error on stopping all trading:\n'+str(sys.exc_info()[0]))

    if time.time()-printtimer > 2:
        printtimer = time.time()
        print('--------- xbtaug ---------')
        print('deribit:',bestbid,bestbidq,bestask,bestaskq,bidaskbalance)
        print('coinflex:', coinflex_ticker_bid, coinflex_ticker_ask)
        print('coinflex work levels:', round(coinflex_working_bid), round(coinflex_working_ask))
        print('coinflex min/max', MIN_FAIR_VALUE, MAX_FAIR_VALUE, 'coinflex fair:', round(coinflex_fair_value,2))
        print('c:', coinflex_position, 'cfmax:',COINFLEX_MAX_POSITION,'cfglobal:',coinflex_global_stop_flag)

    # cut api counters; it's a per second threshold
    temp = time.time()
    with lock:
        coinflex_api_counter = [i for i in coinflex_api_counter if temp-i<1]
    

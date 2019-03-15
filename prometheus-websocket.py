import websocket
import logging
import logging.handlers as handlers
from prometheus_client import start_http_server, Gauge
import time
import argparse
import sys

def on_message(ws, message):
    logger.info("Created a websocket connection")
    logger.info(message)
    logger.debug("Setting websocket_cf_up 1")
    g.set(1)

def on_error(ws, error):
    logger.debug("websocket connection to Cloudflare has been lost - on_error")
    g.set(0)

def on_close(ws):
    logger.debug("Closing websocket connection - on_close")
    g.set(0)


def on_open(ws):
    logger.debug("Initiating a websocket connection - on_open")

def main(host):
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://"+host+"/v1",
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close,
                                  on_open = on_open)

    while True:
        try:
            logger.info("Setting up continual websocket connection to "+host)
            ws.run_forever(ping_interval=45, ping_timeout=10)
            time.sleep(15)
        except KeyboardInterrupt:
            print("Keyboard interrupted")
            sys.exit(0)
            # pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Cloudflare websocket endpoint.")
    parser.add_argument("--port", help="Port to expose prometheus metrics on.", type=int)
    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Here we define our formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    logHandler = handlers.TimedRotatingFileHandler('prometheus-websocket-port-'+str(args.port)+'.log', when='M', interval=1, backupCount=2)
    logHandler.setLevel(logging.INFO)
    # Here we set our logHandler's formatter
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    g = Gauge('websocket_cf_up', 'Last time a cloudflare connection state was dropped')
    logger.info("Starting HTTP scrap endpoint on port "+str(args.port))
    start_http_server(args.port)

    main(args.host)

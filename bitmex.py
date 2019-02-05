import bitmex


def getquote(instrument):
    #print(instrument)
    client = bitmex.bitmex()
    client.Quote.Quote_get(symbol=instrument,count=1).result()


def main():
    getquote('XBTUSD')


if __name__ == '__main__':
    main()
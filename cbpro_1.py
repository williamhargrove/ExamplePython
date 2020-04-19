import numpy as np
import pandas as pd
import datetime as dt
import cbpro
import time

# CD Prod granted api credentials as strings
apiKey = "603178e57aa3423391604f06371480d4"
apiSecret = "FplRSsbCon+tbKP6F7vvTeZHbHxTnOsMfPk31lRFQT3hEyqhPGijcERgVfHxltn5XmBjZOiDv3k5/Pjl/N6teg=="
passphrase = "t7x17fc883p"

auth_client = cbpro.AuthenticatedClient(apiKey, apiSecret, passphrase)

# amount to initially invest
initInvestment = 20.00

# aount that will be used for purchase starts at the initial amount
funding = initInvestment

# currenty to trade, for reference:
# BTC-GBP
currency = 'BTC-GBP'


# return the ID of the specific currency account
def getSpecificAccount(cur):
    list_of_accounts = auth_client.get_accounts()
    for account in list_of_accounts:
        if account['currency'] == cur:
            return account['id']


# get the currency specific ID (take slice 0-2)
specificID = getSpecificAccount(currency[:3])

# granularity (seconds). 300 = data from every 5 mins
period = 300

# keep track of number of bot iterations
iteration = 1

# start by looking to buy
buy = True

#global price

def RSI(series,period):
    chg = price
    relativeStrength =
    relativeStrengthIndex = 100 - 100 / (1 + relativeStrength)
    return relativeStrengthIndex

while True:

    #try:
    historicData = auth_client.get_product_historic_rates(currency, granularity=period)
    #print(historicData)

    # returns a matrix of historic price data and covert to an array
    price = np.squeeze(np.asarray(np.matrix(historicData)[:, 4]))

    #print(price)

    # wait for 1 second to avoid API limit
    time.sleep(1)

    # get latest data
    newData = auth_client.get_product_ticker(product_id=currency)
    #print(newData)
    currentPrice = newData['price']

    #except:
    #    print("Error Encountered")

    # calculate the rate of change 11 and 14 units back, then sum them

    ROC11 = np.zeros(13)
    ROC14 = np.zeros(13)
    ROCSUM = np.zeros(13)

    for ii in range(0,13):
        ROC11[ii] = (100 * (price[ii]-price[ii + 11]) / float(price[ii + 11]))
        ROC14[ii] = (100 * (price[ii]-price[ii + 14]) / float(price[ii + 14]))
        ROCSUM[ii] = (ROC11[ii] + ROC14[ii])

    # Calculate the past 4 Coppock values with Weighted Moving Average
    coppock = np.zeros(4)
    for ll in range(0,4):
        coppock[ll] = (((1*ROCSUM[ll+9]) + (2*ROCSUM[ll+8]) + (3*ROCSUM[ll+7]) +
                        (4*ROCSUM[ll+6]) + (5*ROCSUM[ll+5]) + (6*ROCSUM[ll+4]) +
                        (7*ROCSUM[ll+3]) + (8*ROCSUM[ll+2]) + (9*ROCSUM[ll+1]) +
                        (10*ROCSUM[ll])) / float(55))

    # Calculate the past 3 derivatives of the Coppock Curve
    coppockD1 = np.zeros(3)
    for mm in range(3):
        coppockD1[mm] = coppock[mm] - coppock[mm+1]

    # maximum amount of crypto that can be purchased with funds
    possiblePurchase = (float(funding)) / float(currentPrice)

    # amount of currency owned
    owned = float(auth_client.get_account(specificID)['available'])

    # value of cryptocurrency
    possibleIncome = float(currentPrice) * owned

    # calculate 14 period RSI
    relativeStrengthIndex = RSI(price, 14)

    # buy conditions: latest derivative is + and previous is -
    if buy == True and (coppockD1[0]/abs(coppockD1[0])) == 1.0 and (coppockD1[1]/abs(coppockD1[1])) == -1.0:
        # print(coppockD1[0]/abs(coppockD1[0]))
        # print(coppockD1[1] / abs(coppockD1[1]))

        auth_client.place_market_order(product_id=currency, side='buy', funds = str(funding))

        message = "Buying approximately " + str(possiblePurchase) + " " + \
        currency + " Now @ " + str(currentPrice) + "/Coin. Total = " + \
        str(funding)

        print(message)

        # update funding level and buy variable
        funding = 0
        buy = False

    if buy == False and (coppockD1[0] / abs(coppockD1[0])) == -1.0 and (coppockD1[1]/abs(coppockD1[1])) == 1.0:
        # print (coppockD1[0] / abs(coppockD1[0]))
        # print (coppockD1[1]/abs(coppockD1[1]))

        # place the order
        auth_client.place_market_order(product_id=currency, side='sell', size = str(owned))

        message = "Selling " + str(owned) + " " + currency + "Now @ " + \
        str(currentPrice) + "/Coin. Total = " + str(possibleIncome)

        print(message)

        # update funding level and buy variable
        funding = int(possibleIncome)
        buy = True

    # stop loss: sell everything and stop trading if value is less than 80% of initial investment
    if (possibleIncome+funding) <= 0.8 * initInvestment:

        # if there is any crypto, sell it
        if owned > 0.0:
            auth_client.place_market_order(product_id=currency, side='sell', size = str(owned))
            print("Stop loss hit: sold all")
        break

    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("iteration number", iteration)

    # Print the details for reference
    print("Current Price: ", currentPrice)
    print("Your Funds = ", funding)
    print("You Own ", owned, "BTC")
    print("Coppock left", coppockD1[0] / abs(coppockD1[0]))
    print("Coppock right",coppockD1[1] / abs(coppockD1[1]))

    # Wait for 5 minutes before repeating
    time.sleep(period)
    iteration += 1
import talib
import numpy as np
import pandas as pd
import time
import json
import requests
import pymongo
import pprint


apiKey = 'JVECI853Y04MXZAW'

#------------------------------------------------------
# DATABASE CONNECT
#------------------------------------------------------
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.forex

collectionEUR = db.eur
collectionCNY = db.cny
collectionJPY = db.jpy
collectionBTC = db.btc

while True:

#------------------------------------------------------
# TIME
#------------------------------------------------------
    NY = 'America/New_York'
    now = pd.Timestamp.now(tz=NY)
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%m/%d/%Y")


#------------------------------------------------------
# ALPHA VANTAGE API CALLS 1 minute with LOAD
#------------------------------------------------------
    try:


        usdBTC = requests.get("https://rest.coinapi.io/v1/exchangerate/BTC?apikey=92CE5212-5303-4D09-B8AF-5E079ACA72D2")
        usdEUR = requests.get("https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=EUR&interval=1min&outputsize=compact&apikey=" + apiKey)
        usdCNY = requests.get("https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=CNY&interval=1min&outputsize=compact&apikey=" + apiKey)
        usdJPY = requests.get("https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=JPY&interval=1min&outputsize=compact&apikey=" + apiKey)
        data1 = usdEUR.json()
        data2 = usdCNY.json()
        data3 = usdJPY.json()
        data4 = usdBTC.json()

        EURdata1_list = list(data1['Time Series FX (1min)'])[0]

        print(f"The current time is {current_date} {current_time}")
        print("")

        EURpost = data1['Time Series FX (1min)'][EURdata1_list]
        EURpost['open'] = EURpost['1. open']
        EURopen = EURpost['open']
        EURpost['high'] = EURpost['2. high']
        EURhigh = EURpost['high']
        EURpost['low'] = EURpost['3. low']
        EURlow = EURpost['low']
        EURpost['close'] = EURpost['4. close']
        EURclose = EURpost['close']

        CNYdata1_list = list(data2['Time Series FX (1min)'])[0]

        CNYpost = data2['Time Series FX (1min)'][CNYdata1_list]
        CNYpost['open'] = CNYpost['1. open']
        CNYopen = CNYpost['open']
        CNYpost['high'] = CNYpost['2. high']
        CNYhigh = CNYpost['high']
        CNYpost['low'] = CNYpost['3. low']
        CNYlow = CNYpost['low']
        CNYpost['close'] = CNYpost['4. close']
        CNYclose = CNYpost['close']

        JPYdata1_list = list(data3['Time Series FX (1min)'])[0]

        JPYpost = data3['Time Series FX (1min)'][JPYdata1_list]
        JPYpost['open'] = JPYpost['1. open']
        JPYopen = JPYpost['open']
        JPYpost['high'] = JPYpost['2. high']
        JPYhigh = JPYpost['high']
        JPYpost['low'] = JPYpost['3. low']
        JPYlow = JPYpost['low']
        JPYpost['close'] = JPYpost['4. close']
        JPYclose = JPYpost['close']

        rates = data4['rates']

        for assest in rates:
            if assest['asset_id_quote'] == 'USD':

                BTCclose = assest['rate']

        insertBTC = {
                'date': current_date,
                'time': current_time,
                'close': BTCclose
            }

        collectionBTC.insert_one(insertBTC)

        insertEUR = {
                'date': current_date,
                'time': current_time,
                'open': EURopen,
                'high': EURhigh,
                'low' : EURlow,
                'close': EURclose

        
            }


        collectionEUR.insert_one(insertEUR)



        insertCNY = {
                'date': current_date,
                'time': current_time,
                'open': CNYopen,
                'high': CNYhigh,
                'low' : CNYlow,
                'close': CNYclose


            }


        collectionCNY.insert_one(insertCNY)



        insertJPY = {
                'date': current_date,
                'time': current_time,
                'open': JPYopen,
                'high': JPYhigh,
                'low' : JPYlow,
                'close': JPYclose


            }


        collectionJPY.insert_one(insertJPY)
        print("DB LOADED")
        print("")

    except Exception as e:
        print(e)


#------------------------------------------------------
# HISTORY
#------------------------------------------------------
    db = client.forex

    collectionEUR = db.eur
    listingsEUR = db.eur.find()

    listings_listEUR = []
    for listingEUR in listingsEUR:
    #     print(listing)

        listings_listEUR.append(float(listingEUR["close"]))

    pricehistoryEUR = listings_listEUR[-100:]

    priceEUR = np.array(pricehistoryEUR)

    len_priceEUR = len(priceEUR)


    collectionCNY = db.cny
    listingsCNY = db.cny.find()

    listings_listCNY = []
    for listingCNY in listingsCNY:
    #     print(listing)

        listings_listCNY.append(float(listingCNY["close"]))

    pricehistoryCNY = listings_listCNY[-100:]

    priceCNY = np.array(pricehistoryCNY)

    len_priceCNY = len(priceCNY)


    collectionJPY = db.jpy
    listingsJPY = db.jpy.find()

    listings_listJPY = []
    for listingJPY in listingsJPY:
    #     print(listing)

        listings_listJPY.append(float(listingJPY["close"]))

    pricehistoryJPY = listings_listJPY[-100:]

    priceJPY = np.array(pricehistoryJPY)

    len_priceJPY = len(priceJPY)

    collectionBTC = db.btc
    listingsBTC = db.btc.find()

    listings_listBTC = []
    for listingBTC in listingsBTC:
    #     print(listing)

        listings_listBTC.append(float(listingBTC["close"]))

    pricehistoryBTC = listings_listBTC[-100:]

    priceBTC = np.array(pricehistoryBTC)

    len_priceBTC = len(priceBTC)


#------------------------------------------------------
# TALIB
#------------------------------------------------------
    if len_priceEUR > 13:
        try:


            realEUR = talib.RSI(priceEUR, timeperiod=50)
            realCNY = talib.RSI(priceCNY, timeperiod=50)
            realJPY = talib.RSI(priceJPY, timeperiod=50)
            realBTC = talib.RSI(priceBTC, timeperiod=30)

        except Exception as e:
            print(e)

# ------------------------------------------------------
# MAIN LOGIC
#------------------------------------------------------

        # print(f'USD/EUR Close: {EURclose}')
        print("PRICE HISTORY USD/EUR")
        print(priceEUR)
        print("_____________________________________________")
        print("")

        # print(f"USD/CNY Close: {CNYclose}")
        print("PRICE HISTORY USD/CNY")
        print(priceCNY)
        print("_____________________________________________")
        print("")

        # print(f'USD/JPY Close: {JPYclose}')
        print("PRICE HISTORY USD/JPY")
        print(priceJPY)
        print("_____________________________________________")
        print("")

        # print(f'USD/JPY Close: {JPYclose}')
        print("PRICE HISTORY USD/BTC")
        print(priceBTC)
        print("_____________________________________________")
        print("")

        print(f'RSI EUR: {realEUR[-1]}')
        print(f'RSI CNY: {realCNY[-1]}')
        print(f'RSI JPY: {realJPY[-1]}')
        print(f'RSI BTC: {realBTC[-1]}')
        print("_____________________________________________")
        print("")

        if realEUR[-1] < 30:
            print("EUR IS A BUY RECOMMENDATION")

        elif realEUR[-1] > 70:
            print("EUR IS A SELL RECOMMENDATION")

        else:
            print("EUR IS A HOLD RECOMMENDATION")

        if realCNY[-1] < 30:
            print("CNY IS A BUY RECOMMENDATION")

        elif realCNY[-1] > 70:
            print("CNY IS A SELL RECOMMENDATION")

        else:
            print("CNY IS A HOLD RECOMMENDATION")

        if realJPY[-1] < 30:
            print("JPY IS A BUY RECOMMENDATION")

        elif realJPY[-1] > 70:
            print("JPY IS A SELL RECOMMENDATION")

        else:
            print("JPY IS A HOLD RECOMMENDATION")

        if realBTC[-1] < 30:
            print("BTC IS A BUY RECOMMENDATION")

        elif realBTC[-1] > 70:
            print("BTC IS A SELL RECOMMENDATION")

        else:
            print("BTC IS A HOLD RECOMMENDATION")




    print("")
    time.sleep(10)

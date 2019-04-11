import talib
import numpy as np
import pandas as pd
import time
import logging
import json
import requests
import pymongo



#------------------------------------------------------
# DATABASE CONNECT
#------------------------------------------------------
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.forex
    collection = db.time


while True:
#------------------------------------------------------
# BROKERAGE CALLS --- TODO
#------------------------------------------------------
    # account  = api.get_account()
    # position = api.list_positions()
    # clock    = api.get_clock()
    # orders   = api.list_orders()


#------------------------------------------------------
# TIME
#------------------------------------------------------
    now = clock.timestamp
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%m/%d/%Y")
    now = pd.Timestamp.now(tz=NY)


    print(f"The current time is {current_date} {current_time}")
    print("")



#------------------------------------------------------
# ALPHA VANTAGE API CALLS 1 minute with LOAD
#------------------------------------------------------
    try:


        usdEUR = requests.get("https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=EUR&interval=1min&outputsize=full&apikey=" + apiKey)
        usdCNY = requests.get("https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=CNY&interval=1min&outputsize=full&apikey=" + apiKey)
        usdJPY = requests.get("https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=JPY&interval=1min&outputsize=full&apikey=" + apiKey)
        data1 = usdEUR.json()
        data2 = usdCNY.json()
        data3 = usdJPY.json()
        last_price1= data1['last']['price']
        last_price2= data2['last']['price']
        last_price3= data3['last']['price']


        print(f'LAST PRICE of USD/EUR: {last_price1}')
        print(f'LAST PRICE of USD/CNY: {last_price2}')
        print(f'LAST PRICE of USD/JPY: {last_price3}')

        post = {
                'date': current_date,
                'time': current_time,
                'price': last_price
            }


        collection.insert_one(post)
        print("DB LOAD")
        print("********************************************")
        print("")
    except Exception as e:
        print(e)


#------------------------------------------------------
# HISTORY
#------------------------------------------------------

    listings = db.time.find()

    listings_list = []
    for listing in listings:
    #     print(listing)

        listings_list.append(listing['price'])

    pricehistory = listings_list[-100:]

    price = np.array(pricehistory)

    len_price = len(price)
    print("PRICE HISTORY")
    print(price)
    print("********************************************")

#------------------------------------------------------
# MACD
#------------------------------------------------------
    if len_price > 50:
        try:
            macd_raw, signal, macd_hist = talib.MACD(price,
                                                    fastperiod=12,
                                                    slowperiod=26,
                                                    signalperiod=9)


            real = talib.RSI(price, timeperiod=14)

            macdaddy = round(macd_raw[-1],2) - round(signal[-1],2)

            print("")
            print(f'MACD: {round(macdaddy,2)}')
            print("_____________________________________________")
            print(f'Macd_raw: {macd_raw[-1]}')
            print(f'signal: {signal[-1]}')
            print(f'macd_hist: {macd_hist[-1]}')
            print("_____________________________________________")
            print(f'RSI: {real[-1]}')
            print("_____________________________________________")
        except Exception as e:
            print(e)

#------------------------------------------------------
# MAIN LOGIC
#------------------------------------------------------

        print("OPEN FOR TRADING")
        if real[-1] < 20  and len(position) <= 0 and len(orders) <= 0:
            try:
                print("BUYING")
                order = api.submit_order()
            except Exception as e:
                print(e)

        elif real[-1] > 75 and len(position) > 0 and len(orders) <= 0:
            try:
                print("SELLING")
                order = api.submit_order()
            except Exception as e:
                print(e)
    else:
        print("NOT TIME TO START TRADING YET- STILL LOADING")

        print("")

#------------------------------------------------------
# CURRENT POSITIONS
#------------------------------------------------------
    if len(position) <= 0:
        print('YOU HAVE NO POSITIONS')
    elif len(position) > 0:
        pos = position[0]
        print(f'You have {pos.qty} Positions of {pos.symbol} ')
        print(f'Market Value {pos.market_value} AVG Entry Price {pos.avg_entry_price}')

    print("")
    time.sleep(10)

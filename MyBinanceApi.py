#!/usr/bin/env python

import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
import timeit
#config_logging(logging, logging.DEBUG)

spot_client = Client(base_url="https://api.binance.com")

currencylist =[]
f = open('currencyList.txt', 'r')
for line in f.readlines():
    currencylist.append(line.strip())
f.close()
_avgtime = 0
def updateList():
    global currencylist
    currencylist = []
    f = open('currencyList.txt', 'r')
    for line in f.readlines():
        currencylist.append(line.strip())
    f.close()

def getPrice():
    global _avgtime
    global currencylist
    result=[]
    start = timeit.default_timer()
    apiResult = spot_client.ticker_price()
    for item in apiResult:
        if currencylist.count(item["symbol"]) is not 0:
            price = float(item['price'])
            price = str(price)
            result.append(item["symbol"]+": "+price)
    stop = timeit.default_timer()
    _avgtime =round((stop-start)*1000/len(currencylist),2)
    #print('avg Time: ', str(time)+" ms")
    return result


def getAvgResponseTime():
    global _avgtime
    return _avgtime

def getAll():
    result = spot_client.ticker_price()
    list =[]
    #print(result)
    #print(len(result))
    num = 0
    for item in result:
        if (item["symbol"].find("USDT")) is not -1:
            #print(item["symbol"])
            num+=1
            list.append(item["symbol"])
    #print(num)
    return list

#getAll()
# if __name__ == '__main__':
#     price = spot_client.ticker_price()
#     print(price)
#     test ="BTCUSDT"
#     for item in currencylist:
#         print (float((([x["price"][0] for x in price if x["symbol"]==item]))))


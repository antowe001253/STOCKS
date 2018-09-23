from yahoo_finance import Share
from rtstock.stock import Stock
from googlefinance import getQuotes
import json
json_data =(json.dumps(getQuotes('asm'), indent=2))
print(json_data)
trade_price = ""
try:
	trade_price = getQuotes('eyeg')[0]["LastTradePrice"]
except: print("Not FOund")
print (trade_price)
print (type(trade_price))
yahoo = Share('EYEG')
yahoo.refresh()
##print ("Open -> ",yahoo.get_open())
#print ("Current Price -> ",yahoo.get_price())
#print ("Ave Volume -> ",yahoo.get_avg_daily_volume())
#print ("Volume -> ",yahoo.get_volume())
#print ("Time -> ",yahoo.get_trade_datetime())

#stock = Stock('EYEG')
#print(stock.get_latest_price())
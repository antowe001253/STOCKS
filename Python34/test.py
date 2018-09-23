from get_ticker_info import *
ticker="DRYS"
print(ticker)
get_info(ticker,'Previous Close')
get_info(ticker,'Open')
get_info(ticker,'Volume')
get_info(ticker,'Avg. Volume')
get_info(ticker,'Market Cap')
get_info(ticker,'PE Ratio')
get_info(ticker,'Forward Dividend')
print("Price -> ",price_yahoo_parsing(ticker=ticker)[0])

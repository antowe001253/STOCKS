from get_ticker_info import *
from multiprocessing import Process
from datetime import date
import calendar
from connect_mysql import *
import requests
import time
def send_mysql(ticker,price,website_time,news):
		print("-"*50, ticker)
		volume=get_info(ticker=ticker,info="Volume",display=False)
		#print(volume)
		if str(volume).find(",")>=0:
				volume=volume.replace(",","")
		#print(volume)
		#k=input("-------------")
		opening=get_info(ticker=ticker,info="OPEN-value",display=False)
		beta=get_info(ticker=ticker,info="Beta",display=False)
		P_E=get_info(ticker=ticker,info="PE Ratio",display=False)
		avg_volume=get_info(ticker=ticker,info="Avg. Volume",display=False)
		previous_close=get_info(ticker=ticker,info="Previous Close",display=False)
		dividents=get_info(ticker=ticker,info="Forward Dividend",display=False)
		if str(dividents).find("%")>=0:
				dividents=dividents.replace("%","")
		market_cap=get_info(ticker=ticker,info="Market Cap",display=False)
		if str(market_cap).lower().find("m")>=0:
			market_cap=market_cap.lower().split("m")[0]
			market_cap=float(market_cap)*1000000
		if str(market_cap).lower().find("b")>=0:
			market_cap=market_cap.lower().split("b")[0]
			market_cap=float(market_cap)*1000000000
		if str(market_cap).lower().find("k")>=0:
			market_cap=market_cap.lower().split("k")[0]
			market_cap=float(market_cap)*1000
		earnings=0
		p_growth=0
		mysql_send_data(website_time,ticker,price,volume,opening,P_E,beta,earnings,dividents,p_growth,market_cap,news)
		
		
		
def getting_list_of_record(data):
	for i,line in enumerate(data):
		if line.find("Done writting in file")>=0 : continue
		data_split=line.split(" ")
		#print (data_split)
		try: k="[",i,"-",len(data),"]",data_split[0],data_split[1],data_split[2]," ".join(data_split[3:])
		except: print(data_split)
		Process(target=send_mysql,args=(data_split[0],data_split[1],data_split[2]," ".join(data_split[3:]))).start()
		#send_mysql(data_split[0],data_split[1]," ".join(data_split[2:]))

if __name__ == '__main__':
	start=time.time()
	processes=[]
	while(1):
		
		nbr_of_stock_to_be_sent_to_db=open("data/nbr_of_stock_to_be_sent_to_db.txt",'r')
		data=nbr_of_stock_to_be_sent_to_db.read()
		if data.find("Done writting in file")>=0:
			data_split=data.split("\n")
			#print(data_split[-1])
			print("----------> ",len(data_split))
			getting_list_of_record(data_split)
			#processes.append(Process(target=getting_list_of_record,args=data_split))
			#Process(target=getting_list_of_record,args=data_split).start()
			#getting_list_of_record(data_split)
			#print("="*25)
			#k=input()
			start=time.time()
			nbr_of_stock_to_be_sent_to_db=open("data/nbr_of_stock_to_be_sent_to_db.txt",'w')
		#for p in processes:
		#	if p.is_alive()==None: p.start()
		#for p in processes:
		#	print(p.is_alive())
		print("Sleeping -> ",time.time()-start)
		time.sleep(5)
		

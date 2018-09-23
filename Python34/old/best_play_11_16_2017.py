# THis is just for super Nova, no for dip 
from multiprocessing import Process
from get_ticker_info import *
from connect_mysql import *
import requests
import time


#def send_mysql(ticker,price,news):
def send_mysql(ticker,price,news):
		print("-"*50)
		volume=get_info(ticker=ticker,info="Volume",display=False)
		#print(volume)
		if str(volume).find(",")>=0:
				volume=volume.replace(",","")
		#print(volume)
		#k=input("-------------")
		opening=get_info(ticker=ticker,info="Open",display=False)
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
		mysql_send_data(ticker,price,volume,opening,P_E,earnings,dividents,p_growth,market_cap,news)
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)  
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls() 
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close() 
        print ('successfully sent the mail')
        return 1
    except:
        print ("failed to send mail")
        return 0

scanner ={} 
list_of_symbols=[] # fom the app scanner_stocks
active_scan={} # stock which are actif
timer ={}

def morning_sticker_data():
    global scanner
    global ticker_news
    print("===== Loading morning Stickers and Prices")
    symbols_and_prices_file=open("symbols_and_prices.txt","r")
    symbols_and_prices_text = symbols_and_prices_file.read()
    symbols_and_prices_file.close()
    scanner_from_file = symbols_and_prices_text.split("\n")
    #print(scanner_from_file)
    for each_item in scanner_from_file:
        if len(each_item)>0:
            ticker_news[each_item.split(" ")[0]]=(" ").join(each_item.split(" ")[3:])
            timer[each_item.split(" ")[0]]= int((each_item.split(" ")[2]).split(".")[-1])
            scanner[each_item.split(" ")[0]] = float(each_item.split(" ")[1])
            print(each_item)

#k=input(scanner)
        







   
ticker_news={}
def new_stikers_from_scanner_stock_APP():
	global ticker_news
	global list_of_symbols
	symbols_file=open("symbols.txt","r")
	symbols_text = symbols_file.read()
	symbols_file.close()
	#print("In new_stikers_from_scanner_stock_APP",len(symbols_text))
	symbols_text_split = symbols_text.split("\n")
	if 	(len(symbols_text_split)>0):
		for line in symbols_text_split:
			ticker_news[line.split(" ")[0]]=(" ").join(line.split(" ")[1:])
			each_symbol=line.split(" ")[0]
			if len(each_symbol)>0 :
				exit = ""
				#print("before checking price")
				exit=price_yahoo_parsing(ticker=each_symbol)[0]
				#print(exit)
				if type(exit) == float:
					#print("===== [New] Loading Stickers from scanner_stocks App -> ",)
					#print(type(exit))
					#print(each_symbol)
					#k=input("Ticket found")
					print("Ticket found: ",each_symbol,exit)
					list_of_symbols.append(each_symbol)
				else:
					f=10
					print("Not Found",each_symbol)
					#print("No ticket founds")
				#print(each_symbol)
				#k=input(each_symbol)
	symbols_file=open("symbols.txt",'w').close()
def getting_price_for_new_stickers():
    global ticker_news
    global timer
    global list_of_symbols
    global scanner 
	
    for ticker in list_of_symbols:
        if ticker not in scanner:
            #print("===== Getting orices for all New Stickers", len(list_of_symbols))
            price = price_yahoo_parsing(ticker=ticker)[0]
			
            #print(ticker,"-> ",price)
            if type(price) != float: continue
          
			
				#continue # Ticker no found
            if price <= 0 :                 			
                continue # Ticker no found

            #print("[ADDING... ]",ticker)
            #send_mysql(ticker=ticker,price=price,news=ticker_news[ticker])
            scanner [ticker]=price
            symbols_and_prices_file=open("symbols_and_prices.txt","a") 
            symbols_and_prices_file.write(ticker+" "+str(price)+" "+time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))+" "+ticker_news[ticker]+'\n')
			
            #timer[ticker]=time.strftime("%m/%d/%Y ---- %H:%M:%S")
            timer[ticker]=((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))
			
			#symbols_and_prices_file.write(ticker+" "+str(price)+'\n')
            symbols_and_prices_file.close()
            print("====[SAVING... ]",ticker," ",price)
    list_of_symbols = [] # all that data is now in scanner
    #print(scanner)

#morning_sticker_data()
para_list=[]
if  __name__=='__main__':
	while(1):
    
		morning_sticker_data_="Yes"
		if morning_sticker_data_=="Yes":morning_sticker_data()
		morning_sticker_data_="No"
	#if (int(time.strftime("%H"))<16 and int(time.strftime("%H"))>9) or (int(time.strftime("%H"))==9 and int(time.strftime("%M"))>29):
	
		new_stikers_from_scanner_stock_APP()
		#print("Done with new tickers")
		if len(list_of_symbols)>0:
			
			getting_price_for_new_stickers()
		#k=input(scanner)
		
		start=time.time()
        
		for symbol, initial_price in scanner.items():
			
			actual_price = price_yahoo_parsing(ticker=symbol)[0]
			if type(actual_price)!= float: 
			    #print("Price: ",actual_price)
			    #print("Symbol: ",symbol)
			    continue
				
			price_dif = actual_price-initial_price
			
			active_scan[symbol]=price_dif
			#for symbol_name, prive_value in active_scan.items():
			print("[",len(active_scan),"] ",symbol,"\t",str(actual_price).zfill(5),"<-Act Init->",initial_price,"\t","{0:.5f}".format(price_dif), " "+time.strftime("---%H:%M:%S "))#,symbol_name,"\t",prive_value)

				#print("[",len(active_scan),"] ",symbol,"\t",price_dif)
			news="" if symbol not in ticker_news else ticker_news[symbol]
			if symbol not in ticker_news:
				print(symbol)
				k=input()
			para_list.append([symbol,actual_price,news])
			
			#send_mysql(ticker=symbol,price=actual_price,news=news)
			if price_dif >= 0.05:
				if -timer[symbol]+(int(time.strftime("%d"))*24)+(int(time.strftime("%H"))) == 0: statut="[NEW]" 			
				else: statut=""
				
				message = "Stock Name: "+symbol+'\n'+"Now: "+str(actual_price)+'\n'+"Opening: "+str(initial_price)+'\n'+"Dif: "+str(price_dif)+'\n'+'\n'+"Time: "+time.strftime("%m/%d/%Y ---- %H:%M:%S")+"\t"+time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))+'\n'+'Volume =%s'%get_info(ticker=symbol,info="Volume",display=False)+'\n'+news+'\n'
				validation = send_email("alex.don257@gmail.com","thebest001","alex.don257@gmail.com","####"+statut+" ["+symbol+"] at ",str(actual_price)+statut+message)
				if validation ==1: scanner[symbol]= actual_price
				print("Timer:",-timer[symbol]+(int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))         
				print(statut,"===========",timer[symbol],[symbol]," This Stock Is ACTIF       now: ",time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H")))))
		end=time.time()
		sleeping_time=45 
		if int(time.strftime("%H")) in [19,20,21,22,23,24,1,2,3,4,5,6,7]:
				sleeping_time=3600
		print("Sleeping for -> ",sleeping_time-(end-start))
		print("Length -> ",len(para_list))
		nbr_of_stock_to_be_sent_to_db=para_list[:]
		print("nbr_of_stock_to_be_sent_to_db -> ",len(nbr_of_stock_to_be_sent_to_db))
		items_sent=0
		
		for each_record_count in range(0,len(para_list)):
			print("[",each_record_count,"] | to BD -> ",para_list[each_record_count][0])
			send_mysql(para_list[each_record_count][0],para_list[each_record_count][1],para_list[each_record_count][2])
			items_sent+=1
			if int(time.time()-start)>sleeping_time: break
		#for time_available in range(0,abs(int(sleeping_time-(end-start)))):
		#		if time_available>=len(nbr_of_stock_to_be_sent_to_db):break
		#		print("[",time_available,"] | to BD -> ",para_list[time_available][0])
		#		send_mysql(para_list[time_available][0],para_list[time_available][1],para_list[time_available][2])
		#		items_sent+=1
		para_list[:items_sent]=[]
		print(len(para_list))
		end=time.time()
		print("Sleeping for -> ",sleeping_time-(end-start))
		sleep_time=sleeping_time-(end-start)
		time.sleep(sleep_time if sleep_time>=0 else 0)
		print("-"*50)
		
		command_file = open("best_play_file_commands.txt",'r')
		key_command = command_file.read()
		if len(key_command)>0:
			print(key_command)
			if key_command.find("print")>=0:
				#for symbol_name, prive_value in active_scan.items():
				print("[",len(scanner),"] "+str(symbol_name)+"  "+str(prive_value)+"  "+time.strftime("%b %d, %Y---%H:%M:%S "))#,symbol_name,"\t",prive_value)

			#k=input("-----------")
		#print("="*50)
		#print("[",len(scanner),"] "+time.strftime("%b %d, %Y---%H:%M:%S "))#,symbol_name,"\t",prive_value)
    
	#else:	
	     
		#import os 
		#os.system('cls')  # for Windows 
		#remaining_time=0
		#if int(time.strftime("%H")) >=16:
		    #remaining_time=int(25*60*60 )-((int(time.strftime("%H"))*60 + int(time.strftime("%M")))*60 + int(time.strftime("%S")))+ ((9*60)+30)*60
		#else: remaining_time = ((9*60)+30)*60 - ((int(time.strftime("%H"))*60 + int(time.strftime("%M")))*60 + int(time.strftime("%S")))
		#print(time.strftime("%H:%M:%S "))
		#print(remaining_time)
		
		
		time.sleep(5)
		
	

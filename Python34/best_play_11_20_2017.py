# THis is just for super Nova, no for dip 
from multiprocessing import Process
from get_ticker_info import *
from connect_mysql import *
import requests
import time
from datetime import date
import calendar


#def send_mysql(ticker,price,news):
def send_mysql(ticker,price,news):
		#print("-"*50, ticker)
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
        #print ('successfully sent the mail')
        #return 1
    except:
        """ """
        #print ("failed to send mail")
        #return 0

scanner ={} 
list_of_symbols=[] # fom the app scanner_stocks
active_scan={} # stock which are actif
timer ={}

def morning_sticker_data():
    global scanner
    global ticker_news
    key_begin="start^~^"
    key_end="done^~^"
    #print("===== Loading morning Stickers and Prices")
    symbols_and_prices_file=open("data/symbols_and_prices.txt","r")
    symbols_and_prices_text = symbols_and_prices_file.read()
    symbols_and_prices_text=symbols_and_prices_text.replace(key_begin,"")
    symbols_and_prices_text=symbols_and_prices_text.replace(key_end,"")
    symbols_and_prices_file.close()
    scanner_from_file = symbols_and_prices_text.split("\n")
    #print(scanner_from_file)
    for each_item in scanner_from_file:
        if len(each_item)>0:
            #print(each_item)
            ticker_news[each_item.split(" ")[0]]=(" ").join(each_item.split(" ")[3:])
            #print((each_item.split(" ")[2]).split(".")[-1])
           # k=input()
            try:
                timer[each_item.split(" ")[0]]= int((each_item.split(" ")[2]).split(".")[-1])
                scanner[each_item.split(" ")[0]] = float(each_item.split(" ")[1])
            except:
                print("*"*50)
                print("Error")
                print("This shsould be a daate-> ",each_item)
                continue
                
            #print(each_item)

#k=input(scanner)
        







   
ticker_news={}
def new_stikers_from_scanner_stock_APP():
	
	global ticker_news
	global list_of_symbols
	symbols_file=open("data/symbols.txt","r")
	symbols_text = symbols_file.read()
	symbols_file.close()
	#print("In new_stikers_from_scanner_stock_APP",len(symbols_text))
	symbols_text_split = symbols_text.split("\n")
	data_length=len(set(symbols_text_split))
	
	#[print(i) for i in set(symbols_text_split)]
	#print("-"*100)
	#[print(i) for i in symbols_text_split]
	#k=input()
	if 	(len(symbols_text_split)>0):
		
		for count, line in enumerate(set(symbols_text_split)):
			#print("-------------------------------",)
			ticker_news[line.split(" ")[0]]=(" ").join(line.split(" ")[1:])
			each_symbol=line.split(" ")[0]
			#print("-------------------------------",each_symbol)
			if len(each_symbol)>0 and each_symbol not in list_of_symbols :
				exit = ""
				#print("before checking price")
				exit=price_yahoo_parsing(ticker=each_symbol)[0]
				#print(exit)
				if type(exit) == float:
					#print("===== [New] Loading Stickers from scanner_stocks App -> ",)
					#print(type(exit))
					#print(each_symbol)
					#k=input("Ticket found")
					#print("Ticket found: ",each_symbol,exit)
					print(count,"/",data_length)
					list_of_symbols.append(each_symbol)
				else:
					f=10
					#print("Not Found",each_symbol)
					#print("No ticket founds")
				#print(each_symbol)
				#k=input(each_symbol)
	#k=input()
	symbols_file=open(r"C:/Users/Alex.Ntowe/Documents/Project/Python/STOCKS/Python34/data/symbols.txt",'w').close()
def getting_price_for_new_stickers():
    global ticker_news
    global timer
    global list_of_symbols
    global scanner
    key_begin="start^~^"
    key_end="done^~^"
	
    for ticker in list_of_symbols:
        symbols_and_prices_file=open("data/symbols_and_prices.txt","a")
        symbols_and_prices_file.write(key_begin)
        symbols_and_prices_file.close()
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
            symbols_and_prices_file=open("data/symbols_and_prices.txt","a") 
            symbols_and_prices_file.write((ticker+" "+str(price)+" "+time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))+" "+ticker_news[ticker]).replace("\n","")+'\n')
			
            #timer[ticker]=time.strftime("%m/%d/%Y ---- %H:%M:%S")
            timer[ticker]=((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))
			
			#symbols_and_prices_file.write(ticker+" "+str(price)+'\n')
            symbols_and_prices_file.close()
            print("====[SAVING... ]",ticker," ",price)
    list_of_symbols = [] # all that data is now in scanner
    #print(scanner)
    symbols_and_prices_file=open("data/symbols_and_prices.txt","a")
    symbols_and_prices_file.write(key_end)
    symbols_and_prices_file.close()

#morning_sticker_data()
para_list=[]
if  __name__=='__main__':
	morning_sticker_data_="Yes"
	while(1):
		#try:
			if int(time.strftime("%H")) in [20,21,22,23,24,0,1,2,3,4,5,6,7]:
				sleeping_time=3600
				continue
			my_date = date.today()
			day=calendar.day_name[my_date.weekday()]
			hold_dates=['Sunday','Saturday']
			if day in hold_dates :
				print("Today's date -> ",day)
				print("Sleeping for 3600 seonds")
				time.sleep(3600)
			else:
				nbr_of_stock_to_be_sent_to_db=open("data/nbr_of_stock_to_be_sent_to_db.txt","a")
				
				if morning_sticker_data_=="Yes":morning_sticker_data()
				morning_sticker_data_="No"
				
			#if (int(time.strftime("%H"))<16 and int(time.strftime("%H"))>9) or (int(time.strftime("%H"))==9 and int(time.strftime("%M"))>29):
			
				new_stikers_from_scanner_stock_APP()
				#print("Done with new tickers")
				if len(list_of_symbols)>0:
					
					getting_price_for_new_stickers()
				#k=input(scanner)
				
				start=time.time()
				#para_list=[]
				count=0
				for symbol, initial_price in scanner.items():
					count+=1
					actual_price,website_time = price_yahoo_parsing(ticker=symbol)
					if type(actual_price)!= float: 
						#print("Price: ",actual_price)
						#print("Symbol: ",symbol)
						continue
						
					price_dif = actual_price-initial_price
					news="" if symbol not in ticker_news else ticker_news[symbol]
					if symbol not in ticker_news:
						print(symbol)
						k=input()
					active_scan[symbol]=price_dif
					#for symbol_name, prive_value in active_scan.items():
					if price_dif >= 0.05:
						if -timer[symbol]+(int(time.strftime("%d"))*24)+(int(time.strftime("%H"))) == 0: statut="[NEW]" 			
						else: statut=""
						volume_=get_info(ticker=symbol,info="Volume",display=False)
						message = "Stock Name: "+symbol+'\n'+"Now: "+str(actual_price)+'\n'+"Opening: "+str(initial_price)+'\n'+"Dif: "+str(price_dif)+'\n'+'\n'+"Time: "+time.strftime("%m/%d/%Y ---- %H:%M:%S")+"\t"+time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))+'\n'+'Volume =%s'%volume_+'\n'+news+'\n'
						#validation = send_email("alex.don257@gmail.com","thebest001","alex.don257@gmail.com","####"+statut+" ["+symbol+"] at ",str(actual_price)+statut+message)
						#Process(target=send_email,args=("alex.don257@gmail.com","thebest001","alex.don257@gmail.com","####"+statut+" ["+symbol+"] at ",str(actual_price)+statut+message)).start()
						scanner[symbol]= actual_price
						#print("Timer:",-timer[symbol]+(int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))         
						#timer__=-timer[symbol]+(int(time.strftime("%d"))*24)+(int(time.strftime("%H")))
						print("[",count,"/",len(set(scanner)),"] ",symbol," [ACTIF]-> ",str(actual_price).zfill(5),"<-Act Init->",initial_price,"\t","{0:.5f}".format(price_dif),"V=",volume_, " "+time.strftime("---%H:%M:%S "))
					#else: print("[",count,"/",len(scanner), "] ",symbol,"\t",str(actual_price).zfill(5),"<-Act Init->",initial_price,"\t","{0:.5f}".format(price_dif), " "+time.strftime("---%H:%M:%S "))#,symbol_name,"\t",prive_value)

						#print("[",len(active_scan),"] ",symbol,"\t",price_dif)
					
					#Process(target=send_mysql,args=(symbol,actual_price,news)).start()
					#para_list.append([symbol,actual_price,news])
					output_to_file=symbol+" "+str(actual_price)+" "+website_time+" "+str(news)+"\n"
					nbr_of_stock_to_be_sent_to_db.write(output_to_file)
					
					#send_mysql(ticker=symbol,price=actual_price,news=news)
					end=time.time()
				sleeping_time=45 
				
				nbr_of_stock_to_be_sent_to_db.write("Done writting in file")
				nbr_of_stock_to_be_sent_to_db.close()
				if int(time.strftime("%H")) in [20,21,22,23,24,0,1,2,3,4,5,6,7]:
						sleeping_time=3600
				#print("Sleeping for -> ",sleeping_time-(end-start))
				
				end=time.time()
				print("Sleeping for -> ",sleeping_time-(end-start))
				sleep_time=sleeping_time-(end-start)
				time.sleep(sleep_time if sleep_time>=0 else 0)
				#print("-"*50,len(para_list))
				#para_list=[]
				
				
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
		#except Exception as e:
			#print("Error -> ",e)
		#	time.sleep(30)
		
	

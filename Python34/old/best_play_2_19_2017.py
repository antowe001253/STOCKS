# THis is just for super Nova, no for dip buy
from yahoo_finance import Share
from googlefinance import getQuotes
import requests
import time
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
    print("===== Loading morning Stickers and Prices")
    symbols_and_prices_file=open("symbols_and_prices.txt","r")
    symbols_and_prices_text = symbols_and_prices_file.read()
    symbols_and_prices_file.close()
    scanner_from_file = symbols_and_prices_text.split("\n")
    #print(scanner_from_file)
    for each_item in scanner_from_file:
        if len(each_item)>0:
            timer[each_item.split(" ")[0]]= int((each_item.split(" ")[-1]).split(".")[-1])
            scanner[each_item.split(" ")[0]] = float(each_item.split(" ")[1])
            print(each_item)

#k=input(scanner)
        





def get_price_GOOGLE(ticker):
#for ticker in list_of_symbols:
	trade_price = ""
	try:
		trade_price = getQuotes(ticker)[0]["LastTradePrice"]
		#print(trade_price)
		return float(trade_price)	
	except: f=0
	#print (trade_price)
		
def get_price_YAHOO(ticker):
#for ticker in list_of_symbols:
	try:
		
		yahoo = Share(ticker)
		yahoo.refresh()
		price_finance = yahoo.get_price()
		#print("IN->",ticker)
		#print ("Open -> ",yahoo.get_open())
		#print ("Current Price -> ",yahoo.get_price())
		#print ("Ave Volume -> ",yahoo.get_avg_daily_volume())
		#print ("Volume -> ",yahoo.get_volume())
		#print ("Time -> ",yahoo.get_trade_datetime())
		#print(price_finance)
		return float(price_finance)
	except:
		#print(".",end="")
		f=1

   
def new_stikers_from_scanner_stock_APP():
	global list_of_symbols
	symbols_file=open("symbols.txt","r")
	symbols_text = symbols_file.read()
	symbols_file.close()
	
	symbols_text_split = symbols_text.split("\n")
	if 	(len(symbols_text_split)>0):
		for each_symbol in symbols_text_split:
			if len(each_symbol)>0 :
				exit = ""
				#print("before checking price")
				exit=get_price_GOOGLE(each_symbol)
				if type(exit) == float:
					#print("===== [New] Loading Stickers from scanner_stocks App -> ",)
					#print(type(exit))
					#print(each_symbol)
					#k=input("Ticket found")
					#print("Ticket found: ",each_symbol)
					list_of_symbols.append(each_symbol)
				else:
					f=10
					#print("Not Found",each_symbol)
					#print("No ticket founds")
				#print(each_symbol)
				#k=input(each_symbol)
	symbols_file=open("symbols.txt",'w').close()
def getting_price_for_new_stickers():
    global timer
    global list_of_symbols
    global scanner 
	
    for ticker in list_of_symbols:
        if ticker not in scanner:
            #print("===== Getting orices for all New Stickers", len(list_of_symbols))
            price = get_price_GOOGLE(ticker)
			
            #print(ticker,"-> ",price)
            if type(price) != float: continue
          
			
				#continue # Ticker no found
            if price <= 0 or price>16:                 			
                continue # Ticker no found

            #print("[ADDING... ]",ticker)
            scanner [ticker]=price
            symbols_and_prices_file=open("symbols_and_prices.txt","a") 
            symbols_and_prices_file.write(ticker+" "+str(price)+" "+time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))+'\n')
			
            #timer[ticker]=time.strftime("%m/%d/%Y ---- %H:%M:%S")
            timer[ticker]=((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))
			
			#symbols_and_prices_file.write(ticker+" "+str(price)+'\n')
            symbols_and_prices_file.close()
            print("====[SAVING... ]",ticker," ",price)
    list_of_symbols = [] # all that data is now in scanner
    #print(scanner)

morning_sticker_data()
while(1):
    
	#if (int(time.strftime("%H"))<16 and int(time.strftime("%H"))>9) or (int(time.strftime("%H"))==9 and int(time.strftime("%M"))>29):
	
		new_stikers_from_scanner_stock_APP()
		#print("Done with new tickers")
		if len(list_of_symbols)>0:
			
			getting_price_for_new_stickers()
		#k=input(scanner)
		
		
		for symbol, initial_price in scanner.items():
			
			actual_price = get_price_GOOGLE(symbol)
			if type(actual_price)!= float: 
			    #print("Price: ",actual_price)
			    #print("Symbol: ",symbol)
			    continue
				
			price_dif = actual_price-initial_price
			
			active_scan[symbol]=price_dif
			#for symbol_name, prive_value in active_scan.items():
			print("[",len(active_scan),"] ",symbol,"\t",actual_price,"<-Act Init->",initial_price,"\t","{0:.5f}".format(price_dif), " "+time.strftime("---%H:%M:%S "))#,symbol_name,"\t",prive_value)

				#print("[",len(active_scan),"] ",symbol,"\t",price_dif)
			
			if price_dif >= 0.05:
				if -timer[symbol]+(int(time.strftime("%d"))*24)+(int(time.strftime("%H"))) == 0: statut="[NEW]" 			
				else: statut=""
				message = "Stock Name: "+symbol+'\n'+"Now: "+str(actual_price)+'\n'+"Opening: "+str(initial_price)+'\n'+"Dif: "+str(price_dif)+'\n'+'\n'+"Time: "+time.strftime("%m/%d/%Y ---- %H:%M:%S")+"\t"+time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))+'\n'
				validation = send_email("alex.don257@gmail.com","thebest001","alex.don257@gmail.com","####"+statut+" ["+symbol+"] at ",str(actual_price)+statut+message)
				if validation ==1: scanner[symbol]= actual_price
				print("Timer:",-timer[symbol]+(int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))         
				print(statut,"===========",timer[symbol],[symbol]," This Stock Is ACTIF       now: ",time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H")))))
				
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
		
	

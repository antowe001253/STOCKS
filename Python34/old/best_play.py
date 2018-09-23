# THis is just for super Nova, no for dip buy
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
#f=open("symbols.txt","r")
#text_of_symbols = f.read()
#f.close()
#f=open("symbols.txt",w).close()
#list_of_symbols = text_of_symbols.split(" ")
scanner ={} 
list_of_symbols=[] # fom the app scanner_stocks
active_scan={} # stock which are actif
timer ={}

def morning_sticker_data():
    global scanner
    #print("===== Loading morning Stickers and Prices")
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
        




def get_price(ticker):
#for ticker in list_of_symbols:
    #g_page = requests.get("https://finance.yahoo.com/quote/"+ticker+"?p="+ticker)
    g_page = requests.get("http://finviz.com/quote.ashx?t="+ticker)
    detail_page=g_page.text
    count_script=detail_page.count("</script>")
                                #k=input(count_script)
    while(count_script>0):
        pos1=detail_page.find("<script")
        pos2=detail_page.find("</script>")
        detail_page=detail_page[:pos1]+detail_page[pos2+9:]
        count_script=detail_page.count("</script>")

    ##if detail_page.find("Symbols similar to")>=0 or detail_page.find("Try looking again!")>=0 :
    if detail_page.find("not found")>=0:
        symbol_no_found_file=open("symbols_no_found.txt","a")
        symbol_no_found_file.write(ticker+'\n')
        symbol_no_found_file.close()
        #k=input("The requested symbol was not found in our database")
        return 0
    else:
        #print("Found")
        detail_page_plit = detail_page.split("<span")
        #print(len(detail_page_plit))
        for nbr_span, span_text in enumerate(detail_page_plit):
            if len(detail_page_plit)>=nbr_span+3:
			    
                if detail_page.find("open")>=0: print(span_text)
                print("In > 3")
                #if detail_page_plit[nbr_span+1].find("quote-market-notice")>=0 and detail_page_plit[nbr_span+2].find(" EST.")>=0:
                if detail_page_plit[nbr_span+2].find(" EST. Market open.")>=0:
                    print("IN")
                    span_text = span_text[:span_text.rfind("</span>")]
                    #print(span_text)
                    span_text = span_text[span_text.rfind(">")+1:]
                    #k=input("The Current price is: ",span_text)
                    if len(span_text)<=0:
                        print(ticker," ====== NO PRICE FOUND =====")
                        return get_price(ticker)
                    return float(span_text)
        else:
        #    print(" === A F T E R   H O U R ===")#print("Found")
		    
            print("===== NO FOUND ====")
            print(ticker)
            if detail_page.count("N/A")>10: 
                print("Char Unavailable")
                return 0
								
            else: return(get_price(ticker))
			
        #    detail_page_plit = detail_page.split("<span")
            #print(len(detail_page_plit))
         #   for nbr_span, span_text in enumerate(detail_page_plit):
         #       if len(detail_page_plit)>=nbr_span+4:
						
                    #print("In the for loop")
                    #print(ticker)
                    #print("-"*50)
                    #print(span_text)
                    #if span_text.find("At close:")>=0: k=input(span_text)
                    #k=input(span_text)
                   #if detail_page_plit[nbr_span+2].find("At close:")>=0 and detail_page_plit[nbr_span+4].find("People also watch")>=0:
           #         if detail_page_plit[nbr_span+2].find("At close:")>=0 :
                        #print(span_text)
                        
                        
           #             span_text = span_text[:span_text.rfind("</span>")]
                        #print(span_text)
           #             span_text = span_text[span_text.rfind(">")+1:]
                       # k=input("The Current price is: ",span_text)
                        #print(span_text)
          #              if len(span_text)<=0:
                            #k=input(ticker," ====== NO PRICE FOUND =====")
           #                 return get_price(ticker)
            #            return float(span_text)
            #else: return get_price(ticker)
			 #print(ticker," === COULDN'T FIND THE ACTUAL PRICE ===")
				#k=input(ticker," === COULDN'T FIND THE ACTUAL PRICE ===")
				#return get_price(ticker) print("ok")
			  
				
			   
                
    #print("OUT OF CHECKING PRICE\n\n")
    
def new_stikers_from_scanner_stock_APP():
	global list_of_symbols
	symbols_file=open("symbols.txt","r")
	symbols_text = symbols_file.read()
	symbols_file.close()
	symbols_file=open("symbols.txt",'w').close()
	symbols_text_split = symbols_text.split("\n")
	if 	(len(symbols_text_split)>0):
		for each_symbol in symbols_text_split:
			if len(each_symbol)>0:
				#print("===== [New] Loading Stickers from scanner_stocks App")
				list_of_symbols.append(each_symbol)
				#print(each_symbol)
				#k=input(each_symbol)
            
def getting_price_for_new_stickers():
    global timer
    global list_of_symbols
    global scanner 
	
    for ticker in list_of_symbols:
        if ticker not in scanner:
            #print("===== Getting orices for all New Stickers", len(list_of_symbols))
            price = get_price(ticker)
			
            print(ticker,"-> ",price)

            if price == 0 or price>16:                 			
                continue # Ticker no found

            #print("[ADDING... ]",ticker)
            scanner [ticker]=price
            symbols_and_prices_file=open("symbols_and_prices.txt","a") 
            symbols_and_prices_file.write(ticker+" "+str(price)+" "+time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))+'\n')
			
            #timer[ticker]=time.strftime("%m/%d/%Y ---- %H:%M:%S")
            timer[ticker]=((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))
			
			#symbols_and_prices_file.write(ticker+" "+str(price)+'\n')
            symbols_and_prices_file.close()
            print("[SAVING... ]",ticker," ",price)
    list_of_symbols = [] # all that data is now in scanner
    #print(scanner)

morning_sticker_data()
while(1):
    
	#if (int(time.strftime("%H"))<16 and int(time.strftime("%H"))>9) or (int(time.strftime("%H"))==9 and int(time.strftime("%M"))>29):
	
		new_stikers_from_scanner_stock_APP()
		
		if len(list_of_symbols)>0:
			
			getting_price_for_new_stickers()
		#k=input(scanner)
		
		
		for symbol, initial_price in scanner.items():
			
			actual_price = get_price(symbol)
			#print(actual_price)
			price_dif = actual_price-initial_price
			
			active_scan[symbol]=price_dif
			#for symbol_name, prive_value in active_scan.items():
			#print("[",len(active_scan),"] ",symbol,"\t",price_dif)
			
			if price_dif >= 0.05:
				if timer[symbol]-(int(time.strftime("%d"))*24)-(int(time.strftime("%H"))) == 0: statut="[NEW]" 			
				else: statut=""
				message = "Stock Name: "+symbol+'\n'+"Now: "+str(actual_price)+'\n'+"Opening: "+str(initial_price)+'\n'+"Dif: "+str(price_dif)+'\n'+time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))+'\n'
				validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com","####"+statut+" ["+symbol+"] at "+str(actual_price)+statut,message)
				if validation ==1: scanner[symbol]= actual_price
				print(timer[symbol]-(int(time.strftime("%d"))*24)-(int(time.strftime("%H"))))         
				print(statut,"===========",timer[symbol],[symbol]," This Stock Is ACTIF       now: ",time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H")))))
		#print("-"*50)
		
		command_file = open("best_play_file_commands.txt",'r')
		key_command = command_file.read()
		if len(key_command)>0:
			print(key_command)
			if key_command.find("print")>=0:
				for symbol_name, prive_value in active_scan.items():
					print("[",len(scanner),"] "+str(symbol_name)+"  "+str(prive_value)+"  "+time.strftime("%b %d, %Y---%H:%M:%S "))#,symbol_name,"\t",prive_value)

			#k=input("-----------")
		
		print("[",len(scanner),"] "+time.strftime("%b %d, %Y---%H:%M:%S "))#,symbol_name,"\t",prive_value)
    
	#else:	
	     
		#import os 
		#os.system('cls')  # for Windows 
		#remaining_time=0
		#if int(time.strftime("%H")) >=16:
		    #remaining_time=int(25*60*60 )-((int(time.strftime("%H"))*60 + int(time.strftime("%M")))*60 + int(time.strftime("%S")))+ ((9*60)+30)*60
		#else: remaining_time = ((9*60)+30)*60 - ((int(time.strftime("%H"))*60 + int(time.strftime("%M")))*60 + int(time.strftime("%S")))
		#print(time.strftime("%H:%M:%S "))
		#print(remaining_time)
		
		
		#time.sleep(1)
		
	

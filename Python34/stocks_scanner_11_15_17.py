# check if a title can have more keys word and add that number to my email suject
# the program sent me a symble og FDA which is not supposed to be approved because it in company abbreavation
#you can use http://finance.yahoo.com/quote/assp to see if a symbol exits or not
#Create another program to track if this one is running, if not, send me an email and re run  this again.
# prioritize : before () or <a look for nasdaq or nyse
# SHARE = STOCK = OWNERSHIP = EQUITY 
import requests
import winsound
import time
import msvcrt
import re
#from pynput.keyboard import Key, Listener
stop_loop=1
# we import the Twilio client from the dependency we just installed
#from twilio.rest import TwilioRestClient

# the following line needs your Twilio Account SID and Auth Token
#client = TwilioRestClient("AC960f28d0893eab0257b89e0446aa1ae5", "6611e947499c2fb627a3e58bcdffd5ab")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number

def delete_script_content(detail_page):
        count_script=detail_page.count("</script>")
        #k=input(count_script)
        while(count_script>0):
                pos1=detail_page.find("<script")
                pos2=detail_page.find("</script>")
                detail_page=detail_page[:pos1]+detail_page[pos2+9:]
                count_script=detail_page.count("</script>")
        return detail_page


def write_in_file(nbr_emails,file_name,message):
	f=open("archives/"+file_name,"a")
	f.write(re.sub(r'[^\x20-\x7e]',"","""Size of the list appending "+"["+str(nbr_emails)+"] "+"[TIME] "+time.strftime("%b %d, %Y---%H:%M:%S ")+message""")+'\n')
	f.close()
	
def failed_email(message):
    #f=open("failled_email_send.txt",'w').close
    location = "errors/failled_email "+time.strftime("%b %d, %Y")+".txt"
    f=open(location,'a')
    f.write("[TIME] "+time.strftime("%b %d, %Y---%H:%M:%S ")+message+'\n')
    f.close()
    
def sendsms(message):
    client.messages.create(to="+12404245394", from_="+12407702195", 
                       body=message)


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


def newAlert(stockName):
     f_output = open('data/stocks_found.txt','a')
     f_output.write(stockName)
     f_output.close()
       
#def anyKey():
   # while(stop_loop):
       # print(stop_loop)
        
            #break
def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False

# Collect events until released

        

def deepSound():
    Freq = 2500 # Set Frequency To 2500 Hertz
    Dur = 1000 # Set Duration To 1000 ms == 1 second
    winsound.Beep(Freq,Dur)

def check_file_beeping():
    f_output = open('data/stocks_found.txt','r')
    contend = f_output.readlines()
    f_output.close()
                    
    if(contend):
        for line in contend:
            if line.find("-")<0:
                deepSound()
                print("====[ New Alert ]====\n",line)
                print("="*10)
    else:
        print("The file is empty")

    #k=input("Exiting readin file")



#with Listener(
#        on_press=on_press,
 #       on_release=on_release) as listener:
            
#            listener.join(deepSound())

            

list_of_stock = ["URRE","GSAT","CNAT","XGTI","ANY"]
stock_webpage = ["http://www.uraniumresources.com/investors/news-releases",
                 "http://www.globalstar.com/en/index.php?cid=7010",
                 "http://ir.conatuspharma.com/releases.cfm?view=all",
                 "http://www.xgtechnology.com/category/press-release",
                 "http://sphere3d.com/category/press-releases/",
                 ]

webpage_names = ["http://finance.yahoo.com/news/provider-businesswire/?bypass=true",
                 "http://finance.yahoo.com/news/provider-accesswire/?bypass=true",
                 "http://www.marketwired.com/news_room/all_news/?headlines-only=HLO",
                 "http://www.globenewswire.com/",
                "http://finance.yahoo.com/news/provider-prnewswire/?bypass=true"
     ]

key_words = [ "8*k",
                 "Acquir",
                 "Agreement",
                 "Amend",
                 "Amazon",
                 "Announc",
                 "Apple",
                 "approval",
                 "Assets",
                 "AVAILABLE at",
                 "Bankruptcy",
                 "Benefit",
                 "Billion",
                 "Buy",
                 "Cash",
                 "Collaborat",
                 "combin",
                 "Complet",
                 "Demonstrat",
                 "Earning",
                 "Fda",
                 "file",
                 "Google",
                 "Grow",
                 "initiat",
                 "J.P. Morgan",
                 "join",
                 "Launch",
                 "Merger",
                 "Million",
                 "Partner",
                 "PATENT",
                 "PHASE",
                 "POSITIVE",
                 "Present",
                 "Reports",
                 "Result",
                 "revenue",
                 "Sale",
                 "sec", 
                 "Sell",
              "sign",
                 "Significant",
                 "Trillion",
                 "WAIT LOSS",             
                 "world's leading",
                 "Yahoo",
                 "%"]
alert_key_word=[ "Acquir",
                 "Agreement",
                 "Amendment",
                 "Announc",
                 "approval"
                 "Assets",
                 "Available AT",
                 "Bankruptcy",
                 "Business Progress",
                 "Collaborat",
                 "Completion",
                 "ETD Assets",
                 "grant",
                 "Announce Global",
                 "Join",
                 "Merger",
                 "Million",
                 "Patent",
                 "Partner",
                 "pivotal",
                 "Phase",
                 "Reports",
                 "Result",
                 "revenue",
                 "Reverse Stock Split",
                 "sign",
                 "Top",
                 "Volatility",
                 "world's leading",
                
                ]
companies_abraviations=["AAFCA",
                        "AAHRPP",
                        "ABSSSI",
                        "ACEDS",
                        "ACA",
                        "AIM",
                        "APM",
                        "APV",
                        "ARS",
                        "ASSP",
                        "AURAK",
                        "BAC",
                        "BKL",
                        "BLA",
                        "BNSF",
                        "BVK",
                        "CASB",
			"CDP",
                        "CES",
                        "CFC",
                        "CKD",
                        "CPP",
                        "CPU",
                        "CRAC",
                        "CTI",
                        "DAS",
                        "DLSO",
                        "DME",
                        "EMA",
                        "ENW",
                        "ERP",
                        "ET",
                        "FDA"
                        "FEH",
                        "FPC",
                        "GDP",
                        "GE",
                        "GMP",
                        "HD",
                        "HDR",
                        "HOA",
			"HSN",
                        "IBD",
                        "ICH",
                        "IGA",
                        "IDRBT",
                        "IPC",
                        "IRD",
                        "ITP",
                        "KDS",
                        "LAC",
                        "LFB",
                        "LID",
                        "LIDT",
                        "LIMA",
                        "LTPAC",
                        "MAP",
                        "MNTN",
                        "MPI",
                        "MSIL"
                        "MSK",
                        "MWS",
                        "NAEP",
                        "NDA",
                        "NDT",
                        "NEIH",
                        "NICHD",
                        "NIH",
                        "NIO",
                        "NIR",
                        "NOAA",
                        "NPCI",
                        "NSWCDD",
                        "NVH",
                        "PFE",
                        "PMG",
                        "PNH",
                        "POC",
                        "POS",
                        "RIA",
                        "RVVC",
                        "SCCHN"
                        "SCLC",
                        "SMMC",
                        "SECTUR",
                        "SSA",
                        "SVB",
                        "TLC",
                        "TMBI",
                        "TMNA",
                        "TMR",
                        "TSP",
                        "VVA",
                        "VSCP",
                        "UBI"
                        "UDH",
                        "UHNW",
                        "USA",
                        "USS",
                        "UWF",
                        "XEKT",
                        "YMS",
                        ]


this_worad_and_alert_key_word = ["Reports",
                                  "Available AT",
                                  "Agreement",
                                  "--",
                                  "--"
                                  ]
#anyKey()
#print(time.strftime("%b %d, %Y"))# Jan 04, 2017
#k_input = input("---------")
title_bank = set()
#print("kjkj".isalpha())
#print(all([i.isupper() for i in "GJGUGFF"]))
#k=input("===============")
def write_in_symbol_file_to_best_play_app(ticker_and_url):# the app best_play read in to that file to get the symbol and see if there is a change in price
        symbol_file=open("data/symbols.txt","a")
        symbol_file.write(ticker_and_url+'\n')
        symbol_file.close()
        print("Saved in symbol.txt -> ",ticker_and_url)
        print(time.strftime("%b %d, %Y---%H:%M:%S "))
        print("-"*75)
not_sent={}              
while(1):
    #open("archives/"+"log"+time.strftime(" %m-%d-%Y")+".txt",'w').close()
    cheker = open("data/cheker.txt","w")
    cheker.write("Working")
    cheker.close()
    time.sleep(5)
    #print("Actualle size of the array -> ",len(title_bank))
    #print("Max size of the array ->  536,870,912")
   # check_file_beeping()

    for number_page, wesite in enumerate(webpage_names):
        try:
            #print(wesite)
            g_page = requests.get(wesite)
            if (g_page.status_code != 200):
                print("*********[ Page No FOUND:",wesite," ]*********")
                failed_email("*******[ E R R O R ]*******\n\n CODE !+ 200\n" + wesite)
                #k_input=input("Press to continue\n\n")
            else:
                #print("We are in -> ",wesite)
                g_txt = g_page.text
                g_txt_split = g_txt.split("href=")

                for g_txt_split_val in g_txt_split:
                    g_txt_split_val= "".join(g_txt_split_val)
                    #print("href separedted-> ",g_txt_split_val)
                    #k=input("href separedted->")
                    if ((wesite.find("yahoo")>=0 or wesite.find("globenewswire")>=0 )and(g_txt_split_val.find("hours")<0 and g_txt_split_val.find("hour")<0 and (g_txt_split_val.find("minutes ago")>=0 or g_txt_split_val.find("minute ago")>=0))) or (wesite.find("marketwired")>=0 and g_txt_split_val.find("hours")<0 and g_txt_split_val.find("minutes ago")<0 and g_txt_split_val.find(time.strftime("%b %d, %Y"))>=0):
                        if g_txt_split_val.find("html")<0: link_name = g_txt_split_val[g_txt_split_val.find('href="')+2:g_txt_split_val.find('.htm')+4]
                        else: link_name = g_txt_split_val[g_txt_split_val.find('href="')+2:g_txt_split_val.find('.html')+5]
                        title_name =  g_txt_split_val[g_txt_split_val.find('">')+2:g_txt_split_val.find("</a>")]
                        #print("href separedted-> ",g_txt_split_val)
                        #print("title name ->",title_name)
                        #print("Link name -> ",link_name)
                        #print("webside -> ",wesite)
                        write_in_file(len(title_bank),"log"+time.strftime(" %m-%d-%Y")+".txt","Title name: "+title_name+"  wesite: "+wesite+" link_name: "+link_name)
                        #k=input("href separedted->")
                        #print(link_name)
                       #print(link_name)
                        keywrodsFound= [key for key in key_words if title_name.lower().find(key.lower())>=0]
                        #print([ key for key in key_words if title_name.lower().find(key.lower())>=0])
                        print("Keywords find "+str(keywrodsFound) if len(keywrodsFound)>0 else "No keywords found" )
                        #k_input=input("==============================")
                        if title_name not in title_bank and len(keywrodsFound)>0:
                            #print("Link Name -->",link_name)
                            if len(link_name)<10:
                                    print("Error ************************8")
                                    #k_input=input("link_name====================================================")
                            if wesite.find("yahoo")>=0: whole_link_name = "http://finance.yahoo.com"+link_name
                            elif wesite.find("globenewswire")>=0: whole_link_name = "http://www.globenewswire.com"+link_name
                            elif wesite.find("marketwired")>=0: whole_link_name = "http://www.marketwired.com"+link_name
                            #print("main webpage name-> ",wesite)
                           # print("Whole link ->",whole_link_name)

                            detail_page = requests.get(whole_link_name)
                            if (detail_page.status_code != 200):
                                print("*********[ Page No FOUND:",whole_link_name," ]*********")
                                failed_email("*******[ E R R O R ]*******\n\n CODE !+ 200\n" + wesite )
                                #k_input=input("Press to continue\n\n")
                            else:
                                #print("Whole link-> ",whole_link_name)
                                detail_page = detail_page.text
                                #k_input=input("=========Detail Page=====================")
                                new_text=""
                                count_script=detail_page.count("</script>")
                                #k=input(count_script)
                                delete_script_content(detail_page)# call this function to delete all the htlmp with in the script content
                                    #k=input(count_script)
                                detail_page_split = detail_page.split("(")
                                for detail_page_split_val in detail_page_split:
                                    detail_page_split_val= "".join(detail_page_split_val)
                                    detail_page_split_val=detail_page_split_val.replace("TWTR","")

                                    stock_ticker=""
                                    if detail_page_split_val.find(")")>=0:
                                        stock_ticker= detail_page_split_val[:detail_page_split_val.find(")")]
                                        
                                        #print(time.strftime("%b %d, %Y---%H:%M:%S "))
                                       # k=input("================")
                                        
                                        
                                        if stock_ticker.find(':')>=0:#(NYEX:CNAT) or (<a href="">CNAT</a>)
                                            stock_ticker = stock_ticker[stock_ticker.rfind(":")+1:]#to void this issues:  (NYSE: VRX and TSX: VRX) 
                                            
                                            if (stock_ticker.find('<a href="')>=0 or stock_ticker.find('<a rel="')>=0) and stock_ticker.find('</a>')>=0:#(<a href="">CNAT</a>)
                                                stock_ticker = stock_ticker[:stock_ticker.rfind(">")]
                                                stock_ticker = stock_ticker[stock_ticker.find(">")+1:stock_ticker.rfind("<")]          
                                                if stock_ticker.isalpha() and len(stock_ticker)>1 and all([ i.isupper() for i in stock_ticker]):
                                                    #k=input(stock_ticker)
                                                    #print("stock_ticker-> ",stock_ticker)
                                                    #k=input("================")
                                                    #print("NYDE: <a href='CNAT")
                                                    globenewswire_iden = True
                                                    break
                                            elif stock_ticker.find('<a href="')<0 and stock_ticker.find('<a rel="')<0:#(CNAT)
                                                if stock_ticker.find("<")>=0: stock_ticker = stock_ticker[:stock_ticker.find("<")]
                                                if stock_ticker.isalpha() and len(stock_ticker)>1 and all([ i.isupper() for i in stock_ticker]):
                                                    #k=input(stock_ticker)
                                                    #print("NYDE:CNAT")
                                                    #print("stock_ticker-> ",stock_ticker)
                                                    #k=input("================")
                                                    globenewswire_iden = True
                                                    break
                                        elif stock_ticker.find(':')<0:#(CNAT) or (<a href="">CNAT</a>)
                                            
                                            if stock_ticker.find('<a href="')>=0 and stock_ticker.find('</a>')>=0:#(<a href="">CNAT</a>)
                                                #print(stock_ticker)
                                                stock_ticker = stock_ticker[:stock_ticker.rfind(">")]
                                                stock_ticker = stock_ticker[stock_ticker.find(">")+1:stock_ticker.rfind("<")]          
                                                #print(stock_ticker)
                                                #k=input("================")
                                                if stock_ticker.isalpha() and len(stock_ticker)>1 and all([ i.isupper() for i in stock_ticker]):
                                                    #print("<a href="">CNAT</a>")
                                                    #print("stock_ticker-> ",stock_ticker)
                                                    #k=input(stock_ticker)
                                                    #k=input("================")
                                                    globenewswire_iden = True
                                                    break
                                            elif stock_ticker.find('<a href="')<0:#(CNAT)
                                                if stock_ticker.isalpha() and len(stock_ticker)>1 and all([ i.isupper() for i in stock_ticker]):
                                                    #print("CNAT")
                                                    #print("Ticket at any time: ",stock_ticker)
                                                    #k=input(stock_ticker)
                                                    #k=input("================")
                                                    globenewswire_iden = True
                                                    break
                                        

                                    stock_ticker = ""
                                       # if (stock_ticker.find(':')>=0 and stock_ticker.find('<a href="')>=0) or (len(stock_ticker)>2 and not any([i.islower() for i in stock_ticker if not i.isdigit()])):
                                       #     print(": is there",stock_ticker.find(':')>=0,"\ncapitalized and not number->",not any([i.islower() for i in stock_ticker]))
                                      #      k=input(stock_ticker)
                                      #      globenewswire_iden = True
                                     #       break
                                else:
                                    globenewswire_iden=False
                                    stock_ticker=""
                                #print("ticker")
                                #print("found (")
                                #print(stock_ticker)
                                #k=input()
                                if stock_ticker == "BCA":
                                        k=input("BCA FOUND")
                                #print("length of title bank",len(title_bank))
                                if len(title_bank)>= 2000:
                                        title_bank=title_bank[100:]
                                #k=input("================================ticket identified")
                                if title_name.lower().find(" conference call ")<0 and title_name.lower().find(" date ")<0 and (detail_page.find('(<exchange')>=0 or globenewswire_iden) and(stock_ticker not in set(companies_abraviations)):
                                    
                                    #print(time.strftime("%b %d, %Y---%H:%M:%S "))
                                   # print('(<a -> ',detail_page.find('(<a')>=0,'\n(<exchange -> ',detail_page.find('(<exchange')>=0,'\n: <a href -> ',globenewswire_iden)
                                    if len(stock_ticker)<2:
                                        print("*"*25)
                                        print("Tricker: ",stock_ticker)
                                        print("The Triker is wrong")
                                       # k=input("The Triker is wrong")
                                        
                                    if title_name.lower().find("available at")>=0:
                                       #print("="*25)
                                       #print("Ticker -> ",stock_ticker)
                                       write_in_symbol_file_to_best_play_app(stock_ticker+" "+whole_link_name)
									   
                                       #validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com","$$$$["+stock_ticker+"]"+title_name,wesite+'\n\n\n'+whole_link_name)
                           
                                    elif title_name.lower().find(" agreement ")>=0 or title_name.lower().find(" acquire ")>=0 or title_name.lower().find(" approval ")>=0 or title_name.lower().find(" phase ")>=0 or detail_page.lower().find(" agreement with blue cross blue shield")>=0:
                                       #print("="*25)
                                       #print("Ticker -> ",stock_ticker)
                                       write_in_symbol_file_to_best_play_app(stock_ticker+" "+whole_link_name)					  
                                       #validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com","$$$["+stock_ticker+"]"+title_name,wesite+'\n\n\n'+whole_link_name)
                                    elif detail_page.lower().find("per share")>=0:
                                       #print("="*25)
                                       #print("Ticker -> ",stock_ticker)
                                       write_in_symbol_file_to_best_play_app(stock_ticker+" "+whole_link_name)     
                                       #validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com","$["+stock_ticker+"]"+title_name,wesite+'\n\n\n'+whole_link_name)
                                    
                                    elif len([ alert_key for alert_key in alert_key_word if title_name.lower().find(alert_key.lower())>=0])>0:
                                       #print("="*50)
                                       #print("Ticker -> ",stock_ticker)
                                       write_in_symbol_file_to_best_play_app(stock_ticker+" "+whole_link_name)     
                                       #validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com","===["+stock_ticker+"]"+title_name,wesite+'\n\n\n'+whole_link_name)
                                    #sendsms(title_name+'\n\n\n'+wesite+'\n\n\n'+whole_link_name)
                                    #k_input=input("Press to continue\n\n")
                                    else:
                                        write_in_symbol_file_to_best_play_app(stock_ticker+" "+whole_link_name)
                                        validation=0
                                        for tick,val in not_sent.items():
                                                if tick==stock_ticker:
                                                        break
                                        else: not_sent[stock_ticker]=0
                                        
                                        not_sent[stock_ticker]=not_sent[stock_ticker]+1
                                        if not_sent[stock_ticker] >= 5:
                                                validation = 1
                                                failed_email(" Not Send | Ticker: ["+stock_ticker+"] "+"Title: "+title_name+"| Source: "+wesite+'| Link:'+whole_link_name)
                                                del(not_sent[stock_ticker])

                                        
                                        #k=input("IN 5")
                                        #validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com","***["+stock_ticker+"]"+title_name,wesite+'\n\n\n'+whole_link_name)
                                    #if validation == 1:
                                        #title_bank.add(title_name)
                                #else:
                                #sendsms(title_name+'\n\n\n'+wesite+'\n\n\n'+whole_link_name)
                                    #validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com",title_name,wesite+'\n\n\n'+whole_link_name)
                                    #if validation == 1:
                                        #title_bank.add(title_name)
                            #else: failed_email("*******[ E R R O R ]*******\n\n THIS MESSAGE FAILLED/n"+title_name+'\n\n\n'+wesite+'\n\n\n'+whole_link_name)
        except :
            print("*"*10," [DID NOT LOAD THE PAGE] ","*"*10)
            #k=input("Expect called")
                       
                    
                    
k_input=input("Next stoc --->")  
            

print(time.strftime("%d/%b/%Y"))
    

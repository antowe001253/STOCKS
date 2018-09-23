import requests
import winsound
import time
import msvcrt
from pynput.keyboard import Key, Listener
stop_loop=1
# we import the Twilio client from the dependency we just installed
from twilio.rest import TwilioRestClient

# the following line needs your Twilio Account SID and Auth Token
client = TwilioRestClient("AC960f28d0893eab0257b89e0446aa1ae5", "6611e947499c2fb627a3e58bcdffd5ab")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number

def failed_email(message):
    #f=open("failled_email_send.txt",'w').close
    f=open("failled_email_send.txt",'a')
    f.write(message)
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
     f_output = open('stocks_found.txt','a')
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
    f_output = open('stocks_found.txt','r')
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

key_words = ["Agreement",
                 "Complet",
                 "Sale",
                 "Buy",
                 "Sell",
                 "Cash",
                 "Million",
                 "Billion",
                 "Earning",
                 "approval",
                 "Announc",
                 "Trillion",
                 "Collaborat",
                 "Grow",
                 "Partner",
                 "Acquir",
                 "Launch",
                 "Amazon",
                 "Google",
                 "Apple",
                 "Yahoo",
                 "Fda",
                 "file",
                 "Benefit",
                 "Demonstrat",
                 "Significant",
                 "initiat",
                 "8*k",
                 "sec",
                 "Amend",
                 "AVAILABLE",
                 "WAIT LOSS",
                 "AGREEMENT"
                 "PHASE"
                 "PATENT",
                 "POSITIVE",
                 "%"]
companies_abraviations=["NIH",
                        "NICHD",
                        "LID",
                        "MSK",
                        "NSWCDD",
                        "CRAC",
                        "LFB",
                        "LIDT",
                        "TMR",
                        "CASB",
                        "PNH",
                        "RVVC",
                        "BLA",
                        "NDT",
                        "NVH",
                        "ENW",
                        "DLSO",
                        "ERP",
                        "ARS",
                        "FDA"
                        ]

alert_key_word=["Million",
                "Announces",
                "Merger",
                "Partner",
                "Collaborat",
                "Acquir",
                "Phase",
                "Join",
                "Agreement",
                "Bankruptcy",
                "Volatility",
                "Reverse Stock Split",
                "ETD Assets",
                "approval",
				"Reports",
				"Available AT",
				"",
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
print(all([i.isupper() for i in "GJGUGFF"]))
k=input("===============")
while(1):
    print("Actualle size of the array -> ",len(title_bank))
    print("Max size of the array ->  536,870,912")
    time.sleep(5)
   # check_file_beeping()

    for number_page, wesite in enumerate(webpage_names):
        try:
            g_page = requests.get(wesite)
            if (g_page.status_code != 200):
                print("*********[ Page No FOUND:",wesite," ]*********")
                failed_email("*******[ E R R O R ]*******\n\n CODE !+ 200\n" + wesite+"\n" )
                #k_input=input("Press to continue\n\n")
            else:
                print("We are in -> ",wesite)
                g_txt = g_page.text
                g_txt_split = g_txt.split("href=")

                for g_txt_split_val in g_txt_split:
                    g_txt_split_val= "".join(g_txt_split_val)

                    if (g_txt_split_val.find("hours")<0 and g_txt_split_val.find("hour")<0 and (g_txt_split_val.find("minutes ago")>=0 or g_txt_split_val.find("minute ago")>=0))or (g_txt_split_val.find("hours")<0 and g_txt_split_val.find("minutes ago")<0 and g_txt_split_val.find(time.strftime("%b %d, %Y"))>=0):
                        if g_txt_split_val.find("html")<0: link_name = g_txt_split_val[g_txt_split_val.find('href="')+2:g_txt_split_val.find('.htm')+4]
                        else: link_name = g_txt_split_val[g_txt_split_val.find('href="')+2:g_txt_split_val.find('.html')+5]
                        title_name =  g_txt_split_val[g_txt_split_val.find('">')+2:g_txt_split_val.find("</a>")]
                        print(title_name)
                        #print(link_name)
                       #print(link_name)
                        print([ key for key in key_words if title_name.lower().find(key.lower())>=0])
                        #k_input=input("==============================")
                        if title_name not in title_bank and len([ key for key in key_words if title_name.lower().find(key.lower())>=0])>0:
                            
                            if wesite.find("yahoo")>=0: whole_link_name = "http://finance.yahoo.com"+link_name
                            elif wesite.find("globenewswire")>=0: whole_link_name = "http://www.globenewswire.com"+link_name
                            elif wesite.find("marketwired")>=0: whole_link_name = "http://www.marketwired.com"+link_name
                            #print("main webpage name-> ",wesite)
                            print("Whole link ->",whole_link_name)

                            detail_page = requests.get(whole_link_name)
                            if (detail_page.status_code != 200):
                                print("*********[ Page No FOUND:",whole_link_name," ]*********")
                                failed_email("*******[ E R R O R ]*******\n\n CODE !+ 200\n" + wesite+"\n" )
                                #k_input=input("Press to continue\n\n")
                            else:
                                print("We are in -> ",whole_link_name)
                                detail_page = detail_page.text
                                #k_input=input("=========Detail Page=====================")
                                new_text=""
                                count_script=detail_page.count("</script>")
                                #k=input(count_script)
                                while(count_script>0):
                                    
                                    pos1=detail_page.find("<script")
                                    pos2=detail_page.find("</script>")
                                    detail_page=detail_page[:pos1]+detail_page[pos2+9:]
                                    count_script=detail_page.count("</script>")
                                    #k=input(count_script)
                                detail_page_split = detail_page.split("(")
                                for detail_page_split_val in detail_page_split:
                                    detail_page_split_val= "".join(detail_page_split_val)
                                    detail_page_split_val.replace("TWTR","")
                                    stock_ticker=""
                                    if detail_page_split_val.find(")")>=0:
                                        #print("found (")
                                        #k=input("================")
                                        stock_ticker= detail_page_split_val[:detail_page_split_val.find(")")]
                                        if stock_ticker.find(':')<0:#(CNAT) or (<a href="">CNAT</a>)
                                            if stock_ticker.find('<a href="')<0:#(CNAT)
                                                if stock_ticker.isalpha() and len(stock_ticker)>2 and all([ i.isupper() for i in stock_ticker]):
                                                    print("CNAT")
                                                    #k=input(stock_ticker)
                                                    globenewswire_iden = True
                                                    break
                                            elif stock_ticker.find('<a href="')>=0 and stock_ticker.find('</a>')>=0:#(<a href="">CNAT</a>)
                                                #print(stock_ticker)
                                                stock_ticker = stock_ticker[:stock_ticker.rfind(">")]
                                                stock_ticker = stock_ticker[stock_ticker.find(">")+1:stock_ticker.rfind("<")]          
                                                #print(stock_ticker)
                                                #k=input("================")
                                                if stock_ticker.isalpha() and len(stock_ticker)>2 and all([ i.isupper() for i in stock_ticker]):
                                                    print("<a href="">CNAT</a>")
                                                    #k=input(stock_ticker)
                                                    globenewswire_iden = True
                                                    break
                                        elif stock_ticker.find(':')>=0:#(NYEX:CNAT) or (<a href="">CNAT</a>)
                                            stock_ticker = stock_ticker[stock_ticker.find(":")+1:]
                                            if stock_ticker.find('<a href="')<0 and stock_ticker.find('<a rel="')<0:#(CNAT)
                                                stock_ticker = stock_ticker[stock_ticker.find(":")+1:]
                                                if stock_ticker.isalpha() and len(stock_ticker)>2 and all([ i.isupper() for i in stock_ticker]):
                                                    #k=input(stock_ticker)
                                                    print("NYDE:CNAT")
                                                    globenewswire_iden = True
                                                    break
                                            elif (stock_ticker.find('<a href="')>=0 or stock_ticker.find('<a rel="')>=0) and stock_ticker.find('</a>')>=0:#(<a href="">CNAT</a>)
                                                stock_ticker = stock_ticker[:stock_ticker.rfind(">")]
                                                stock_ticker = stock_ticker[stock_ticker.find(">")+1:stock_ticker.rfind("<")]          
                                                if stock_ticker.isalpha() and len(stock_ticker)>2 and all([ i.isupper() for i in stock_ticker]):
                                                    #k=input(stock_ticker)
                                                    print("NYDE: <a href='CNAT")
                                                    globenewswire_iden = True
                                                    break

                                                  
                                       # if (stock_ticker.find(':')>=0 and stock_ticker.find('<a href="')>=0) or (len(stock_ticker)>2 and not any([i.islower() for i in stock_ticker if not i.isdigit()])):
                                       #     print(": is there",stock_ticker.find(':')>=0,"\ncapitalized and not number->",not any([i.islower() for i in stock_ticker]))
                                      #      k=input(stock_ticker)
                                      #      globenewswire_iden = True
                                     #       break
                                else:
                                    globenewswire_iden=False
                                    stock_ticker=""
                                if len(title_bank)>= 268435456:
                                        title_bank=title_bank[134217728:]
                                if (detail_page.find('(<exchange')>=0 or globenewswire_iden) and(stock_ticker not in set(companies_abraviations)):
								
                                    print('(<a -> ',detail_page.find('(<a')>=0,'\n(<exchange -> ',detail_page.find('(<exchange')>=0,'\n: <a href -> ',globenewswire_iden)
                                    if len(stock_ticker)<3:
                                        print(globenewswire_iden)
                                        print("Tricker: ",stock_ticker)
                                        k=input("The Triker is wrong")
                                #sendsms(title_name+'\n\n\n'+wesite+'\n\n\n'+whole_link_name)
                                    #k_input=input("Press to continue\n\n")
                                        if(len[stock_ticker]>=0)
                                    #if (len[ alert_key for alert_key in alert_key_word if title_name.lower().find(alert_key.lower())>=0])>0:
				        validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com","===["+stock_ticker+"]"+title_name,wesite+'\n\n\n'+whole_link_name)

                                    else:
				        validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com","***["+stock_ticker+"]"+title_name,wesite+'\n\n\n'+whole_link_name)
                                    if validation == 1:
                                        title_bank.add(title_name)
                                #else:
                                #sendsms(title_name+'\n\n\n'+wesite+'\n\n\n'+whole_link_name)
                                   # validation = send_email("alex.don257@gmail.com","thebest001","alex.don255@gmail.com",title_name,wesite+'\n\n\n'+whole_link_name)
                                    #if validation == 1:
                                        #title_bank.add(title_name)
                            #else: failed_email("*******[ E R R O R ]*******\n\n THIS MESSAGE FAILLED/n"+title_name+'\n\n\n'+wesite+'\n\n\n'+whole_link_name)
        except:
            print("*"*10," [DID NOT LOAD THE PAGE] ","*"*10)
                       
                    #k_input=input("[YAHOO ]Press to continue\n\n")
##    for  symbol,stock_web in enumerate(stock_webpage):
##        
##        page = requests.get(stock_web)
##        if (page.status_code != 200):
##            print("*********[ Page No FOUND:",stock_web," ]*********")
##            #k_input=input("Press to continue\n\n")
##        else:
##            txt = page.text
##            #print(txt)
##            txt.replace("<span"," ")
##            pos = txt.count("date")
##            #print(pos)
##            #print(txt[pos:pos+500])
##
##            day=time.strftime("%a")
##            month=time.strftime("%b")
##            year=time.strftime("%Y")
##            
##            daynbr=time.strftime("%d")
##            monthnbr=time.strftime("%m")
##            yearnbr=time.strftime("%Y")
##
##            split_textt = txt.split("<")
##            print("-"*50)
##            print("Current date:",time.strftime("%d/%m/%Y"),"/tLooking in this site->\n","[CHECK 1]->",stock_web)
##            
##            for split_text in split_textt:
##                split_text= "".join(split_text)
##                #print(split_text)
##                #print(split_text)
##                #if (split_text.find(day)>=0 and split_text.find(month)>=0 and split_text.find(year)>=0):
##                 #   print("-----------1-------------")
##                 #   print (time.strftime("%a/%b/%Y"))
##                  #  print(stock_web)
##                 #   k_input=input("Press to continue")
##
##                if (split_text.find(daynbr)>=0
##                    and split_text.find(month)>=0
##                    and split_text.find(yearnbr)>=0
##                    and ( split_text.find(">")<=split_text.find(daynbr))
##                    and ( split_text.find(">")<=split_text.find(month))
##                    and ( split_text.find(">")<=split_text.find(yearnbr))):
##                    #print("="*50)
##                    deepSound()
##                    print("-----------1-------------")
##                    print(stock_web)
##                    #print(time.strftime("%d/%b/%Y"))
##                    print(split_text)
##                    newAlert(list_of_stock[symbol])
##                    print("="*50)
##                    #k_input=input("Press to continue")
##          
##        url_seekingalpha="http://seekingalpha.com/symbol/"+list_of_stock[symbol]
##        page2 = requests.get(url_seekingalpha)
##        if (page2.status_code != 200):
##            print("*********[ Page No FOUND:",url_seekingalpha," ]*********")
##            print(page2.status_code)
##            #k_input=input("Press anything to continue\n")
##        else:
##            txt2 = page2.text 
##            print("[CHECK 2]->",url_seekingalpha)
##            split_textt2 = txt2.split("<")
##            
##            for split_text2 in split_textt2:
##                split_text2= "".join(split_text2)
##
##                if(split_text2.find("Today")>=0 and (split_text2.find("PM")>=0 or split_text2.find("AM")>=0) ):
##                    #print("="*50)
##                    deepSound()
##                    print("-----------2-------------")
##                   # print(list_of_stock[symbol])
##                   # print("Today")
##                    print(split_text2)
##                    newAlert(list_of_stock[symbol])
##                    print("="*50)
##                    #k_input=input("Press to continue")

       # page3 = requests.get(global_news_wire[symbol])
          

          
       # if (page3.status_code != 200):
           # print("*********[ Page No FOUND:",global_news_wire[symbol]," ]*********")
            #k_input=input("Press to continue\n\n")
        #else:
           # txt3 = page3.text 
           # print("[CHECK 3]->",global_news_wire[symbol])
           # split_textt3 = txt3.split("<")
            
           # for split_text3 in split_textt3:
                #split_text3= "".join(split_text3)

                #if(split_text3.find("ago")>=0 and (split_text3.find("hours")>=0 or split_text3.find("minutes")>=0) ):
                   # print("="*50)
                   # deepSound()
                   # print("-----------3-------------")
                   # print(list_of_stock[symbol])
                   # print("hours")
                   # print(split_text3)
                   # newAlert(list_of_stock[symbol])
                   # print("="*50)
                    #k_input=input("Press to continue")
                    
k_input=input("Next stoc --->")  
            

print(time.strftime("%d/%b/%Y"))
    

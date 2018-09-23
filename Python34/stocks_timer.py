import time
from datetime import date
import calendar
timer = {}
scanner_from_file=[]
count_recuring = 0


def actual_lines_in_file():
    key_begin="start^~^"
    key_end="done^~^"
    symbols_and_prices_file=open("data/symbols_and_prices.txt","r")
    symbols_and_prices_text = symbols_and_prices_file.read()
    find_key_begin=symbols_and_prices_text.find(key_begin)
    find_key_end=symbols_and_prices_text.find(key_end)
    if find_key_begin>=0: symbols_and_prices_text=symbols_and_prices_text.replace(key_begin,"")
    if find_key_end>=0: symbols_and_prices_text=symbols_and_prices_text.replace(key_end,"")
    symbols_and_prices_file.close()
    scanner_from_file = symbols_and_prices_text.split("\n")
    return scanner_from_file,find_key_begin,find_key_end

    return 
def morning_sticker_data():
    
   
   
    global timer 

    print("===== Loading morning Stickers and Prices")
    #symbols_and_prices_file=open("data/symbols_and_prices.txt","r")
    #symbols_and_prices_text = symbols_and_prices_file.read()
    #find_key_begin=symbols_and_prices_text.find(key_begin)
    #find_key_end=symbols_and_prices_text.find(key_end)
    #if find_key_begin>=0: symbols_and_prices_text=symbols_and_prices_text.replace(key_begin,"")
    #if find_key_end>=0: symbols_and_prices_text=symbols_and_prices_text.replace(key_end,"")
    #symbols_and_prices_file.close()
    scanner_from_file,find_key_begin,find_key_end = actual_lines_in_file()
    #print(scanner_from_file)
    count1=0
    #print(symbols_and_prices_text.find(key_end))
    #print(len(scanner_from_file))
    #print(scanner_from_file[24])
    for i in range(len(scanner_from_file)):
        if len(scanner_from_file[i])>0:
            #print(i)
            try:
                timer[scanner_from_file[i].split(" ")[0]] = scanner_from_file[i].split(" ")[2]# loading all info in symbols_and_prices.txt
            except:# fix this error .512 in symbols_and_prices.txt. the date part is missing from .512
                print(scanner_from_file[i])
                continue  
                #timer[scanner_from_file[i].split(" ")[0]] = scanner_from_file[i].split(" ")[2]
            #print(each_item)
            count1+=1
    print(count1)
    
    
    return (find_key_begin,find_key_end)
    #k=input()

display=False
while(1):
    
    my_date = date.today()
    day=calendar.day_name[my_date.weekday()]
    #hold_dates=['Sunday','Monday']
    hold_dates=['Sunday']
    if day in hold_dates :
        print("Today's date -> ",day)
        print("Sleeping for 3600 seonds")
        time.sleep(3600)
    else:
    #timer = {}
        count=0
        find_key_begin,find_key_end=morning_sticker_data()
        if (find_key_begin<0 or find_key_end>0):
                    	
                    print("[New run ]-----------------------------------------------------------------------------------------------------------------")
                    for ticker, date_ in timer.items(): # timer has all info in symbols_and_prices.txt
                            print(date_)
                            try:
                                time_ = int(date_.split(".")[-1])
                            
                                yy_mm = int(int(date_.split(".")[-0]))
                            except:
                                print("*"*50)
                                print("Error")
                                print("This shsould be a daate-> ",date_)
                                continue
                            
                            time_elpased=int(time.strftime("%d"))*24+int(time.strftime("%H")) - time_
                            if display:
                                    print("Ticker initial time: ",time_)
                                    print("Ticker initial Date: ",yy_mm)
                                    print("Time Now: ",int(time.strftime("%d"))*24+int(time.strftime("%H")))
                                    print("-----------[Ticker]->", ticker ,"[",time_elpased,"]")
                                    print("time_elpased: ",time_elpased)
                                    print(time.strftime("%Y%m"),yy_mm,time_elpased)
                            # STLY 0.82 301801.561 http://www.globenewswire.com/news-release/2018/01/23/1299241/0/en/Stanley-Furniture-Announces-Preliminary-Fourth-Quarter-Sales-and-Net-Loss-Amendment-to-Agreement-to-Sell-

#Substantially-All-of-Its-Assets.html   
                            #k=input()
                            if yy_mm>int(time.strftime("%Y%m")) or abs(time_elpased)>24:
                                    print("Deleting ... [",ticker,"]")
                                    
                                    scanner_from_file = actual_lines_in_file()[0]
                                   
                                    symbols_and_prices_file=open(r"C:\Users\Alex.Ntowe\Documents\Project\Python\STOCKS\Python34\data\symbols_and_prices.txt",'w').close()
                                    #print("---------------------------------Write and close ...")

                                    
                                    print("scanner_from_file -> ",len(scanner_from_file)) 
                                    for line in scanner_from_file:
                                        
                                               
                                            if line.split(" ")[0]== ticker:
                                                    print("Deleted ...", ticker)
                                                    print("dadte",date_)
                                                    print("Ticker initial time: ",time_)
                                                    print("Now: ",int(time.strftime("%d"))*24+int(time.strftime("%H")))
                                                    print("Ticker initial Date: ",yy_mm)
                                                    print("Diff: ",time_elpased)
                                                    print("Total: ",len(scanner_from_file)-1)
                                                    print(""*25+"D E L E T I N G ..."+"*"*25+"["+str(count)+"]")
                                                    count+=1
                                                    #del timer[ticker]
                                                    
                                                    #k=input("Press to continue")
                                                    #continue
                                            elif len(line)>5:
                                                    #k=input(ticker)
                                                    #print("----------------------------------Saving ...",line )
                                                    #k=input()
                                                    symbols_and_prices_file=open("data/symbols_and_prices.txt","a")
                                                    symbols_and_prices_file.write(line.replace("\n","").replace("\r","")+"\n")
                                                    symbols_and_prices_file.close()
                    
                    count_recuring = count_recuring + 1
                    print("-"*15,count_recuring,"-"*15,count,"/",len(timer)," deleted")
                    #k=input()
                    print("Total: ",len(actual_lines_in_file()[0])-1)
                    print(time.strftime("%H:%M:%S"))
                    time.sleep(60)

print("-----------")
print(time.strftime("%H:%M:%S %d %m"))
print(time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H")))))
print((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))


import sys, os
import requests
sys.path.append('../Python34/')
from  connect_mysql import *
from get_ticker_info import *

def best_match(parameter,ticker,info,time,data):
        print("``"*25,"checking %s"%parameter)
        if parameter=="opening": index=3
        elif parameter=="price": index=4
        elif parameter=="volume": index=5
        else: raise "Wrong Parameter %s"%parameter
        found_time=0
        time_diff=0
        
        result=("ivld",-1)
        for record in data:
            record_info=record[index]#volume, price, or opening
            record_time=record[1]
            if record[2]==ticker and record_time!=time and record_info>0:
                #print(record_time,"\t",time)
                #print(record_info,"\t",info)
                #print("Diff ->",abs(record_time-time))
                #print("Old Diff ->",time_diff)
                #print("-"*10)
                if time_diff==0:
                    time_diff=abs(record_time-time)
                    #k=input()
                if abs(record_time-time)<=time_diff:# how much time_diff to use its volume 1h? 30 mins? 15 min? 5 mins diff
                    found_time=record_time
                    result=("vld",record_info)
                    #print("%s= "%parameter,result)
                    #k=input()
                #if found_volume
                #found_volume=record_volume if
        print("Time found -> ",found_time)
        #print(abs(found_time-time),type(abs(found_time-time)),datetime.timedelta(0,300,0),type(datetime.timedelta(0,300,0)))
        if(isinstance(found_time,datetime.timedelta)):
                
                if abs(found_time-time)>datetime.timedelta(0,300,0):#0:12:00  -> 300 seconds
                        if int(str(found_time).split(":")[0]) not in list(range(8,19)):# if the time is not between 19h and 7am
                                print(time,"\t",found_time)
                                print("%s -> "%parameter,result,"\t  ticker -> ",ticker)
                                #k=input("Exiting CHeking %s for "%parameter)
                                #if k=="go":result=("ivld",-1)
                        else:
                                print(time,"\t",found_time)
                                print("%s -> "%parameter,result,"\t  ticker -> ",ticker)
                                print("TIME is During DAY")
                                #k=input("Exiting CHeking %s for "%parameter)
                                #if k=="go":
                                result=("ivld",-1)
                                
                                
        return result

    
def check_time(time="",result_uploaded_date=("","")):
    if not isinstance(time,datetime.timedelta):
        print("**"*25,"check_time")
        print("isinstance(time,datetime.timedelta)->  ",type(time),"datetime.timedelta")
        result=("ivld",time)
    elif "vld" in result_uploaded_date and int(str(result_uploaded_date[-1]).split(":")[0].split()[-1])!=int(str(time).split(":")[0]) and int(str(time).split(":")[1]) not in range(49,60):
        print("**"*25,"check_time")
        print(int(str(result_uploaded_date[-1]).split(":")[0].split()[-1]),int(str(time).split(":")[0]))
        print(time,"\t",result_uploaded_date)
        result=("ivld",time)
        #k=input()
        #if k=="go": result=("vld",time)
    else: result=("vld",time)
    return result

def check_opening(ticker,opening,time,data):
    if opening<0:
        result= best_match("opening",ticker,opening,time,data)
    else:
        result=("vld",opening)
    return result

def check_price(ticker,price,time,data):
    if price<0:
        result= best_match("price",ticker,price,time,data)
    else:
        result=("vld",price)
    return result

def check_volume(ticker,volume,time,data):
    #print("``"*25,"checking V O L U M E")
    #found_time=0
    #time_diff=0
    if volume<0:
        result= best_match("volume",ticker,volume,time,data)
    else: result=("vld",volume)
    return result

def check_P_E(ticker,P_E):
    if P_E <0:
        result=float(get_info(ticker=ticker,info="PE Ratio",timeout=10))
        if result<0:
            #print("**"*25,"check_P_E")
            result=("vld",result)# not that important, always valid
        else: result=("vld",result)
    else: result=("vld",P_E)
    return result

def check_beta(ticker,beta):
    if beta <=-5 or beta==0 or beta==-1:
        result=float(get_info(ticker=ticker,info="Beta",timeout=10))
        if result<=-5:
            #print("**"*25,"check_beta")
            result=("vld",result)# not that important, always valid
        else: result=("vld",result)
    else: result=("vld",beta)
    return result

def check_dividents(ticker,dividents):
    dividents=float(dividents)
    if dividents <0:
        result=get_info(ticker=ticker,info="Forward Dividend",timeout=10)
        if str(result).find("%")>=0:
            result=float(result.replace("%",""))
        #print(result)
        if result<0:
            #print("**"*25,"check_dividents")
            result=("vld",result)#always validd, just fixing if anything is wrong
        else: result=("vld",result)
    else: result=("vld",dividents)
    return result

def check_market_cap(ticker,market_cap):
    if market_cap <0:
        result=get_info(ticker=ticker,info="Market Cap",timeout=10)
        if str(result).lower().find("m")>=0:
            result=result.lower().split("m")[0]
            result=float(result)*1000000
        if str(result).lower().find("b")>=0:
            result=result.lower().split("b")[0]
            result=float(result)*1000000000
        if str(result).lower().find("k")>=0:
            result=result.lower().split("k")[0]
            result=float(result)*1000
        print(result)
        result=float(re.sub(r'[^0-9]',"",str(result)))
        #result=float(str(result).replace(",",""))
        if result<0:
            #print("**"*25,"check_market_cap")
            result=("vld",result)
        else: result=("vld",result)
    else: result=("vld",market_cap)
    return result

def check_news(news):
    status_code=100
    try:
            g_page = requests.get(news)
            status_code=g_page.status_code
    except: status_code=100
    if (status_code != 200):
        result=("ivld",news)
    else: result=("vld",news)
    return result

def check_uploaded_date(uploaded_date):
    
    if not isinstance(uploaded_date,datetime.datetime):
        print("**"*25,"check_uploaded_date")
        print("isinstance(uploaded_date,datetime.datetime)-> ",type(datetime),"datetime.datetime")
        result=("ivld",uploaded_date)
    else: result = ("vld",uploaded_date)
    return result


    """,`time_stamp`) VALUES (NULL,'"""+str(count)+"""','"""+str(website_time)+"""' ,'"""+ticker+"""', '"""+str(price)+"""', '"""+str(volume)+"""', '"""+str(opening)+"""', '"""+str(P_E)+"""', '"""+str(beta)+"""', '"""+str(earnings)+"""', '"""+str(dividents)+"""', '"""+str(p_growth)+"""', '"""+str(market_cap)+"""', '"""+news+"""', '"""+str(uploaded_date)+"""', CURRENT_TIMESTAMP)"""

def main_():
    counter=0
    date='2018-01-17'    
    data_list=mysql_read_data(table='info',date=date)# feching all data
    data_list_vld=mysql_read_data(table='info_vld',date=date,column='uploaded_date')# feching all data
    data_list_ivld=mysql_read_data(table='info_ivld',date=date,column='uploaded_date')# feching all data
    length=len(data_list)
    print("Number of records -> ",length)
    print("Vld-> ",len(data_list_vld)," | ivld-> ",len(data_list_ivld)," Total-> ",len(data_list_vld)+len(data_list_ivld))
    if length!= len(data_list_vld)+ len(data_list_ivld) and (len(data_list_vld)!=0 or len(data_list_ivld) !=0 ):
            print(mysql_delete(table='info_ivld',date=date))
            print(mysql_delete(table='info_vld',date=date))
            data_list_vld=mysql_read_data(table='info_vld',date=date,column='uploaded_date')# feching all data
            data_list_ivld=mysql_read_data(table='info_ivld',date=date,column='uploaded_date')# feching all data
            print("Number of records -> ",length)
            print("Vld-> ",len(data_list_vld)," | ivld-> ",len(data_list_ivld)," Total-> ",len(data_list_vld)+len(data_list_ivld))
    k=input()
    #kk[0],kk[1],"14:02:23",kk[3],kk[4],kk[5],kk[6],kk[7],kk[8],kk[9],kk[10],kk[11],kk[12],kk[13]
	#print(querry)
    for record in data_list:
        counter+=1
        id_count=record[0]
        time=record[1]
        ticker=record[2]
        opening=record[3]
        price=record[4]
        volume=record[5]
        P_E=record[6]
        beta=record[7]
        p_growth=record[8]
        earnings=record[9]
        dividents=record[10]
        market_cap=record[11]
        news=record[12]
        uploaded_date=record[13]

        #t=datetime.timedelta(0,300,0)
        #print(time)
        #print(t)
        #print(abs(t-time))
        #print(type(time))
        #k=input()
        #print("id_count= ",record[0],"\n","time= ",record[1],"\n", "ticker= ",record[2],"\n","opening= ",record[3],"\n","price= ",record[4],"\n", "volume= ",record[5],"\n","P_E= ",record[6],"\n","p_growth= ",record[7],"\n","earnings= ",record[8],"\n","dividents= ",record[9],"\n","market_cap= ",record[10],"\n","news= ",record[11],"\n","uploaded_date= ",record[12],"\n")
        print("-"*25,counter,"Out Of ",length,"  ",date)

        while(1):
                #try:
                        result_opening=check_opening(ticker,opening,time,data_list)
                        result_price=check_price(ticker,price,time,data_list)
                        result_volume=check_volume(ticker,volume,time,data_list)
                        result_news=check_news(news)
                        result_uploaded_date=check_uploaded_date(uploaded_date)
                        result_time=check_time(time,result_uploaded_date)
                        result_P_E=check_P_E(ticker,P_E)
                        result_beta=check_beta(ticker,beta)
                        result_dividents=check_dividents(ticker,dividents)
                        result_market_cap=check_market_cap(ticker,market_cap)
                        break
               #""" except Exception as e:

                        """print("*"*50)
                        print(e)
                        print("*********************** E R R O R    Trying again ****************************")
                        print("result_opening",result_opening)
                        print("result_price",result_price)
                        print("result_volume",result_volume)
                        print("result_news",result_news)
                        print("result_uploaded_date",result_uploaded_date)
                        print("result_time",result_time)
                        print("result_P_E",result_P_E)
                        print("result_beta",result_beta)
                        print("result_dividents",result_dividents)
                        print("result_market_cap",result_market_cap)
                        print("*"*50)
                        print("*"*50)"""
                        #time.sleep(30)

    
        


        
        #if "ivld" in result:
           # mysql_send_data_table("info_ivld",)
           # continue
        """ print("result_opening= ",result_opening)
        print("result_price= ",result_price)
        print("result_volume= ",result_volume)
        print("result_time= ",result_time)
        print("result_uploaded_date= ",result_uploaded_date)
        print("result_news= ",result_news)
        print("result_P_E= ",result_P_E)
        print("result_dividents= ",result_dividents)
        print("result_market_cap= ",result_market_cap)"""
        
        if "ivld" in (result_news[0],result_uploaded_date[0],result_time[0],result_P_E[0],result_beta[0],result_dividents[0],result_market_cap[0],result_opening[0], result_price[0],result_volume[0]):
                print("Invalid Somewhere")
                #k=input()
                mysql_send_data_table("info_ivld",id_count,result_time[1],ticker,result_opening[1],result_price[1],result_volume[1],result_P_E[1],result_beta[1],p_growth,earnings,result_dividents[1],result_market_cap[1],result_news[1],result_uploaded_date[1])

        else:
                #def mysql_send_data_table(table,count,website_time,ticker,price,volume,opening,P_E,earnings,dividents,p_growth,market_cap,news,uploaded_date):
                mysql_send_data_table("info_vld",id_count,result_time[1],ticker,result_opening[1],result_price[1],result_volume[1],result_P_E[1],result_beta[1],p_growth,earnings,result_dividents[1],result_market_cap[1],result_news[1],result_uploaded_date[1])


main_()

print("==================[ D O N E ]==================")
k=input()






def check_():
    pass
def check_():
    pass
def check_():
    pass
def check_():
    pass
def check_():
    pass
def check_():
    pass

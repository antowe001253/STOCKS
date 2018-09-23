from datetime import datetime
import re
import calendar
import time


def weeklyReport():
    pass

def readData():
	f=open("list_data_3.txt",'r')
	text=f.read()
	f.close()
	#k=input(text)
	return text
    #return  "5-22-2018 DRYS \n5-23-2018  CCSA \n5-24-2018  CCSA \n5-25-2018 MGK"

#cleaning
#----------
def cleanData(data):
    data=data.replace(",",";")
    data_split=data.split("\n")
    #k=input(data_split)
    return data_split

def getDayName(today_date):
        d = datetime.strptime(today_date, '%m-%d-%Y')
        day_string = d.strftime('%m-%a-%Y')
        day=re.findall('-(\w+)-',day_string)
        #print(day_string)
        #print("Day -> ",day[0])
        return day[0]
    
def analysis(pos,neg,prices,display='No'):
    
    open_price=parsePrice(prices)[0]
    close_price,price_time=parsePrice(prices)[1],parsePrice(prices)[2]
    if display=='Yes':
        print("open_price: ",open_price)
        print("close_price: ",close_price)
        print("price_time: ",price_time)
        k=input(prices)
    price_dif=close_price-open_price
    if price_dif>=0:pos=pos+1
    else: neg=neg+1
    return pos,neg

#Anaysing: getting date for a specific data
#-------------------------------------------

def parsePrice(prices):
    #print(prices)
    #print(prices)
    return float(prices[0]),0 if prices[1].find("None")>=0 else float(prices[1].split("-")[0]),prices[1].split("-")[1]

def getDateFromMonthYear(month,year):
	num_days = calendar.monthrange(year, month)[1]
	import datetime
	days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
	return days
    
def getDatesUntilToday():
    from datetime import date
    today_date = time.strftime("%m-%d-%Y ")
    month_= today_date.split("-")[0]
    days_= today_date.split("-")[1]
    #print(month_)
    days,days_final=[],[]
    for each_month in range(6,int(month_)+1):
        days+=getDateFromMonthYear(each_month,2018)
        if date.today() in days:
            print("Today's date found -> ",today_date)
            for each_d in days:
                days_final.append(each_d)
                if date.today() == each_d: break
            break
    return days_final
    #for i in days_final:print(i)
    


def dailyreportAnalysis(data,display='No'):
    weekly_pos,weekly_neg,all_pos,all_neg=0,0,0,0
    f=open("try.csv",'w').close()
    list_of_dates=["05-23-2018","05-25-2018","05-28-2018","06-01-2018","06-04-2018","06-05-2018"]
    list_of_dates=getDatesUntilToday()
    f=open("try.csv",'a')
    
    for each_date in list_of_dates:
        each_date=str(each_date)
        # changing format from _y-m-d to m-d-Y and from datetime to str
        each_date=each_date.split("-")[1]+"-"+each_date.split("-")[2]+"-"+each_date.split("-")[0]
        #k=input(each_date)
        day_name=getDayName(each_date)# the input has to be str
        if day_name=='Sun' or day_name=='Sat': continue
        
        data_prepared,pos,neg=[],0,0
        if display=='Yes':
            k=input(each_date)
            print("="*50)
        for line in data:
            #if display=='Yes': k=input(line)
            if line.split(" ")[0]==each_date:
                if display=='Yes': k=input(line)
                pos,neg=analysis(pos,neg,line.split()[4:6])
                data_prepared.append(line)
                
        #print("Data prepared-> ",data_prepared)
        
        #Orginize to save in file
        #print(data_prepared)
        data_orginize=",".join(data_prepared)
        sumT=pos+neg if pos+neg!=0 else 1
        #data_orginize=day+", ["+str(pos*100/(sumT))+"% "+str(neg*100/(sumT))+"% "+str(pos+neg)+"], "+data_orginize+'\n'
        data_orginize=day_name+", [ Good:"+str(pos)+" Bad:"+str(neg)+" ToT:"+str(pos+neg)+"], "+data_orginize+'\n'
        weekly_pos,weekly_neg=weekly_pos+pos,weekly_neg+neg
        all_pos,all_neg=all_pos+weekly_pos,all_neg+weekly_neg

        
        #print(data_orginize)
        print('='*75)
        for line in data_orginize.split(','):
            
            #print(line)
            #for i in line[1:]:
            if len(line.split())>5:
                print("[","G" if parsePrice(line.split()[4:6])[1]-parsePrice(line.split()[4:6])[0]>=0 else "B","] "+" ".join(line.split()[:]))
            else: print(line)
            print('-'*50)
        #print("Data to be sent-> ",[ print(line) for line in data_orginize])
        f.write(data_orginize)
        if day_name=='Fri':
            print('\n\n')
            data_orginize='\nWEEKLY SUMMARY,Good:,'+str(weekly_pos)+',Bad:,'+str(weekly_neg)+',Total:,'+str(weekly_pos+weekly_neg)
            print(data_orginize)
            f.write(data_orginize)
            weekly_pos,weekly_neg=0,0
        
    data_orginize='\nALL SUMMARY,Good:'+str(all_pos)+', Bad:'+str(all_neg)+', Total:'+str(all_pos+all_neg)+ '\t Win :'+str(100*all_pos/(all_pos+all_neg))+"%"
    print(data_orginize)
    f.write(data_orginize)
    f.close()
    
data=readData()
clean_data=cleanData(data)
dailyreportAnalysis(clean_data)
#getDatesUntilToday() for testing
k=input("Done... ")


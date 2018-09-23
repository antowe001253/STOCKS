import  GRAPH_TICKER 
import random
import datetime
import calendar

def getdays(month_start,year_start,month_end,year_end):
        days=[]
        #print(len(range(year_start,year_end+1)))
        for year in range(year_start,year_end+1):
                print(year)
                for month in range(month_start,month_end+1):
                        #print(month)
                        num_days = calendar.monthrange(year, month)[1]
                        days = days+[datetime.date(year, month, day) for day in range(1, num_days+1)]
        return days

def checkContaint(ticker_time,hour):
	count=0
	for line in ticker_time:
		if int(str(line).split(":")[0])==hour:
			count+=1
	return count
def getClosingTime(list_of_timer_for_a_ticker,list_of_price_for_a_ticker,ticker):
	closedAt_time,closedAt_price=0,0
	count=0
	for eachRecord in list_of_timer_for_a_ticker:
		if int(str(eachRecord).split(":")[0]) == 15:
			if closedAt_time==0 or eachRecord>closedAt_time:
				closedAt_time=eachRecord
				closedAt_price=list_of_price_for_a_ticker[count]  
			#print(eachRecord,list_of_price_for_a_ticker[count],ticker,count)
		count+=1
	return closedAt_time,closedAt_price

"""def getOpeningTime(list_of_timer_for_a_ticker,list_of_price_for_a_ticker,ticker):
    closedAt_time,closedAt_price=0,0
    count=0
    for eachRecord in list_of_timer_for_a_ticker:
        if int(str(eachRecord).split(":")[0]) == 16:
            if closedAt_time==0 or eachRecord>closedAt_time:
                closedAt_time=eachRecord
                closedAt_price=list_of_price_for_a_ticker[count]  
            print(eachRecord,list_of_price_for_a_ticker[count],ticker,count)
        count+=1
    return closedAt_time,closedAt_price"""
def preprocessingData(day):# geting all info vol, price of each time on that date
	#print(day)
	min_volume=50000
	nbr_timed_records=50
	data=GRAPH_TICKER.GRAPH_TICKER(str(day))
	data.preprocessingData()# geting all info vol, price of each time on that date
	#k=input()
	print("After preprocessingData -> ",len(data.Xtickers.keys()))# umber of time or price on that date
	toDelete=[]
	for ticker in data.Xtickers.keys():#  ticker:time

		"""if ticker!='DLOC':continue
		print(ticker)
		ii=0
		for i in data.Xtickers[ticker]:
			print(i,"\t",data.Ytickers[ticker][ii],ii)
			ii+=1
		#print(data.Xtickers[ticker])"""
		data.closeAt[ticker]=getClosingTime(data.Xtickers[ticker],data.Ytickers[ticker],ticker)[-1]
		#print("Opening-> ",data.opening[ticker],"   Closed At-> ",data.closeAt[ticker])
		if len(data.Xtickers[ticker])<nbr_timed_records or sum(data.volume[ticker])/len(data.volume[ticker])<min_volume:
			#print("We are removing -> ",ticker,'  | len-> ',len(data.Xtickers[ticker]),'  |Vol->',sum(data.volume[ticker])/len(data.volume[ticker]))
			#data.graph(data.Xtickers[ticker],data.Ytickers[ticker],data.volume[ticker],ticker)
			toDelete.append(ticker)
		if_time = checkContaint(data.Xtickers[ticker],15)
		if if_time <7:
			if ticker not in  toDelete:
				toDelete.append(ticker)
		#print(set(random.sample(data.Ytickers[ticker],len(data.Ytickers[ticker])//2)))
		#print(len(set(random.sample(data.Ytickers[ticker],len(data.Ytickers[ticker])//2)))==1)
		try:
			if (data.opening[ticker] - data.closeAt[ticker] == 0 or len(set(random.sample(data.Ytickers[ticker],len(data.Ytickers[ticker])//2)))==1):
				if ticker not in  toDelete:
					#print("Try")
					#data.graph(data.Xtickers[ticker],data.Ytickers[ticker],data.volume[ticker],ticker)
					toDelete.append(ticker)
		except:
			if ticker not in  toDelete: 
				#print("Except", ticker)
				data.opening[ticker]=0
				#data.graph(data.Xtickers[ticker],data.Ytickers[ticker],data.volume[ticker],ticker)
				toDelete.append(ticker)
			
			
		#else:
			#data.graph(data.Xtickers[ticker],data.Ytickers[ticker],data.volume[ticker],ticker)
			#print("Opening-> ",data.opening[ticker],"   Closed At-> ",data.closeAt[ticker])
		#print (ticker," -> ",len(data.Xtickers[ticker]),"|",sum(data.volume[ticker])/len(data.volume[ticker]))


	for i in toDelete:
		del (data.Xtickers[i])
	#[del (data.Xtickers[ticker]) for i in toDelete]
	if len(data.Xtickers.keys())==0: print('Remain-> ',len(data.Xtickers), '  Removed-> ',len(toDelete))
	return data # a class having data for one day
	#ticker='CSRH'
	#data.graph(data.Xtickers[ticker],data.Ytickers[ticker],data.volume[ticker],ticker)


def classification(data,day):
	losing=[]
	wining=[]
	best=[]
	field={}
	total=len(data.Xtickers)
	pw,pl,pb=0,0,0
	if total>0: print("Total number of Ticker -> ",total)

	for  ticker in data.Xtickers.keys():
		ticker_day=ticker+" "+str(day)
		best.append(ticker)
		if ticker in data.beta.keys():beta=data.beta[ticker]
		else: beta=0
		#k=input(beta)
		field[ticker_day]=('A',beta,data.news[ticker])# dic of ticker_day:(grade,news for that ticker)
		for eachPrice in data.Ytickers[ticker]:
			if eachPrice<data.opening[ticker]:
				del(field[ticker_day])
				best.pop()
				break
		if data.closeAt[ticker]-data.opening[ticker]>0:
			wining.append(ticker)
			if ticker_day not in field: field[ticker_day]=('C',beta,data.news[ticker])
		elif data.closeAt[ticker]-data.opening[ticker]<=0:
			losing.append(ticker)
			field[ticker_day]=('F',beta,data.news[ticker])


	if total>0:
		print("Nbr of Losing-> %0.3f"%(len(losing)),"Nbr of Wining-> %0.3f"%(len(wining)),"Nbr of Best-> %0.3f"%(len(best)))
		pl,pw,pb=len(losing)/float(total)*100,len(wining)/float(total)*100,len(best)/float(total)*100
		print("%% of Losing-> %0.2f%%"%(pl),"%% of Wining-> %0.2f%%"%(pw),"%% of Best-> %0.2f%%"%(pb))

	#count=0
	#for ticker in best:
		#print(count,"/",total)
		#count+=1
		#data.graph(data.Xtickers[ticker],data.Ytickers[ticker],data.volume[ticker],ticker)
	return losing,wining,best,field

def main(months=[11], years=[2017]):
	days=[]
	#days=getdays(1,2018,1,2018)
	days=getdays(10,2017,12,2017)
	days+=getdays(1,2018,4,2018)
	print("Number of days-> ",len(days))
	#k=input()
	
	#days=['2017-12-22']
	pl,pw,pb=[],[],[],
	field={}
	[print(day) for day in days]
	k=input("Waiting")
	data_date_dict={}
	for day in days:
		print("-"*50)
		data=preprocessingData(day)
		# dic of date:GRAPH_TICKER  FOr date, we have a class having the properties of tickers: time tickers:prices  tickers:beta
		data_date_dict[str(day)]=data# list of all the data class by date
		
		#k=input(len(data.Xtickers.keys()))
		results=classification(data,day)
		field.update(results[-1])# add the last element of return losing,wining,best,field which is field->a dic [ticker_day]=('C',beta,data.news[ticker])
		#print(results)
		if results[0]!=0 and len(results[0])>0:
			pl+=results[0]
			pw+=results[1]
			pb+=results[2]
			print("-"*25)
			print("Nbr of Lossing-> %0.2f"%(len(pl)),"   ","Nbr of Wining-> %0.2f"%(len(pw)),"   ","Nbr of Best-> %0.2f"%(len(pb)),"   ")
			print("%% of Lossing-> %0.2f"%(100*len(pl)/(len(pl)+len(pw))),"   ","%% of Wining-> %0.2f"%(100*len(pw)/(len(pw)+len(pl))),"   ","%% of Best-> %0.2f"%(100*len(pb)/(len(pw)+len(pl))),"   ")
	#k=input(field)
	return (field,data_date_dict)
	#for i in range(len(pb)):
	   # print("Lossing-> %0.2f"%pl[i],"   ","Wining-> %0.2f"%pw[i],"   ","Best-> %0.2f"%pb[i])
	print("="*70)
	print("Nbr of Lossing-> %0.2f"%(len(pl)),"   ","Nbr of Wining-> %0.2f"%(len(pw)),"   ","Nbr of Best-> %0.2f"%(len(pb)),"   ")
	print("%% of Lossing-> %0.2f"%(100*len(pl)/(len(pl)+len(pw))),"   ","%% of Wining-> %0.2f"%(100*len(pw)/(len(pw)+len(pl))),"   ","%% of Best-> %0.2f"%(100*len(pb)/(len(pw)+len(pl))),"   ")

	unik=set(pb)
	print("Repeated Best-> %d  | Unique Best(set)-> %d"%(len(pb),len(unik)))
	text=" ".join(pb)
	for line in unik:
		r=(line,text.count(line))
		if r[1]>1:
				print(r)

	i=0
	for eachTicker in field.keys():
		if field[eachTicker][0]=='A':
			i+=1
		print(i)

########################################################################
#field is a dict with all ticker
#field[a ticker + date]  ->  (scrore,news) // data_by_date['2017-11-27'].Xtickers['LB']
#data_date_dict  -- dict key=date value->data

# HOw to use  getdays
#days=getdays(10,2017,12,2017)
#days+=getdays(1,2018,1,2018)
#for day in days: print(str(day))
#print(len(days))
#main()

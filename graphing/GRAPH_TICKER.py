import sys, os
import pylab as plt
import requests
sys.path.append('../Python34/')
from  connect_mysql import *
from get_ticker_info import *

class GRAPH_TICKER():
    def __init__(self,date):
        self.date=date#date
        self.data=mysql_read_data(table='info_vld',date=self.date,column='uploaded_date')
        self.Xtickers={}# dictionary of tickers: time 
        self.Ytickers={}# dic of tickers: prices
        self.volume={}
        self.closeAt={}
        self.opening={}
        self.news={}
        self.beta={}
    def __str__(self):
        return "< Date ->"+self.date
    def preprocessingData(self):
        counter=0
        length=len(self.data)
        print("Number of records -> ",length)
        #kk[0],kk[1],"14:02:23",kk[3],kk[4],kk[5],kk[6],kk[7],kk[8],kk[9],kk[10],kk[11],kk[12],kk[13]
            #print(querry)
        invld,vld=0,0
        for record in self.data:
            counter+=1
            record=record[1:]# only for info_vld
            id_count=record[0]
            time=record[1]
            ticker=record[2]
            opening=record[3]
            if int(str(time).split(":")[0]) in range(10,16):self.opening[ticker]=opening
            price=record[4]
            volume=record[5]
            P_E=record[6]
            beta=record[7]
            if beta != 0: self.beta[ticker]=beta
            p_growth=record[8]
            earnings=record[9]
            dividents=record[10]
            market_cap=record[11]
            news=record[12]
            self.news[ticker]=news
            uploaded_date=record[13]
            #print(record)
            #k=input()
            if int(str(time).split(":")[0]) not in range(9,17) :
                invld+=1
                continue
            try:
                vld+=1
                self.Xtickers[ticker].append(str(time).zfill(8))#[:str(time).rfind(":")])
                self.Ytickers[ticker].append(float(price))
                self.volume[ticker].append(float(volume))
            except:
                vld+=1
                self.Xtickers[ticker]=[]
                self.Ytickers[ticker]=[]
                self.volume[ticker]=[]
                
                self.Xtickers[ticker].append(str(time).zfill(8))#[:str(time).rfind(":")])
                self.Ytickers[ticker].append(float(price))
                self.volume[ticker].append(float(volume))
        print("Vld-> ",vld,"  Invld -> ",invld)            
    def graph(self,x,y,volume,ticker):
        #plt.figure('%s'%ticker)# new windows for the plot below
        #plt.clf()#o clear the figure

        fig, ax = plt.subplots()
        ax.plot_date(x,y,label='Price',linestyle='-',linewidth=3.0)
        fig.autofmt_xdate()
        #plt.ylim(0,900)# Constraint on y ascis
        #plt.plot(x,y,'bo',label='Price',linewidth=3.0)
        #plt.legend(loc='upper left')
        plt.title('%s Vol: %0.0f | open %0.2f | closed %0.2f'%(ticker,sum(volume)/len(volume),self.opening[ticker],self.closeAt[ticker]))
        #plt.autofmt_xdate()
        plt.show()


def main():
	t=GRAPH_TICKER('2017-12-01')
	t.preprocessingData()
	count=0
	print("Length-> ",len(t.Xtickers))
	for i in t.Xtickers.keys():
		count=len(t.Xtickers[i])
		print(count)
		print(i)
		#k=input()
		k="go"
		if k=="go":
			for nbr in  range(len(t.Ytickers[i])):
				print(t.Xtickers[i][nbr],"\t",t.Ytickers[i][nbr],"\t",t.volume[i][nbr])
			t.graph(t.Xtickers[i],t.Ytickers[i],t.volume[i],i)
			
			#k=input()

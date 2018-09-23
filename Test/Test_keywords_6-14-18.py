import re
import requests
import sys
import pandas as pd
import pylab as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA

from datetime import date
import calendar
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD 
from sklearn.preprocessing import normalize 

sys.path.append('../graphing/')
import reporting
sys.path.append('../ML/')
sys.path.append('../Python34/')
import get_ticker_info

import TICKER
#/w+ -> any word
#d+ any number
#(.*?) -> anything
#[] only match set of char -> list of char ['c']
#k=(re.findall('^<script(.*?)</script>',text,re.DOTALL))
#re.findall('>(\d+.\d+)<',g_txt[position-calibrator:position],re.DOTALL)
mUrl='http://www.marketwired.com/press-release/peapack-gladstone-bank-announces-appointment-christian-gaudioso-senior-vice-president-nasdaq-pgc-2242109.htm'
gUrl='http://www.globenewswire.com/news-release/2017/11/28/1207209/0/en/Castle-Resources-Announces-Going-Private-Transaction.html'
#urlRequesr = requests.get(url)
#text = urlRequesr.text
#url='http://www.globenewswire.com/news-release/2017/11/28/1207209/0/en/Castle-Resources-Announces-Going-Private-Transaction.html'
#print (len(text))
#k=(re.findall('<div class="mw_release">(.*?)</div>',text,re.DOTALL))
#print(len(k))

yUrl='https://finance.yahoo.com/news/makes-nordson-ndsn-stock-solid-135001147.html'
#url='http://finance.yahoo.com/m/33047d8b-c7b1-37d3-bf70-408b93f81ff6/ss_ranchimall-and-ico%E2%80%99s-in.html'
"""
http://finance.yahoo.com/news/provider-businesswire/?bypass=true",
                 "http://finance.yahoo.com/news/provider-accesswire/?bypass=true",
                 "http://www.marketwired.com/news_room/all_news/?headlines-only=HLO",
                 "http://www.globenewswire.com/",
                "http://finance.yahoo.com/news/provider-prnewswire/?bypass=true"
"""
header="Date_m_d_Y-Name-Volume-Beta-Opening-Previous_close_price-Previous_close_time-\
Lowest_price-Keywords_found-Url-Title"

delimiter="^~^"
def getParams(title,body,url):
        #print(url)
        urlRequesr = requests.get(url)
        text = urlRequesr.text
        param='%s(.*?)%s'%(title[0],title[1])
        #k=input(param)
        title=re.findall(param,text,re.DOTALL)
        #print("======================= [Title]",len(title))
        param='%s(.*?)%s'%(body[0],body[1])
        body=re.findall(param,text,re.DOTALL)
        #assert len(title)==1 and len(body)==1, "No body in URL found length->%d"%len(body)
        if len(title)!=1 or len(body)!=1:
            print("No body in URL found length->%d"%len(body))
            #k=input()
            return "",""
        #print("======================== [Body]",len(body[0]))
        #return title[0],clean(body[0])
        return re.sub(r'[^\w\s]',' ',title[0]),re.sub(r'[^\w\s]',' ',clean(body[0]))


        


def getContent(url):
        title=""
        body=""
        
        if url.lower().find('globenewswire')>=0:
            title=('<title>','</title>')
            body=('<span itemprop="articleBody">','<!--Begin Related Articles-->')
            
        elif url.lower().find('marketwired')>=0:
            title=('<p id="news-date">','<div class="mw_release">')
            body=('<div class="mw_release">','</div>')

        elif url.lower().find('yahoo')>=0:
            title=('<title>','</title>')
            body=('<article','</article>')
            
        #print(title)
        #print(body)
        
        
        assert len(title)>0 and len(body)>0 , "not title or body encloses"+"      "+url
        return getParams(title,body,url)


def top_tfidf_feats(row, features, top_n=20):
        topn_ids = np.argsort(row)[::-1][:top_n]
        top_feats = [(features[i], row[i]) for i in topn_ids]
        df = pd.DataFrame(top_feats, columns=['features', 'score'])
        return df
def top_feats_in_doc(X, features, row_id, top_n=25):
        row = np.squeeze(X[row_id].toarray())
        return top_tfidf_feats(row, features, top_n)

def top_mean_feats(X, features,grp_ids=None, min_tfidf=0.1, top_n=25):
        if grp_ids:
            D = X[grp_ids].toarray()
        else:
            D = X.toarray()
        D[D < min_tfidf] = 0
        tfidf_means = np.mean(D, axis=0)
        return top_tfidf_feats(tfidf_means, features, top_n)


def plot_tfidf_classfeats_h(dfs):
        fig = plt.figure(figsize=(12, 9), facecolor="w")
        x = np.arange(len(dfs[0]))
        for i, df in enumerate(dfs):
            ax = fig.add_subplot(1, len(dfs), i+1)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.set_frame_on(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()
            ax.set_xlabel("Tf-Idf Score", labelpad=16, fontsize=14)
            ax.set_title("cluster = " + str(df.label), fontsize=16)
            ax.ticklabel_format(axis='x', style='sci', scilimits=(-2,2))
            ax.barh(x, df.score, align='center', color='#7530FF')
            ax.set_yticks(x)
            ax.set_ylim([-1, x[-1]+1])
            yticks = ax.set_yticklabels(df.features)
            plt.subplots_adjust(bottom=0.09, right=0.97, left=0.15, top=0.95, wspace=0.52)
        plt.show()

def top_feats_per_cluster(X, y, features, min_tfidf=0.1, top_n=25):
        dfs = []

        labels = np.unique(y)
        for label in labels:
            ids = np.where(y==label) 
            feats_df = top_mean_feats(X, features, ids, min_tfidf=min_tfidf, top_n=top_n)
            feats_df.label = label
            dfs.append(feats_df)
        return dfs

def saveFile(tic,score,tit,b):
        delimiter="`"
        f=open("data_test.txt","w").close()
        f=open("data_test.txt","a")
        for i in range(len(tit)):
            data=str(tic[i])+delimiter+score[i]+delimiter+str(tit[i])+delimiter+str(b[i])
            f.write(re.sub(r'[^\x20-\x7e]',"",data)+"\n")
        print("Saved ...")
        f.close()
pA=0
pNotA=0
wordFrequencyWin,wordFrequencyLoss={},{}
totalWordWin,totalWordLoss=0,0


def clean(body):
        body=re.sub(r'[\d+]',"",body)
        stopWord=["nbsp"]
        words=""
        no_words=""
        #print("All words In Body-> ", len(body))
        #print("Count [<>] -> ",body.count("<"))
        t=body.split(">")
        count=0
        for line in t:
            line=line+">"
            #print(line)
            #print("-"*25)
            r=re.findall('<(.+)>',line,re.DOTALL)
            #print(r)
            if len(r)>0:
                count+=1
                no_words+=r[0]
                line=line.replace("<"+r[0]+">","").replace("nbsp","")
                #print(line)
                line=" ".join([i for i in line.split() if len(i)>2])
                #line=" ".join([i for i in line.split(".") if len(i)>2])
                #line=" ".join([i for i in line.split("-") if len(i)>2])
                #if " mr" in line.lower():
                    #print(line)
                #print(line)
                    #k=input()
                words+=line+" "
            #k=input()
        #print("Word-> ",len(words))
        #print("No Word-> ",len(no_words))
        #print("Count[<>] -> ",count)
        #f=open("badwords.txt","w")
        #f.write(no_words)
        #f.close()
        #k=input()
        if len(words)<=0:
            k=input()
            print("-----------------------> ",body)
        return words.lower()

##########################################################################################


def getAllInfo(ticker,url,old_price=1000):
        
	title,body=getContent(url)
	#print("["count,"/",count_t,"]","-"*50, ticker)
	volume=get_ticker_info.get_info(ticker=ticker,info="Volume",display=False)
	#print(volume)
	if str(volume).find(",")>=0:
		volume=volume.replace(",","")
	#print(volume)
	#k=input("-------------")
	opening=get_ticker_info.get_info(ticker=ticker,info="OPEN-value",display=False)
	beta=get_ticker_info.get_info(ticker=ticker,info="Beta",display=False)
	P_E=get_ticker_info.get_info(ticker=ticker,info="PE Ratio",display=False)
	avg_volume=get_ticker_info.get_info(ticker=ticker,info="Avg. Volume",display=False)
	previous_close=get_ticker_info.price_yahoo_parsing(ticker=ticker)
	dividents=get_ticker_info.get_info(ticker=ticker,info="Forward Dividend",display=False)
	if str(dividents).find("%")>=0:
			dividents=dividents.replace("%","")
	market_cap=get_ticker_info.get_info(ticker=ticker,info="Market Cap",display=False)
	if str(market_cap).lower().find("m")>=0:
		market_cap=market_cap.lower().split("m")[0]
		market_cap=float(market_cap)*1000000
	if str(market_cap).lower().find("b")>=0:
		market_cap=market_cap.lower().split("b")[0]
		market_cap=float(market_cap)*1000000000
	if str(market_cap).lower().find("k")>=0:
		market_cap=market_cap.lower().split("k")[0]
		market_cap=float(market_cap)*1000
	lowest_price=old_price
	print(ticker," |Old-> ",old_price," New-> ",previous_close[0])
	#if (previous_close[0]) <(lowest_price): k=input()
	#if old_price!=1000:input()
	b_lowest_price=lowest_price
	if previous_close[0] =='None': lowest_price=old_price
	else:lowest_price=previous_close[0] if (previous_close[0]) <(lowest_price) else (lowest_price)
	#ff=open("lower_price.txt","a")
	#ff.write(ticker+"-Price: "+str(previous_close[0])+" Lower P: "+str(lowest_price)+" Before change: "+str(b_lowest_price)+"\n")
	#ff.close()
	title=title.replace('\n',' ').replace('\r',' ')
	TICKER_instance=TICKER.TICKER(ticker)
	TICKER_instance.setVolume(volume)
	TICKER_instance.setBeta(beta)
	TICKER_instance.setOpening(opening)
	TICKER_instance.setPrevious_close_price(previous_close[0])
	TICKER_instance.setPrevious_close_time(previous_close[1])
	TICKER_instance.setLowest_price(lowest_price)
	#TICKER_instance.setUrl()
	
	TICKER_instance.setTitle(title)
	#return [str(ticker), str(volume), str(beta), str(opening), str(previous_close[0])/
                #+"-"+str(previous_close[1]),str(lowest_price), title.replace('\n',' ').replace('\r',' ')]
	#print(title)
	#print(TICKER_instance)
	#k=input()
	return TICKER_instance
	
def check_keywords_in_title(title,keywords_list):
	result=""
	for word in keywords_list:
		if (title.find(" "+word.lower()+" ")>=0 )and len(word)>1:
			result=word+"-"+result
			
	#print(title)
	#print(keywords_list)
	#print(result)
	#k=input()
	return result

def update_old_records(old_list_of_class):
        print("------------------------------------- Update Old Records")
        OLD_LIST_OF_CLASS=[]
        for EACH_OLD_CLASS in old_list_of_class:
                #line_arr=line.split()
                if EACH_OLD_CLASS.getUrl().find("http")>=0 and EACH_OLD_CLASS.getDate_m_d_Y()==time.strftime("%m-%d-%Y") :# check if the ext file there is a url
                        #n= 8 #if line_arr[7].find("http")>=0 else 6
                        ticker=EACH_OLD_CLASS.getName()
                        url=EACH_OLD_CLASS.getUrl()
                        keywords_found=EACH_OLD_CLASS.getKeywords_found()
                        #keywords_list=line_arr[6]
                        #title=line_arr[8:]
                        lowest_price=EACH_OLD_CLASS.getLowest_price()
                        #k=input(old_price)
                        print(type(lowest_price))
                        print(lowest_price)
                        if lowest_price =='None': lowest_price=1000
                        else: lowest_price=float(lowest_price)
                        #k=input("============")
                        TICKER_instance=TICKER.TICKER(ticker)
                        ff=open("lower_price.txt","a")
                        ff.write(ticker+"-----Price: "+str(EACH_OLD_CLASS.getPrevious_close_price())+" Lower P: "+str(EACH_OLD_CLASS.getLowest_price())+"\n")
                        
                        TICKER_instance=getAllInfo(ticker,url,lowest_price)
                        print("Old-> ",EACH_OLD_CLASS.getPrevious_close_price(), " Returned-> " ,TICKER_instance.getLowest_price(),lowest_price)
                       # k=input()
			#print("*8888888888888888888888888888888888888888888888888888",all_info)

                        title= TICKER_instance.getTitle()
                        
                        if len(keywords_found)<1: continue
                        #print("Date-> ",EACH_OLD_CLASS.getDate_m_d_Y())
                        #print("Ticker-> ",TICKER_instance.getName())
                        #print("Volume-> ",TICKER_instance.getVolume())
                        #print("Beta-> ",TICKER_instance.getBeta())
                        #print("Open-> ",TICKER_instance.getOpening())
                        #print("Now-> ",TICKER_instance.getPrevious_close_price())
                        #print("Lowest-> ",TICKER_instance.getLowest_price())
                        #print("title-> ",title)
                        #print("Keywords Found-> ",keywords_found)
                        
                        #data=time.strftime("%m-%d-%Y")+" "+++++++++++" ".join(all_info[:-1]+[keywords_found]+[new]+[all_info[-1]])
                        TICKER_instance.setDate_m_d_Y(time.strftime("%m-%d-%Y"))
                        TICKER_instance.setKeywords_found(keywords_found)
                        TICKER_instance.setUrl(url)
                       # print(TICKER_instance)
                        ff.write(ticker+"After-----Price: "+str(EACH_OLD_CLASS.getPrevious_close_price())+" Lower P: "+str(EACH_OLD_CLASS.getLowest_price())+"\n")
                        ff.close()
                        #data_final.append(data)### the return data should be a list of string
                        OLD_LIST_OF_CLASS.append(TICKER_instance)
                        #print(data_final)
                        #k=input(data)
                        
                else:
                        
                        if EACH_OLD_CLASS.getDate_m_d_Y() ==time.strftime("%m-%d-%Y"):
                                print(EACH_OLD_CLASS.getTitle().find("http")>=0)
                                print(EACH_OLD_CLASS)
                                print(time.strftime("%m-%d-%Y"))
                                print(EACH_OLD_CLASS)
                                print("http is not find in url")
                                k=input()
                        OLD_LIST_OF_CLASS.append(EACH_OLD_CLASS)# good, class, not change done, record from a prevoius date
                #k=input("done ...")
        return OLD_LIST_OF_CLASS
        
def textToClass(data):##data is a list
        print("-"*75,"textToClass")
        
        list_of_class=[]
        header=data.pop(0)
        print("Headers")
        print(header)
        #k=input()
        for line in data:
                print(line)
                line_slipt=line.split(delimiter)
                if len(line_slipt)>1:
                        if len(line_slipt)!=11:
                                
                                print("Length is diff to 11","|  Actual length-> ",len(line_slipt))
                                print("Record")
                                print(line)
                                print("All header in orders on python so far")
                                print("Date_m_d_Y-Name-Volume-Beta-Opening-Previous_close_price-Previous_close_time-\
        Lowest_price-Keywords_found-Url-Title")
                                k=input()
                        TICKER_instance=TICKER.TICKER(line_slipt[1])
                        TICKER_instance.setDate_m_d_Y(line_slipt[0])
                        TICKER_instance.setVolume(line_slipt[2])
                        TICKER_instance.setBeta(line_slipt[3])
                        TICKER_instance.setOpening(line_slipt[4])
                        TICKER_instance.setPrevious_close_price(line_slipt[5])
                        TICKER_instance.setPrevious_close_time(line_slipt[6])
                        TICKER_instance.setLowest_price(line_slipt[7])
                        TICKER_instance.setKeywords_found(line_slipt[8])
                        TICKER_instance.setUrl(line_slipt[9])
                        TICKER_instance.setTitle(line_slipt[10])
                        list_of_class.append(TICKER_instance)
                        #k=input("Done ...")
        
        return list_of_class

def classToText(CLASS_LIST):
        print("-"*50,"classToText")
        #delimiter="^~^"
        #list_of_class=[]
        #print("Headers")
        print(header)
        #k=input()
        all_text=""
        for EACH_CLASS in CLASS_LIST:
                #print(EACH_CLASS)
                Date_m_d_Y=EACH_CLASS.getDate_m_d_Y()
                Name=EACH_CLASS.getName()
                Volume=EACH_CLASS.getVolume()
                Beta=EACH_CLASS.getBeta()
                Opening=EACH_CLASS.getOpening()
                Previous_close_price=EACH_CLASS.getPrevious_close_price()
                Previous_close_time=EACH_CLASS.getPrevious_close_time()
                Lowest_price=EACH_CLASS.getLowest_price()
                Keywords_found=EACH_CLASS.getKeywords_found()
                Url=EACH_CLASS.getUrl()
                Title=EACH_CLASS.getTitle()

                text=str(Date_m_d_Y)+delimiter+str(Name)+delimiter+str(Volume)+delimiter+str(Beta)+delimiter+str(Opening)\
                      +delimiter+str(Previous_close_price)+delimiter+str(Previous_close_time)+\
                      delimiter+str(Lowest_price)+delimiter+str(Keywords_found)+delimiter+Url+delimiter+Title+'\n'
                text_slipt=text.split(delimiter)
                if len(text_slipt)!=11:
                        
                        print("Length is diff to 11")
                        print("Record")
                        print(text)
                        print("All header in orders on python so far")
                        print("Date_m_d_Y-Name-Volume-Beta-Opening-Previous_close_price-Previous_close_time-\
Lowest_price-Keywords_found-Url-Title")
                        k=input()
                all_text+=text
        return all_text
        
        
                
def loadData(TICKER_new_class):#onle class
        #header="Date_m_d_Y-Name-Volume-Beta-Opening-Previous_close_price-Previous_close_time-\
#Lowest_price-Keywords_found-Url-Title"
        print("[FOUND]=========================================Loading ...",TICKER_new_class)
        all_data=[]
        try: f=open('list_data_3.txt','r')
        except:
                f=open('list_data_3.txt','w').close()
                f=open('list_data_3.txt','r')
        getData=f.read()# old data
        data=getData.split("\n")# old data
        OLD_LIST_OF_CLASS=textToClass(data)
        print('Old data [',len(OLD_LIST_OF_CLASS),']'+'-'*50+'->' )
        
        flag=True
        OLD_LIST_OF_CLASS_updated=update_old_records(OLD_LIST_OF_CLASS)## update the old record of the day to their urrent price
        #for EACH_CLASS in OLD_LIST_OF_CLASS_updated:
         #       print(EACH_CLASS)
          #      print("-"*25)
        #k=input("Updating Done")
        for OLD_CLASS_updated in OLD_LIST_OF_CLASS_updated:# each record in the old data from the text file
                #if len(line)>0:
                        #print(OLD_CLASS_updated)
                        #print("-"*25)
                        if OLD_CLASS_updated.getName()==TICKER_new_class.getName(): # if one record in that old data is equal to the new data/line
                                flag=False  # line is not new, it existed before
                                TICKER_new_class.setDate_m_d_Y(time.strftime("%m-%d-%Y"))
                                all_data.append(TICKER_new_class)
                                print(TICKER_new_class)
                                #k=input("Record matching, time updated")
                                ###all_data.append(time.strftime("%m-%d-%Y")+" "+" ".join(all_info)) #that new data is added to all data
                        else: all_data.append(OLD_CLASS_updated) # in case none of the old data matches the new data, we still record back all the old data
        if flag==True:
                TICKER_new_class.setDate_m_d_Y(time.strftime("%m-%d-%Y"))
                
                print("-"*75,"New record added -> ",TICKER_new_class)
                #k=input()
                all_data.append(TICKER_new_class) # here we add all the new data
                #all_data.append(time.strftime("%m-%d-%Y")+" "+" ".join(all_info)) # here we add all the new data
        print("nbr of classes: ",len(all_data))
        #k=input("Converting Class to Text")
        all_text=classToText(all_data)
        all_text=header+'\n'+all_text
        #print(all_text)
        #k=input("Data to be saved ")
        #f_data="\n".join(all_data)
        
        f=open('list_data_3.txt','w')
        f.write(all_text)
        print('Data saved -> \n',all_text)
        print("-"*25)
        print('Total-> ',len(all_data),' |Data added -> ',1 if flag==True else 0)
        f.close()
        #k=input()

def dailyReport():
        f=open('list_data_3.txt','r')
        getData=f.read()
        data=getData.split("\n")

        for each_data in data:
                ticker=each_data.split()[0]
                url=each_data.split()[-2]
                all_info=getAllInfo(ticker,url)
                keywords_found=each_data.split()[-1]
                print("Ticker-> ",all_info[0])
                print("Volume-> ",all_info[1])
                print("Beta-> ",all_info[2])
                print("Open-> ",all_info[3])
                print("Now-> ",all_info[4])
                print("Lowest-> ",all_info[5])
                print("title-> ",all_info[6])
                print("Keywords Found-> ",keywords_found)
                
         
def main():
	#try:
#symbols_and_prices_file.write((ticker+" "+str(price)+" "+time.strftime("%Y%m.")+str((int(time.strftime("%d"))*24)+(int(time.strftime("%H"))))+" "+ticker_news[ticker]).replace("\n","")+'\n')
		#delimiter="^~^"
		f=open("C:/Users/Alex.Ntowe/Documents/Project/Python/STOCKS/Python34/data/nbr_of_stock_to_be_sent_to_db.txt",'r')
		f_words=open("keywords.txt","r")
		keywords_text=f_words.read()
		keywords_list=keywords_text.split("\n")
		data=f.read()
		length=len(data.split("\n"))
		print("Lentgh of data -> ",length)
		#k=input()
		count_=0
		for each_data in data.split("\n"):#each data in the file generated by best_plays
			if each_data.find("Done writting in file")>=0: continue
			each_data=each_data.split()
			if len(each_data)<=1:continue
			ticker=each_data[0]
			url=each_data[-1]
			#print("All-> ",each_data)
			#print ("Ticker-> ",ticker,"News-> ",new)
			count_=count_+1
			print("[",count_,"/",length,"]","-"*50, ticker)
			TICKER_class=getAllInfo(ticker,url)
			#print("*8888888888888888888888888888888888888888888888888888",all_info)
			#title= all_info[6]
			title= TICKER_class.getTitle()
			keywords_found=check_keywords_in_title(" "+title.lower()+" ",keywords_list)#return a list
			if len(keywords_found)<1: continue
			#print("Ticker-> ",all_info[0])
			#print("Volume-> ",all_info[1])
			#print("Beta-> ",all_info[2])
			#print("Open-> ",all_info[3])
			#print("Now-> ",all_info[4])
			#print("Lowest-> ",all_info[5])
			#print("title-> ",title)
			#print("Keywords Found-> ",keywords_found)
			#k=input()
			#print(TICKER_class)
			TICKER_class.setKeywords_found(keywords_found)
			TICKER_class.setUrl(url)
			#print("-"*25,"Adding url and keyword")
			#print(TICKER_class)
			#k=input()
			#loadData(all_info[:-1]+keywords_found+[url]+[all_info[-1]])
			loadData(TICKER_class)# open old record and check if this new record is already there
			#print(all_info)
			
			
		print("="*80)
		print(time.strftime("%b %d, %Y---%H:%M:%S "))
		if len(data.split("\n"))>1:
			if int(time.strftime("%H")) in [16,17,18,19,20,21,22,23,24,0,1,2,3,4,5,6,7]:
				time.sleep(3600)
			else:
				print("Sleeping for 250 secs")
				time.sleep(250)
		if int(time.strftime("%H")) in [16,17,18,19,20,21,22,23,24,0,1,2,3,4,5,6,7]:
				print("Sleeping for: 1h")
				time.sleep(3600)
				
		
		
		#k=input()
	#except:
		#print("error")

	
#field_ticker_by_score,data_by_date=reporting.main(month=[1,2,3],year=2018)

#def lowestPrice(lowest_price,current_price):
        
while(1):
	my_date = date.today()
	day=calendar.day_name[my_date.weekday()]
	hold_dates=['Sunday','Saturday']
	if day in hold_dates :
		print("Today's date -> ",day)
		print("Sleeping for 3600 seonds")
		time.sleep(3600)
		continue
	main()
#loadData(["EPER" ,"1969336", "4.65", "3.310", "3.305-16:01:35", "secured", "EP Energy Announces Pricing Of 7 750  Senior Secured Notes Due 2026"])
#dailyReport()

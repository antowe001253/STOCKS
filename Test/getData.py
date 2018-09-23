import re
import requests
import sys
import pandas as pd
import pylab as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA



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
import keywords
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
def getParams(title,body,url):
        #print(url)
        urlRequesr = requests.get(url)
        text = urlRequesr.text
        param='%s(.*?)%s'%(title[0],title[1])
        #print(param)
        title=re.findall(param,text,re.DOTALL)
        print("======================= [Title]",len(title))
        param='%s(.*?)%s'%(body[0],body[1])
        body=re.findall(param,text,re.DOTALL)
        #assert len(title)==1 and len(body)==1, "No body in URL found length->%d"%len(body)
        if len(title)!=1 or len(body)!=1:
            print("No body in URL found length->%d"%len(body))
            #k=input()
            return "",""
        print("======================== [Body]",len(body[0]))
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
        
        assert len(title)>0 and len(body)>0 , "not title or body encloses"
        return getParams(title,body,url)


def parsing():
        y=getContent(yUrl)
        m=getContent(mUrl)
        g=getContent(gUrl)


        mm=str(m[0]+m[1])
        gg=str(g[0]+g[1])
        yy=str(y[0]+y[1])

        d_m=set(mm.split())
        d_y=set(yy.split())
        d_g=set(gg.split())

        d_mm=set([i for i in d_m if len(i)>3])
        d_yy=set([i for i in d_y if len(i)>3])
        d_gg=set([i for i in d_g if len(i)>3])

        y_m=d_mm&d_yy
        m_g=d_mm&d_gg
        g_y=d_mm&d_yy

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
def readFile(file="data_test.txt"):
        global pNotA
        global pA
        count1,count2,count3,count4=0,0,0,0
        tic,score,tit,b=[],[],[],[]
        delimiter="`"
        f=open("data_test.txt","r")
        count=0
        for line in f:
            
            if line.count(delimiter)!=3:
                print( "Error nbr of ^ -> %d "%line.count(delimiter))
                k=input()
                continue
            x,w,y,z=line.split(delimiter)
            z=extraClean(z)
            if not isinstance(z,str):
                print("len(z)<=0 ", z)
                k=input()
            #print(w)
            #k=input()
            if w=='A':
                    count1+=1
                    #continue
            elif w=='C':
                    count2+=1
                    #continue
            elif w=='F':
                    count3+=1
                    
            
            else: count4+=1
            processEmail(z,w)
            tic.append(x)
            score.append(w);
            tit.append(y)
            b.append(z)
            #print(count,"---",w)
            count+=1
        print(len(b))
        pA=(count1+count2)/float(count1+count2+count3)
        pNotA=count3/float(count1+count2+count3)
        print("pA-> ",pA)
        print("pNotA-> ",pNotA)
        print("Count A-> ",count1,"  Best%-> ",100*count1/(count1+count2+count3))
        print("Count C-> ",count2,"  Win%-> ",100*count2/(count1+count2+count3))
        print("Count F-> ",count3,"  Lost%-> ",100*count3/(count1+count2+count3))
        print("None of A, C, F",count4)
        print("Total A+C+F-> ",count1+count2+count3)
        k=input("Done")
            
        return (tic,score,tit,b)

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
def extraClean(body):
        body=re.sub(r'[\d+]',"",body)
        body=re.sub(r'[\W+]'," ",body)
        #body=body.replace("-"," ").replace("."," ").replace(","," ").replace(")"," ").replace("("," ").replace(":"," ")
        words=""
        data=body.split()
        for line in data:
            #if "st" in line.lower() or "st" in line.lower() or "st" in line.lower() or "st" in line.lower():
             #   print(line)
              #  k=input()
            if len(line)>2:
                words+=line+" "
        return words.lower()

##########################################################################################

def processEmail(body, label):
    global wordFrequencyWin
    global wordFrequencyLoss
    global totalWordWin
    global totalWordLoss
    #print(type(body))
    #print(len(body))
    #print(body[:50])
    #k=input()
    for word in body.split():
        #print(word[:25])
        #k=input()
        if label == "A" or label =="C":
            if word in wordFrequencyWin: wordFrequencyWin[word] += 1 
            else:wordFrequencyWin[word] = 1 
            totalWordWin+= 1
        else:
            if word in wordFrequencyLoss: wordFrequencyLoss[word] += 1
            else: wordFrequencyLoss[word] = 1
            totalWordLoss += 1
def conditionalWord(word, win):
    global wordFrequencyWin
    global wordFrequencyLoss
    global totalWordWin
    global totalWordLoss
    #print("wordFrequencyWin=",len(wordFrequencyWin),"  wordFrequencyLoss=",len(wordFrequencyLoss),"  totalWordWin= ",totalWordWin," totalWordLoss= " ,totalWordLoss)
    if word not in wordFrequencyWin or word not in wordFrequencyLoss: return 1
    #k1=wordFrequencyWin[word]
    #k2=float(totalWordWin)
    #print(k1,k2)
    if win:
       #prob of each win world in all the win word ex: "free":21 times in 1000 words p "free"=21/1000
       return wordFrequencyWin[word]/float(totalWordWin)
    return wordFrequencyLoss[word]/float(totalWordLoss)

def conditionalEmail(body, win):
    result = 1.0
    for word in body:
        #print (word)
        #k=input()
        #getting p(H/E)
        result *= conditionalWord(word, win)
        print(result)
        k=input()
    return result

def classify(new):
    global pA
    global pNotA

    global wordFrequencyWin
    global wordFrequencyLoss
    global totalWordWin
    global totalWordLoss
    p_H_E_win=conditionalEmail(new, True) # P (A | B)
    p_H_E_loss= conditionalEmail(new, False) # P(¬A | B)
    print("p_H_E_win-> ",p_H_E_win)
    print("p_H_E_loss-> ",p_H_E_loss)
    isSpam = pA * p_H_E_win
    notSpam = pNotA * p_H_E_loss

    print("wordFrequencyWin-> ",len(wordFrequencyWin))
    print("wordFrequencyLoss-> ",len(wordFrequencyLoss))
    print("totalWordWin-> ",totalWordWin)
    print("totalWordLoss-> ",totalWordLoss)
    print("pA-> ",pA)
    print("pNotA-> ",pNotA)
    print("Win-> ",isSpam)
    print("Lost-> ",notSpam)
    return isSpam > notSpam



def main(field_ticker_by_score,data_by_date=reporting):
        tic=[]
        tit=[]
        b=[]
        betaList=[]
        score=[]
        k=input("Enter-> web | file: ")
        if k=='web':
            
            #
            #day='2017-12-14'
            #days=reporting.getdays()
            #days+=reporting.getdays(month=12)

            data_list=[]
            #for day in days:
                #data_list.append(reporting.preprocessingData(day))

            #field_ticker_by_score,data_by_date=reporting.main()
            k='go'
            for ticker_date in field_ticker_by_score.keys():
                ticker,date=ticker_date.split()[0],ticker_date.split()[1]
                data=data_by_date[date]
                #for ticker in data.Xtickers.keys():
                print(ticker)
                new=data.news[ticker]
                beta_=-1
                try:
                    beta_=data.beta[ticker]
                except: beta_=0
                print(new)
                title,body=getContent(new)
                if len(body)>0:
                        tic.append(ticker_date)
                        score.append(field_ticker_by_score[ticker_date][0])
                        tit.append(title)
                        b.append(body)
                        betaList.append(beta_)
                if k!='go': k=input()
                print("Score-> ",field_ticker_by_score[ticker_date][0])
                print("Beta-> ",beta_)
                #if beta_ != 0: k=input("\n--------------------------------------")
            print("Number total of url",len(b))
            #print("ticker-> ",tic,"   Score-> ",score,"  Title-> ",tit," Body-> ",b)
            k=input(field_ticker_by_score[ticker_date])
            saveFile(tic,score,tit,b)
            #k=input()
        else:
            print("Reading...")
            tic,score,tit,b=readFile()
            keywords.go(tit,score)
            return(tic,score,tit,b)
        print(len(tic),len(score),len(tit),len(b))
      

        
                
        k=input()
        ###############################################################
        email={'ticker':tic,'title':tit,'body':b}
        email_df = pd.DataFrame(email)# just as an array of dict, like a table structure in the db
        vect = TfidfVectorizer(stop_words='english', max_df=0.9, min_df=3)
        X = vect.fit_transform(email_df.body)
        print(type(X))
        print(X)
        k=input()
        X_dense = X.todense()
        print(type(X_dense))
        print(X_dense[:25])
        k=input()
        coords = PCA(n_components=2).fit_transform(X_dense)
        plt.scatter(coords[:, 0], coords[:, 1], c='m')
        plt.show()
        #k=input()
        features = vect.get_feature_names()
        print (top_feats_in_doc(X, features, 1, 50))
        print (top_mean_feats(X, features, top_n=50))

        n_clusters = 3
        clf = KMeans(n_clusters=n_clusters, 
                max_iter=100, 
                init='k-means++', 
                n_init=1)
        labels = clf.fit_predict(X)

        # For larger datasets use mini-batch KMeans, so we dont have to read all data into memory.
        # batch_size = 500
        # clf = MiniBatchKMeans(n_clusters=n_clusters, init_size=1000, batch_size=batch_size, max_iter=100)  
        # clf.fit(X)

        # Let's plot this with matplotlib to visualize it.
        # First we need to make 2D coordinates from the sparse matrix.
        X_dense = X.todense()
        pca = PCA(n_components=2).fit(X_dense)
        coords = pca.transform(X_dense)

        # Lets plot it again, but this time we add some color to it.
        # This array needs to be at least the length of the n_clusters.
        label_colors = ["#2AB0E9", "#2BAF74", "#D7665E", "#CCCCCC", 
                    "#D2CA0D", "#522A64", "#A3DB05", "#FC6514"]
        colors = [label_colors[i] for i in labels]

        plt.scatter(coords[:, 0], coords[:, 1], c=colors)
        plt.show()
        # Plot the cluster centers
        centroids = clf.cluster_centers_
        centroid_coords = pca.transform(centroids)
        plt.scatter(centroid_coords[:, 0], centroid_coords[:, 1], marker='X', s=200, linewidths=2, c='#444d60')
        plt.show()

        #Use this to print the top terms per cluster with matplotlib.
        plot_tfidf_classfeats_h(top_feats_per_cluster(X, labels, features, 0.1, 25))

        """t1=open("info (2).csv","r").read()
        t2=open("info (3).csv","r").read()
        print(len(t1))
        print(len(t2))
        """
#field_ticker_by_score,data_by_date=reporting.main(month=[1,2,3],year=2018)
field_ticker_by_score,data_by_date="",""
tic,score,tit,b=main(field_ticker_by_score,data_by_date)

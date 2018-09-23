import re
import time
import datetime


class TICKER():
    def __init__(self,name):
        self.name=name
        self.volume=0
        self.beta=0
        self.opening=0
        self.previous_close_price=0
        self.previous_close_time=0
        self.lowest_price=0
        self.url=""
        self.title=""
        self.good=0
        self.best=0
        self.bad=0
        self.percentage=0

    def setVolume(self,volume):
        self.volume=volume
        
    def setBeta(self,beta):
        self.beta=beta
        
    def setOpening(self,opening):
        self.opening=opening
        
    def setPrevious_close_price(self,previous_close_price):
        self.previous_close_price=previous_close_price
        
    def setPrevious_close_time(self,previous_close_time):
        self.previous_close_time=previous_close_time
        
    def setLowest_price(self,lowest_price):
        self.lowest_price=lowest_price
        
    def setUrl(self,url):
        self.url=url
        
    def setTitle(self,title):
        self.title=self.title
        
    def setBest(self):
        self.best=self.best+1
        
    def setGood(self):
        self.good=self.good+1
        
    def setBad(self):
        self.bad=self.bad+1

    def setPercentage(self):
        self.percentage = 100*(self.good+self.best)/(self.good+self.best+self.bad)


    def getBest(self):
        return self.best

    def getGood(self):
        return self.good

    def getBad(self):
        return self.bad

    def getName(self):
        return self.name

    def getPercentage(self):
        return self.percentage

    def __str__(self):
        return "< Name >"+self.name+" Best "+str(self.best)+" Good "+str(self.good)+" Bad "+str(self.bad)+" Percentage  "+str(self.percentage)

    
def split_words(all_words,tit,score,betaList):
    print(len(betaList))
    for count, each_title in enumerate(tit):
        k=input(each_title)
        print("Reading ...", count+1,"//",len(tit))
        each_title=re.sub(r'[^\w\s]',' ',each_title)
        each_word_list=each_title.lower().split()

        for each_word in each_word_list:
            if len(each_word)<=3:
                continue
            else:
                if each_word not in all_words:
                    EACH_KEYWORD=KEYWORD(each_word)
                else: EACH_KEYWORD=all_words[each_word]

                if  score[count]=="A":
                    EACH_KEYWORD.setBest()
                if  score[count]=="C":
                    EACH_KEYWORD.setGood()
                if  score[count]=="F":
                    EACH_KEYWORD.setBad()

                EACH_KEYWORD.setPercentage(	)

                #if EACH_KEYWORD.getName() not in all_words: 
                     #all_words[EACH_KEYWORD.getName()]=[]
                all_words[EACH_KEYWORD.getName()]=EACH_KEYWORD
                
def save_data(all_words):
    print("Saving ...")
    f=open("keyword_"+str(time.strftime("%m-%d-%Y_%H-%M-%S"))+".csv","w")
    f_100=open("keyword_100_"+str(time.strftime("%m-%d-%Y_%H-%M-%S"))+".csv","w")
    print(len(all_words))
    f.write("KEYWORDS"+", BEST"+",GOOD"+",BAD"+",EACH WORD %%\n")
    f_100.write("KEYWORDS 100"+", BEST"+",GOOD"+",BAD"+",EACH WORD %%\n")
    for word,EACH_KEYWORD in all_words.items():
        #print(word,EACH_KEYWORD.getBest(),EACH_KEYWORD.getGood(),EACH_KEYWORD.getBad(),"---------------> ",str(EACH_KEYWORD.getPercentage()).zfill(5))
        f.write(word+","+str(EACH_KEYWORD.getBest())+","+str(EACH_KEYWORD.getGood())+","+str(EACH_KEYWORD.getBad())+","+str(EACH_KEYWORD.getPercentage()).zfill(5)+"\n")
        if EACH_KEYWORD.getGood()+EACH_KEYWORD.getBad()>=100 :f_100.write(word+","+str(EACH_KEYWORD.getBest())+","+str(EACH_KEYWORD.getGood())+","+str(EACH_KEYWORD.getBad())+","+str(EACH_KEYWORD.getPercentage()).zfill(5)+"\n")
    f.close
    f_100.close
    print("Saving Done...")
    

def display(all_words):
    for word,EACH_KEYWORD in all_words.items():
         if EACH_KEYWORD.getBest()+EACH_KEYWORD.getGood()+EACH_KEYWORD.getBad()>100 and EACH_KEYWORD.getPercentage()>0:
               print(word,EACH_KEYWORD.getBest(),EACH_KEYWORD.getGood(),EACH_KEYWORD.getBad(),"---------------> ",str(EACH_KEYWORD.getPercentage()).zfill(5))
    k=input("Displaying done...")
def go(tit,score,betaList):
    all_words={}
    split_words(all_words,tit,score,betaList)
    save_data(all_words)
    display(all_words)

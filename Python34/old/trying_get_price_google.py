import requests
import time
import re

def delete_script_content(detail_page):
        count_script=detail_page.count("</script>")
        #k=input(count_script)
        while(count_script>0):
                pos1=detail_page.find("<script")
                pos2=detail_page.find("</script>")
                detail_page=detail_page[:pos1]+detail_page[pos2+9:]
                count_script=detail_page.count("</script>")
        return detail_page

#Ticker - Volume - Avg. Volume -  Previous Close  - Open - Market Cap - PE Ratio - Forward Dividend 
def get_info(ticker="DKS",info="Volume",display=False):
        url="https://finance.yahoo.com/quote/"+ticker+"?p="+ticker
        if display:
                print (url)
        
        g_page,g_txt="",""
        try:
                g_page = requests.get(url)
                g_txt = g_page.text
        except:print("Counldn't reach %s"%url)

        g_txt=delete_script_content(g_txt)

        position=g_txt.find(info)
        if position>=0:
                calibrator=200
                result=[]
                if display: print(g_txt[position:position+200])
                if info in ["Avg. Volume", "Volume"]:
                        result=re.findall('\d+,\d+',g_txt[position:position+200],re.DOTALL)
                        if result ==[]:result=re.findall('\d+,\d+,\d+',g_txt[position:position+200],re.DOTALL)
                        result = max(result) if len(result)>1  else result[0]
                if info in ["Previous Close", "Open","PE Ratio"]:
                        result=re.findall('\d+.\d+',g_txt[position:position+200],re.DOTALL)
                        result = max(result) if len(result)>1  else result[0]
                if info in ["Forward Dividend"]:
                        result=re.findall('(\d+.\d+)%',g_txt[position:position+200],re.DOTALL)
                        result+=re.findall('>N/A\D',g_txt[position:position+200],re.DOTALL)
                        result = max(result) if len(result)>1  else result[0]
                        result +="%"
                if info in ["Market Cap"]:
                        #print(info in ["Market Cap"])
                        result=re.findall('>(\d+.\d+\D)<',g_txt[position:position+200],re.DOTALL)
                        if display: print (result)
                        if  isinstance(result,list): result = max(result) if len(result)>1  else result[0]
                        
                        #result=re.findall('\d+,\d+,\d+',g_txt[position:position+200],re.DOTALL)
                #result = max(result) if len(result)>1  else result[0]
                print(info,"-> ",result)
                return (result)
                
        return(-1)

def price_yahoo_parsing(ticker="DKS",display=False):
        if display: print("Ticker -> ",ticker)# Printing the ticker name
        hours=time.strftime("%I")#Here the hour will display as 01 not 13
        hours=int(hours)-0#instead of having and extra 0 as 01, we concert in int ->1
        mins=int(time.strftime("%M"))-1# we want one minutes before the actual time, sometimes yahoo is behind
        time_last_second=str(hours)+":"+str(mins).zfill(2)# the min always have 2 digits: 01

        # here is for the actual time
        hours=time.strftime("%I")
        hours=int(hours)-0
        mins=int(time.strftime("%M"))-0
        time_now=str(hours)+":"+str(mins).zfill(2)

        
        if display: print(time_last_second,time_now)
        url="https://finance.yahoo.com/quote/"+ticker+"?p="+ticker
        if display: print (url)
        g_page,g_txt="",""
        try:
                g_page = requests.get(url)
                g_txt = g_page.text
        except:print("Counldn't reach %s"%url)

        g_txt=delete_script_content(g_txt)
        website_time,position="None",-1
        
        if g_txt.find(time_last_second)>=0 and (g_txt[g_txt.find(time_last_second)-20:g_txt.find(time_last_second)+20].find("Market open")>=0 or g_txt[g_txt.find(time_last_second)-20:g_txt.find(time_last_second)+20].find("At close:")>=0):# if the time with a mins less ins found
                website_time,position=(time_last_second,g_txt.find(time_last_second))#assign the time and its position
        elif g_txt.find(time_now)>=0 and (g_txt[g_txt.find(time_now)-20:g_txt.find(time_now)+20].find("Market open")>=0 or g_txt[g_txt.find(time_now)-20:g_txt.find(time_now)+20].find("At close:")>=0):# if the actula time is  found
                website_time,position=(time_now,g_txt.find(time_now))
        elif g_txt.find("Market open")>=0:website_time,position=(time_now,g_txt.find("Market open"))
        elif g_txt.find("At close:")>=0:website_time,position=(time_now,g_txt.find("At close:"))
        elif g_txt.find("After hours:")>=0:website_time,position=(time_now,g_txt.find("After hours:"))
        else: print("Neither time has been found")
                        
                
        if display: print(website_time,position)

        #print(g_txt[position-10:position+10])
        
        if position>=0:
                calibrator=700
                result=re.findall('>(\d+.\d+)<',g_txt[position-calibrator:position],re.DOTALL)
                if display: print(result)
                result = max(result) if len(result)>1  else result[0]
                if display: print(result)
                #print(g_txt[position-calibrator:position])
                #k=input("-----------")
                #sentense_having_price=g_txt[position-calibrator:position]
                #beginning=sentense_having_price.find("-->")+len("-->")
                #end=(sentense_having_price[beginning:].find("<!--"))+beginning
                #print(sentense_having_price[beginning:end],"  ===========  ",website_time)
                return (result,website_time)
                
        return("No Value",-1)
while(1):
        print("="*15,"   ",time.strftime("%b %d, %Y---%H:%M:%S "))
        start=time.time()
        ticker="HCM"
        print(ticker)
        get_info(ticker,'Previous Close')
        get_info(ticker,'Open')
        get_info(ticker,'Volume')
        get_info(ticker,'Avg. Volume')
        get_info(ticker,'Market Cap')
        get_info(ticker,'PE Ratio')
        get_info(ticker,'Forward Dividend')
        print("Price -> ",price_yahoo_parsing(ticker=ticker)[0])
        #price_yahoo_parsing()
        #result=(list(map(price_yahoo_parsing,["GSAT","ANY"])))
        end=time.time()
        print("Sleeping for -> ",60-(end-start))
        sleep_time=60-(end-start)
        time.sleep(sleep_time if sleep_time>=0 else 0)

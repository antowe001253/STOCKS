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
def get_info(ticker="DKS",info="Volume",display=False,timeout=5,beginning_char='>'):
        #print("In get ticker info")
        if display: print(ticker)
        url="https://finance.yahoo.com/quote/"+ticker+"?p="+ticker
        if display:
                print (url)
        
        g_page,g_txt="",""
        try:
                g_page = requests.get(url,timeout=timeout)
                g_txt = g_page.text
        except: 
                if display: print("Counldn't reach %s"%url)

        g_txt=delete_script_content(g_txt)

        position=g_txt.find(info)
        if position>=0:
                calibrator=300
                result=[]
                if display: print(g_txt[position:position+calibrator])
                if info in ["Avg. Volume", "Volume"]:
                    #print("*"*25,re.findall('>(\d+)<',g_txt[position:position+calibrator],re.DOTALL))
                    result=re.findall(beginning_char+'(\d+,\d+,\d+)',g_txt[position:position+calibrator],re.DOTALL)
                    if display: print("case 1 >(\d+,\d+,\d+)",result)
                    if result ==[]:
                        result=re.findall(beginning_char+'(\d+,\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        if display: print("case 2  "+beginning_char+"(\d+,\d+)",result)
                    if result ==[]:
                        result=re.findall(beginning_char+'(\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        if display: print("case 3  "+beginning_char+"(\d+)",result)
                    if result ==[] :result=re.findall('>N/A',g_txt[position:position+calibrator],re.DOTALL)
                    try: result = max(result) if len(result)>1  else result[0]
                    except:
                        print("Can't find Volume ",ticker)
                        print("-------------result-> ",result)
                        print(g_txt[position-20:position+20])
                        print(g_txt[position:position+calibrator],re.DOTALL)
                        result=-1
                        #k=input()
						#assert 1==2,"********************************"
                if info in ["Previous Close", "OPEN-value","PE Ratio","Beta"]:
                        result=re.findall(beginning_char+'(\W?\d+.?\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        #if result ==[] :result=re.findall('-->(\W?\d+.\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        #if result ==[] :result=re.findall('-->(\W?\d+.?\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        #if result ==[] :result=re.findall('-->(\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        #if result ==[] :result=re.findall('-->(\W?\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        #if result ==[] :result=re.findall('-->(\d+.\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        #if result ==[] :result=re.findall('-->-(\d+.\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        result+=re.findall('>N/A\D',g_txt[position:position+calibrator],re.DOTALL)
                        try: result = max(result) if len(result)>1  else result[0]
                        except:
                            print("Can't find %s "%info,ticker)
                            print("-------------result-> ",result)
                            print(g_txt[position-20:position+20])
                            print(g_txt[position:position+calibrator],re.DOTALL)
                            result=-5
                            #k=input()
							#assert 1==2,"********************************"
                        
                if info in ["Forward Dividend"]:
                        result=re.findall(beginning_char+'(\d+.\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        if result ==[] : result=re.findall(beginning_char+'(\d+)',g_txt[position:position+calibrator],re.DOTALL)
                        if result ==[] :result=re.findall('>N/A\D',g_txt[position:position+calibrator],re.DOTALL)
                        try: result = max(result) if len(result)>1  else result[0]
                        except:
                                
                            print("Can't find Forward Dividend ",ticker)
                            print("-------------result-> ",result)
                            print(g_txt[position-20:position+20])
                            print(g_txt[position:position+calibrator],re.DOTALL)
                            result=-1
                            #k=input()
						#assert 1==2,"********************************"
                        
                        result +="%"
                if info in ["Market Cap"]:
                        #print(info in ["Market Cap"])
                        result=re.findall(beginning_char+'(\d+.\d+\D)',g_txt[position:position+calibrator],re.DOTALL)
                        if result ==[] :result=re.findall(beginning_char+'(\d+\D)',g_txt[position:position+calibrator],re.DOTALL)
                        result+=re.findall('>N/A\D',g_txt[position:position+calibrator],re.DOTALL)
                        if display: print (result)
                        try: 
	                        if  isinstance(result,list): result = max(result) if len(result)>1  else result[0]
                        except:
                            print("Can't find Market Cap ",ticker)
                            print("-------------result-> ",result)
                            print(g_txt[position-20:position+20])
                            print(g_txt[position:position+calibrator],re.DOTALL)
                            result=-1
                            #k=input()
						     #assert 1==2,"********************************"
                        #result=re.findall('\d+,\d+,\d+',g_txt[position:position+calibrator],re.DOTALL)
                #result = max(result) if len(result)>1  else result[0]
                if display: print("="*25,info,"-> ",result)
                #print("Out get ticker info")
                if isinstance(result,str):
                    if result.find("N/A")>=0: return -1
                    else: return (result)
                else: return (result)
                
        #print("Out get ticker info")
        return(-1)

def price_yahoo_parsing(ticker="DKS",display=False,beginning_char='>'):
        #print("In get price_yahoo_parsing")
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
                g_page = requests.get(url,timeout=5)
                g_txt = g_page.text
        except: """print("Counldn't reach %s"%url)"""

        g_txt=delete_script_content(g_txt)
        website_time,position="None",-1
        ketword=""
        if g_txt.find(time_last_second)>=0 and (g_txt[g_txt.find(time_last_second)-20:g_txt.find(time_last_second)+20].find("Market open")>=0 or g_txt[g_txt.find(time_last_second)-20:g_txt.find(time_last_second)+20].find("At close:")>=0):# if the time with a mins less ins found
                website_time,position=(time_last_second,g_txt.find(time_last_second))#assign the time and its position
                ketword=time_last_second
        elif g_txt.find(time_now)>=0 and (g_txt[g_txt.find(time_now)-20:g_txt.find(time_now)+20].find("Market open")>=0 or g_txt[g_txt.find(time_now)-20:g_txt.find(time_now)+20].find("At close:")>=0):# if the actula time is  found
                website_time,position=(time_now,g_txt.find(time_now))
                ketword=time_now
        elif g_txt.find("Market open")>=0:
                website_time,position=(time_now,g_txt.find("Market open"))
                ketword="Market open"
        elif g_txt.find("At close:")>=0:
                website_time,position=(time_now,g_txt.find("At close:"))
                ketword="At close:"
        elif g_txt.find("After hours:")>=0:
                website_time,position=(time_now,g_txt.find("After hours:"))
                ketword="After hours:"
        else:
                """print("Neither time has been found -> ",ticker)"""
                ketword="None"
                        
                
        if display: print(website_time,position)

        #print(g_txt[position-10:position+10])
        
        if position>=0:
                calibrator=700
                result=re.findall(beginning_char+'(\d+.\d+)',g_txt[position-calibrator:position],re.DOTALL)
                if display: print(result)
                try:
                        result = max(result) if len(result)>1  else result[0]
                except:
                        print("Can't find",ticker)
                        print("-------------ketword-> ",ketword)
                        print(g_txt[position-20:position+20])
                        print(g_txt[position-calibrator:position],re.DOTALL)
                        result=-1
                        #k=input()
                        #assert 1==2,"********************************"
                if display: print(result)
                #print(g_txt[position-calibrator:position])
                #k=input("-----------")
                #sentense_having_price=g_txt[position-calibrator:position]
                #beginning=sentense_having_price.find("-->")+len("-->")
                #end=(sentense_having_price[beginning:].find("<!--"))+beginning
                #print(sentense_having_price[beginning:end],"  ===========  ",website_time)
                #print("Out get ticker info")
                try:
                     result=float(result)
                except:
                      print("Error ",ticker)
                      print("-------------ketword-> ",ketword)
                      print(g_txt[position-20:position+20])
                      print(g_txt[position-calibrator:position],re.DOTALL)
                      result=-1
                      
                return (float(result),time.strftime("%H:%M:%S"))
        #print("Out get price_yahoo_parsing")        
        return("None",time.strftime("%H:%M:%S"))

#get_info()

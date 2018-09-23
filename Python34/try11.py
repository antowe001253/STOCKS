from get_ticker_info import *
import re

tickers=["CNAT","MAR","DRYS"]
results=[]
for each in tickers:
    k=get_info(ticker=each,info="Beta",display=True)
    results.append(k)


g_txt="""- react-text: 36 -->0.0037<!-- /react-text --></span><span class="Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)" data-reactid="37"><!-- react-text: 38 -->0.0000 (0.0000%)<!-- /react-text --></span><div id="quote-market-notice" class="C($c-fuji-grey-j) D(b) Fz(12px) Fw(n)" data-reactid="39"><span data-reactid="40">As of  1:51PM EST. Market open"""
result=re.findall('>(\d+.\d+)<',g_txt,re.DOTALL)
print(results)

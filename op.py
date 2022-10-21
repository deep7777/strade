from nsepython import *
from datetime import date
from nsepy import get_history
from nsepy.history import get_price_list

import yfinance as yf
import numpy as np
import pandas as pd
import array

#define the ticker symbol
stock_info = yf.Ticker('SBIN.NS').info
# stock_info.keys() for other properties you can explore
market_price = stock_info['regularMarketPrice']
print('market price ', market_price)


option_type = 'CE'
symbol="SBIN"
strikeprices = range(500,600,5)
def row_print(option_type,row,rclose,rhigh,hval,lval,per,rtype):
    print(option_type,' ',row.name,'    ',row['Strike Price'], ' cl = ',rclose, ' rhigh= ', rhigh,'  ',' hval= ', hval, ' lval= ', lval, ' %%= ',per, rtype)

for sp in strikeprices:
    mt = 10
    expiry = 27
    start = date(2022,mt,1)
    end = date(2022,10,20)
    expiry_date = date(2022,10,27)
    print(sp)
    nifty_opt = get_history(symbol=symbol,
                            start=start,
                            end=end,
                            index=False,
                            option_type=option_type,
                            strike_price=sp,
                            expiry_date=expiry_date)
    df = pd.DataFrame(nifty_opt)
    h=[]
    l=[]
    i=0
    length = len(df.index)
    print("#################### start ############################",symbol)
    for index, row in df.iterrows():
        i = i+1
        name = row.name
        ropen = row.Open
        rhigh = row.High 
        rclose = row.Close
        rlow = row.Low
        rohdiff = rhigh - ropen
        roldiff = ropen - rlow
        l.append(rlow)
        h.append(rhigh)
        hval = max(h)
        lval = min(l)
        per = 0
        rohdiff = rhigh - ropen
        roldiff = ropen - rlow
        if(rohdiff == 0):
            print('\033c')
            print(sp,' ',name,' ', ropen,rhigh,' sell the option=', ' rlow= ', rlow, ' rclose= ', rclose, rohdiff, '=>', expiry_date)
        if(roldiff == 0):
            print('\033c')
            print(sp,' ',name,' ropen= ',ropen,' buy the option', ' rhigh= ',rhigh, ' rclose= ',rclose, roldiff, '=>', expiry_date, sp)

        # if lval !=0:
        #     per = (hval/lval)*10
        # if per > 80 and option_type == 'CE' and rhigh == hval:
        #    row_print(option_type,row,rclose,rhigh,hval,lval,per,'STEP1')
        #    print(row.name,'    ',"!!!!!!!!!!!!!!!!!!!!!!!! ALERT !!!!!!!!!!!!!!") 
        # elif per > 80 and option_type == 'PE' and rlow == lval:   
        #    row_print(option_type,row,rclose,rhigh,hval,lval,per,'STEP1')
        #    print(row.name,'    ',"!!!!!!!!!!!!!!!!!!!!!!!! ALERT !!!!!!!!!!!!!!") 
        # elif(i==length):
        #    row_print(option_type,row,rclose,rhigh,hval,lval,per,'STEP2')
        #    print("#################### end ############################")
        # else:
        #     print(row.name,'    ',row['Strike Price'],'  ',' cl = ',rclose, ' rhigh= ', rhigh,'  ', '  hval= ',hval, ' lval= ', lval, ' ',' % ',per,'   =    ',row['Change in OI'])
        #     print("$@$2$@$2$2$@")
                


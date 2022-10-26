from nsepython import *
from datetime import date
from nsepy import get_history
from nsepy.history import get_price_list

import numpy as np
import pandas as pd
import array

option_type = 'CE'
strikeprices = range(17000,18100,100)
def row_print(option_type,row,rclose,rhigh,hval,lval,per,rtype):
    print(option_type,' ',row.name,'    ',row['Strike Price'], ' cl = ',rclose, ' rhigh= ', rhigh,'  ',' hval= ', hval, ' lval= ', lval, ' %%= ',per, rtype)

for sp in strikeprices:
    mt = 10
    expiry = 27
    day = date.today().strftime('%d');
    print(day,'###')
    start = date(2022,10,20)
    end = date(2022,10,int(day))
    expiry_date = date(2022,10,27)
    nifty_opt = get_history(symbol="NIFTY",
                            start=start,
                            end=end,
                            index=True,
                            option_type=option_type,
                            strike_price=sp,
                            expiry_date=expiry_date)
    df = pd.DataFrame(nifty_opt)
    h=[]
    l=[]
    i=0
    length = len(df.index)
    print(sp, "#################### start ############################")
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
        if lval !=0:
            per = (hval/lval)*10
        if per > 80 and option_type == 'CE' and rhigh == hval:
           row_print(option_type,row,rclose,rhigh,hval,lval,per,'STEP1')
           print(row.name,'    ',"!!!!!!!!!!!!!!!!!!!!!!!! ALERT !!!!!!!!!!!!!!") 
        elif per > 80 and option_type == 'PE' and rlow == lval:   
           row_print(option_type,row,rclose,rhigh,hval,lval,per,'STEP1')
           print(row.name,'    ',"!!!!!!!!!!!!!!!!!!!!!!!! ALERT !!!!!!!!!!!!!!") 
        elif(i==length):
           row_print(option_type,row,rclose,rhigh,hval,lval,per,'STEP2')
           print("#################### end ############################")
        else:
            print(row.name,'    ',row['Strike Price'],'  ',' cl = ',rclose, ' rhigh= ', rhigh,'  ', '  hval= ',hval, ' lval= ', lval, ' ',' % ',per,'   =    ',row['Change in OI'])
            print("$@$2$@$2$2$@")
        
 


        


from nsepython import *
from datetime import date
from nsepy import get_history
from nsepy.history import get_price_list

import numpy as np
import pandas as pd
import array
import csv

#option_type = 'CE'
options = ['PE','CE']
yr = int(sys.argv[1])
arg_start_month = int(sys.argv[2])
arg_start_date = int(sys.argv[3])
arg_end_month = int(sys.argv[4])
arg_end_date = int(sys.argv[5])
arg_expiry_month =int(sys.argv[6])
arg_expiry_date = int(sys.argv[7])
symbol =(sys.argv[8])

ss = int(sys.argv[9])      #strikeprice start
se = int(sys.argv[10])       #strikeprice end
ticks = int(sys.argv[11])       #strkeprice ticks
asp = {}
prev_day_ce_vol={}
prev_day_pe_vol={}
store_ce = {}
store_pe = {}

filename = 'all/'+sys.argv[12]
f = open(filename, 'w')
writer = csv.writer(f)
header = 'Type','Date','StrikePrice','Open','High','Low','Close','Vol/Prev','CE/PE','OI','COI','Volume'
print(header)
writer.writerow(header)
            
for o in options:
    option_type = o
    strikeprices = range(ss,se,ticks)
    def row_print(option_type,row,rclose,rhigh,hval,lval,per,rtype,oi,coi,vol):
        print(option_type,' ',row.name,'    ',row['Strike Price'], ' cl = ',rclose, ' rhigh= ', rhigh,'  ',' hval= ', hval, ' lval= ', lval, ' %%= ',per, rtype,oi,coi,vol)
    for sp in strikeprices:
        mt = 10
        expiry = 27
        day = date.today().strftime('%d');
        #print(day,'###')
        start = date(yr,arg_start_month,arg_start_date)
        end = date(yr,arg_end_month,arg_end_date)#int(day)
        expiry_date = date(yr,arg_expiry_month,arg_expiry_date)
        nifty_opt = get_history(symbol=symbol,
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
        prev = 0
        for index, row in df.iterrows():
            i = i+1
            name = row.name
            strikeprice = round(row['Strike Price'])
            ropen = row.Open
            rhigh = row.High 
            rclose = row.Close
            rlow = row.Low
            rohdiff = rhigh - ropen
            roldiff = ropen - rlow
            oi = row['Open Interest']
            coi = row['Change in OI']
            vol = row['Number of Contracts']
            l.append(rlow)
            h.append(rhigh)
            hval = max(h)
            lval = min(l)
            per = 0
            osp = option_type,' ',row.name,'    ',row['Strike Price'],'  ',' open = ',ropen,' cl = ',rclose, ' rhigh= ', rhigh,'  ', '  hval= ',hval, ' lval= ', lval, ' ',' % ',per,'   =    ',row['Change in OI']
            dt = row.name.strftime('%d%m%y');
            key = str(row['Strike Price'])+'_'+option_type+'_'+str(dt)
            asp[key] = vol
            if(option_type=="CE"):
                pe_key = str(row['Strike Price'])+'_PE'+'_'+str(dt)
                if(asp[key]!=0):
                    cal = asp[key]/asp[pe_key]
                    today = 0;
                    if(prev>0):
                        today = vol/prev
                        today = round(today,2)

                    store_ce[strikeprice] =  {
                        option_type:option_type,
                        date:row.name,
                        strikeprice:row['Strike Price'],
                        ropen:ropen,
                        rhigh:rhigh,
                        rlow:rlow,
                        rclose:rclose,
                        'todayvol':today,
                        cal:cal,
                        oi:oi,
                        coi:coi,
                        vol:vol  
                    }
                    if(option_type=='CE'):
                        prev = vol
                        prev_day_ce_vol[strikeprice]=vol

            elif(option_type=="PE"):
                today = 0;  cal='NA'              
                if(prev>0):
                    today = vol/prev
                    today = round(today,2)                
                store_pe[strikeprice] =  {
                    option_type:option_type,
                    date:row.name,
                    strikeprice:row['Strike Price'],
                    ropen:ropen,
                    rhigh:rhigh,
                    rlow:rlow,
                    rclose:rclose,
                    'todayvol':round(today,2),
                    cal:cal,
                    oi:oi,
                    coi:coi,
                    vol:vol  
                }
                prev = vol    
                prev_day_pe_vol[strikeprice] = vol
            print(option_type,row.name,row['Strike Price'],ropen,rhigh,rlow,rclose,'\033[33m*',today,'*\033[0m ',cal,oi,coi,vol) 
            # open the file in the write mode
            # create the csv writer
            rowline = option_type,row.name,row['Strike Price'],ropen,rhigh,rlow,rclose,today,cal,oi,coi,vol
            writer.writerow(rowline)          
f.close()       

def checkKey(dic, key):
    if key in dic:
        return True
    else:
        return False

def getToday():
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol='+symbol
    print(url)
    indices = nsefetch(url)
    data = indices['filtered']['data']
    ratios = {};
    for x in prev_day_ce_vol:
        print(x,prev_day_ce_vol[x])
        ratios[x] = prev_day_ce_vol[x]/prev_day_pe_vol[x]

    print(prev_day_ce_vol,'CE')
    print(prev_day_pe_vol,'PE')
    print(ratios,'CE/PE')

    print('CE','strikeprice','prevdayvol','vol','vol/prevday', '...','totalVolume', '  ','last_price')
    for x in data:
        sp = round(x['strikePrice'])
        if(x['strikePrice']>=ss  and checkKey(prev_day_ce_vol,sp)):
                vol = x['CE']['totalTradedVolume']
                totalVolume = int(vol)*50
                vol_check_ce = vol/prev_day_ce_vol[sp]
                last_price = x['CE']['lastPrice']
                print('CE',sp,prev_day_ce_vol[sp],vol,vol_check_ce, '...',totalVolume, '  ',last_price)

                vol = x['PE']['totalTradedVolume']
                vol_check_pe = vol/prev_day_pe_vol[sp]
                last_price = x['PE']['lastPrice']
                totalVolume = int(vol)*50
                print('PE',sp,prev_day_pe_vol[sp],vol,vol_check_pe, '...',totalVolume, '   ',last_price)
                if(vol_check_pe!=0):
                    print('CE/PE= ',vol_check_ce/vol_check_pe)
                print('        ')

getToday()

            # if lval !=0:
            #     per = (hval/lval)*10
            # if per > 80 and option_type == 'CE' and rhigh == hval:
            #    row_print(option_type,row,rclose,rhigh,hval,lval,per,oi,coi,vol,'STEP1')
            #    print(row.name,'    ',"!!!!!!!!!!!!!!!!!!!!!!!! ALERT !!!!!!!!!!!!!!") 
            # elif per > 80 and option_type == 'PE' and rlow == lval:   
            #    row_print(option_type,row,rclose,rhigh,hval,lval,per,vol,'STEP1')
            #    print(row.name,'    ',"!!!!!!!!!!!!!!!!!!!!!!!! ALERT !!!!!!!!!!!!!!") 
            # elif(i==length):
            #    row_print(option_type,row,rclose,rhigh,hval,lval,per,oi,coi,vol,'STEP2')
            #    print("                   end                   ")
            # else:
            #     #print(option_type,' ',row.name,'    ',row['Strike Price'],'  ',' open = ',ropen,' cl = ',rclose, ' rhigh= ', rhigh,'  ', '  hval= ',hval, ' lval= ', lval, ' ',' % ',per,'   =    ',row['Change in OI'])
            #     print(row.name,'    ',row['Strike Price'],"$@$2$@$2$2$@",'    ',row.name,'    ',ropen,'    ',rhigh,'    ',rlow,'    ',rclose,'   ',oi,'   ',coi, vol)
 

# {
# Name: 2022-10-27, dtype: object
# 2022-10-27      18000.0 $@$2$@$2$2$@      2022-10-27      300.0      359.2      200.0      295.2     500400     344550
# Symbol                          NIFTY
# Expiry                     2022-11-03
# Option Type                        PE
# Strike Price                  18000.0
# Open                            275.6
# High                            298.0
# Low                             221.2
# Close                          253.55
# Last                            247.0
# Settle Price                   253.55
# Number of Contracts            208627
# Turnover               190443344000.0
# Premium Turnover         2679044000.0
# Open Interest                  589750
# Change in OI                    89350
# Underlying                    17786.8
# }


# how to run this program for index and stocks

# python strikes.py yr stmth stdate emth edate expirymonth expirydate  NIFTY strikepricestart strikepriceend ticks file
# python strikes.py 2022 10 27 11 2 11 24  NIFTY 17000 19000 500 nov.csv



# 1 6 13 20 27  jan 
# 2 9 16 23     feb
# 3 10 17 24 31 mar
# 7 14 21 28    april
# 5 12 19 26    may
# 2 9 16 23 30  june
# 7 14 21 28    july
# 4 11 18 25    aug 
# 1 8 15 22 29  sep 
# 6 13 20 27    oct
# 3 10 17 24    nov
# 1 8 15 22 29  dec

# 2022-01-06  17745.90 2022-01-13  18257.80 2022-01-20  17757.00 2022-01-27  17110.15

# 2022-02-03  17560.20 2022-02-10  17605.85 2022-02-17  17304.60 2022-02-24  16247.95

# 2022-03-03  16498.05 2022-03-10  16594.90 2022-03-17  17287.05 2022-03-24  17222.75 2022-03-31  17464.75

# 2022-04-07  17639.55 2022-04-21  17392.60 2022-04-28  17245.05

# 2022-05-05  16682.65 2022-05-12  15808.00 2022-05-19  15809.40 2022-05-26  16170.15

# 2022-06-02  16628.00 2022-06-09  16478.10 2022-06-16  15360.60 2022-06-23  15556.65 2022-06-30  15780.25

# 2022-07-07  16132.90 2022-07-14  15938.65 2022-07-21  16605.25 2022-07-28  16929.60

# 2022-08-04  17382.00 2022-08-11  17659.00 2022-08-18  17956.50 2022-08-25  17522.45

# 2022-09-01  17542.80 2022-09-08  17798.75 2022-09-15  17877.40 2022-09-22  17629.80 2022-09-29  16818.10

# 2022-10-06  17331.80 2022-10-13  17014.35 2022-10-20  17563.95 2022-10-27  17736.95


















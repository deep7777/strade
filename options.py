from nsepython import *
from datetime import date
from nsepy import get_history
from nsepy.history import get_price_list

import numpy as np
import pandas as pd
import array


strikeprices = [17000, 17100,17200,17300,17400,17500,17600,17700,17800,17900,18000]
for sp in strikeprices:
    mt = 9
    expiry = 27
    start = date(2022,mt,1)
    end = date(2022,10,19)
    expiry_date = date(2022,10,20)
    nifty_opt = get_history(symbol="NIFTY",
                            start=start,
                            end=end,
                            index=True,
                            option_type='CE',
                            strike_price=sp,
                            expiry_date=expiry_date)
    df = pd.DataFrame(nifty_opt)
    for index, row in df.iterrows():
        name = row.name
        ropen = row.Open
        rhigh = row.High 
        rclose = row.Close
        rlow = row.Low
        rohdiff = rhigh - ropen
        roldiff = ropen - rlow
        if(rohdiff == 0):
            print('\033c')
            print(ropen,rhigh,' ohdiff sell the option', rlow, rclose, rohdiff, '=>', name, expiry_date, sp)
        if(roldiff == 0):
            print('\033c')
            print(ropen,rlow,' oldiff buy the option', rhigh, rclose, roldiff, '=>', name, expiry_date, sp)



#print(nifty_opt)

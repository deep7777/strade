# import pandas lib as pd
from nsepython import *
import pandas as pd
import pymongo
import db
import numpy
myclient = db.getclient()
mydb = myclient["strade"]
mycol = mydb["niftyrecords"]

fetch = nsefetch('https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY')
df = pd.DataFrame(fetch)
print(df.records.underlyingValue) #records,data,expiryDates,strikePrices,underlyingValue,timestamp
print(df.filtered.data)
# for index, row in df.iterrows():
#     #print(row[0])
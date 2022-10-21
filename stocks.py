from nsepython import *
from datetime import date
from sqlalchemy import create_engine
from nsepy import get_history

import yfinance as yf
import plotly.graph_objs as go
import yfinance as yf
import mysql.connector
import numpy as np
import pandas as pd
import array
import matplotlib.pyplot as plot
import requests
import sys

# establishing the connection

conn = mysql.connector.connect(user='root', password='root',
                               host='127.0.0.1', database='deepak')
dateval = date.today().strftime('%Y-%m-%d');
print(dateval)
mt = date.today().strftime('%m');
day = date.today().strftime('%d');

start = date(2022,8,1)
end = date(2022,int(mt),int(day))
expiry_date = date(2022,10,27)


cursor = conn.cursor()

# Retrieving single row
sql = 'SELECT cname,csymbol,id,options from companies order by id asc limit 1'
# Executing the query
cursor.execute(sql)
# Fetching 1st row from the table

result = cursor.fetchall()

def getstock(name):
	nifty_opt = get_history(
						symbol='TECHM',
		                start=start,
		                end=end,
		                index=False
	                )
	df = pd.DataFrame(nifty_opt)
	print(df)
	# for index, row in df.iterrows():
	# 	print(row) 

for row in result:
    name = row[1]
    company = row[0]
    options = row[3]
    getstock(name)

   
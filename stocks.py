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
iday = int(day)
start = date(2022,int(mt),iday)
end = date(2022,int(mt),iday)
expiry_date = date(2022,10,27)


cursor = conn.cursor()


def insertStockData(dateval,symbol,series,prevclose,ropen,high,low,last,close,vwap,volume,turnover,trades,deliverablevolume,deliverable):
    insert_stmt = (
    	"INSERT INTO stockdata(dateval, symbol,series,prevclose,open,high,low,last,close,vwap,volume,turnover,trades,deliverablevolume,deliverable,dvlen)" 
    	"VALUES (%s, %s, %s,%s, %s,%s,%s,%s,%s,%s, %s, %s, %s,%s,%s,%s)"
    )
    dvlen = len(str(deliverablevolume))
    data = (dateval,symbol,series,prevclose,ropen,high,low,last,close,vwap,volume,turnover,trades,deliverablevolume,deliverable,dvlen)
    cursor.execute(insert_stmt,data)
    print(symbol,dvlen)
    conn.commit()


def getstock(name):
	nifty_opt = get_history(
						symbol=name,
		                start=start,
		                end=end,
		                index=False
	                )
	df = pd.DataFrame(nifty_opt)
	for index, row in df.iterrows():
		dateval=row.name
		symbol=row[0]
		series=row[1]
		prevclose=row[2]
		ropen=row[3]
		high=row[4]
		low=row[5]
		last=row[6]
		close=row[7]
		vwap=row[8]
		volume=row[9]
		turnover=row[10]
		trades=row[11]
		deliverablevolume=row[12]
		deliverable=row[13]
		insertStockData(dateval,symbol,series,prevclose,ropen,high,low,last,close,vwap,volume,turnover,trades,deliverablevolume,deliverable)

def findKalabazar():
	sql = "select dateval,symbol,volume,deliverablevolume,deliverable,close from stockdata where dvlen!=(select len from companies where csymbol=symbol) and dateval='"+dateval+"' order by deliverable desc"
	cursor.execute(sql)
	result = cursor.fetchall()
	for row in result:
		print(row[0],' symbol',row[1],' volume ',row[2],' deliverable ',row[3],' deliverable ',row[4], ' close ', row[5])

# Retrieving single row
sql = 'SELECT cname,csymbol,id,options from companies where options=1 order by id asc'
# Executing the query
cursor.execute(sql)
# Fetching 1st row from the table
result = cursor.fetchall()
for row in result:
    name = row[1]
    company = row[0]
    options = row[3]
    getstock(name)

findKalabazar()
    

   
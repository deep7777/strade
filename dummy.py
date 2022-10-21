from nsepython import *
from nsepy.history import get_price_list
from nsepy import get_history
from datetime import date

import mysql.connector




import mysql.connector
import numpy as np
import pandas as pd
import array

# Data Source

import yfinance as yf

# Data viz

import plotly.graph_objs as go
import yfinance as yf

# establishing the connection

conn = mysql.connector.connect(user='root', password='root',
                               host='127.0.0.1', database='deepak')

# Creating a cursor object using the cursor() method

cursor = conn.cursor()

# Retrieving single row

sql = 'SELECT cname,csymbol from companies limit 500'

# Executing the query

cursor.execute(sql)

# Fetching 1st row from the table

result = cursor.fetchone()
print(result)

# Fetching 1st row from the table

result = cursor.fetchall()
#print(result)
mycursor = conn.cursor()

def nse_custom_function_secfno(symbol,attribute="lastPrice"):
    positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
    endp = len(positions['data'])
    for x in range(0, endp):
        if(positions['data'][x]['symbol']==symbol.upper()):
            return positions['data'][x]

for row in result:
    cname = row[0]
    csymbol = row[1]
    name = row[1]
    cdate = "2022-10-03"
    print(name)
    #print(nse_custom_function_secfno(name))
    rowData = nse_custom_function_secfno(name)
    if(rowData.open==rowData.dayHigh):
      print('*****************************************High => Sell')
      print(rows, 'High => Sell')
      sql = "INSERT INTO intraday (cname, csymbol,type,cdate,open,high,low) VALUES (%s, %s, %s,%s,%s,%s,%s)"
      val = (cname, csymbol, "sell",cdate,rowData.Open,rowData.dayHigh,rowData.Low)
      mycursor.execute(sql, val)
      conn.commit()
    if(rowData.open==rowData.dayLow):
      print('*****************************************Low => Buy')
      print(rows, 'Low => Buy')
      sql = "INSERT INTO intraday (cname, csymbol,type,cdate,open,high,low) VALUES (%s, %s, %s,%s,%s,%s,%s)"
      val = (cname, csymbol, "buy",cdate,rowData.Open,rowData.High,rowData.Low)
      mycursor.execute(sql, val)
      conn.commit()

    # data = get_history(symbol=row[1],
    #                start=date(2022,10,3),
    #                end=date(2022,10,3))
    # df = pd.DataFrame(data)
    # for index, row in df.iterrows():
    #     print(row)
    #     rows = name,' ',index,' ',row.Open, row.High, row.Low, row.Close
    #     cdate = rows[2];
    #     if(row.Open==row.High):
    #       print('*****************************************High => Sell')
    #       print(rows, 'High => Sell')
    #       sql = "INSERT INTO intraday (cname, csymbol,type,cdate,open,high,low,close) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"
    #       val = (cname, csymbol, "sell",cdate,row.Open,row.High,row.Low,row.Close)
    #       mycursor.execute(sql, val)
    #       conn.commit()
    #     if(row.Open==row.Low):
    #       print('*****************************************Low => Buy')
    #       print(rows, 'Low => Buy')
    #       sql = "INSERT INTO intraday (cname, csymbol,type,cdate,open,high,low,close) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"
    #       val = (cname, csymbol, "buy",cdate,row.Open,row.High,row.Low,row.Close)
    #       mycursor.execute(sql, val)
    #       conn.commit()
    

# Closing the connection

conn.close()

from nsepython import *
from nsepy.history import get_price_list
from nsepy import get_history
from datetime import date
from nsetools import Nse


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

nse = Nse()
# establishing the connection

conn = mysql.connector.connect(user='root', password='root',
                               host='127.0.0.1', database='deepak')

# Creating a cursor object using the cursor() method

cursor = conn.cursor()

# Retrieving single row

sql = 'SELECT id,cname,csymbol from companies'

# Executing the query

cursor.execute(sql)

# Fetching 1st row from the table

result = cursor.fetchone()
print(result)

# Fetching 1st row from the table

result = cursor.fetchall()
#print(result)
mycursor = conn.cursor()

def nse_custom_function_secfno(symbol):
    return nse.get_quote(symbol)

for row in result:
    rowid = row[0]
    cname = row[1]
    csymbol = row[2]
    name = row[1]
    cdate = "2022-10-04"
    
    try:
        rowData = nse.get_quote(csymbol)
        print(rowData)
        if(rowData['open']):
            print(rowid) 
            print(name)
            if(rowData['open']==rowData['dayHigh']):
              print('*****************************************High => Sell')
              sql = "INSERT INTO intraday (cname, csymbol,type,cdate,open,high,low,close) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"
              val = (cname, csymbol, "sell",cdate,rowData['open'],rowData['dayHigh'],rowData['dayLow'],rowData['closePrice'])
              mycursor.execute(sql, val)
              conn.commit()
            if(rowData['open']==rowData['dayLow']):
              print('*****************************************Low => Buy')
              sql = "INSERT INTO intraday (cname, csymbol,type,cdate,open,high,low,close) VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"
              val = (cname, csymbol, "buy",cdate,rowData['open'],rowData['dayHigh'],rowData['dayLow'],rowData['closePrice'])
              mycursor.execute(sql, val)
              conn.commit()
        else:
            print(name+"##############")
    except TypeError as e:
        print(e)
        print("handled successfully")       

    

# Closing the connection

conn.close()

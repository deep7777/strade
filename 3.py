from nsepython import *

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

sql = 'SELECT cname,csymbol,id,options from companies order by id asc limit 500,750'

# Executing the query

cursor.execute(sql)


# Fetching 1st row from the table

result = cursor.fetchall()

def nse_custom_function_secfno(symbol,options,attribute="lastPrice"):
    positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
    endp = len(positions['data'])
    option = ''
    if(options == 1):
        option = 'derivative'

    for x in range(0, endp):
        if(positions['data'][x]['symbol']==symbol.upper()):
            #print(positions['data'][x])
            data = positions['data'][x]
            ropen = data['open']
            rhigh = data['dayHigh']
            rlow = data['dayLow']
            if(ropen == rhigh):
                str =  'Sell '+' '+symbol+' '+option+' '+data['open']+' '+data['dayHigh']+' '+data['lastPrice']
                print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<",symbol,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                return str
            elif(ropen == rlow):
                str =  'Buy'+' '+symbol+' '+option+' '+data['open']+' '+data['dayLow']+' '+data['lastPrice']
                print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",symbol,"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
                return str
            else:
                return ''

arr = []
for row in result:
    name = row[1]
    company = row[0]
    options = row[3]
    getData = nse_custom_function_secfno(name,options)
    if(getData!='' and getData!=None):
        arr.append(getData)

arr.sort()
for row in arr:
    print(row)



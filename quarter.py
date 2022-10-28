from nsepython import *
from datetime import datetime
from sqlalchemy import create_engine

import yfinance as yf
import plotly.graph_objs as go
import yfinance as yf
import mysql.connector
import numpy as np
import pandas as pd
import array
import matplotlib.pyplot as plot
import requests


# establishing the connection

conn = mysql.connector.connect(user='root', password='root',
                               host='127.0.0.1', database='deepak')

# Creating a cursor object using the cursor() method

cursor = conn.cursor()


#https://www.shellhacks.com/telegram-api-send-message-personal-notification-bot/
#https://api.telegram.org/bot5624906546:AAHrfJwHVcNgJjwCltjYm9YR2qlxUWUCJIA/getUpdates
url = 'https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O'
print(url)
positions = nsefetch(url)
arr = []
cnames = []
prices = []
dateval = datetime.today().strftime('%Y-%m-%d')


def plotGraph():
    my_conn = create_engine("mysql+mysqldb://root:root@localhost/deepak")
    query="SELECT concat(cname,'  ',price) as cname,price FROM intraday"    
    df = pd.read_sql(query,my_conn)
    print(df)
    df.plot.barh(x="cname", y="price")
    plot.show()


def quarter_diff(symbol):
    print(symbol)
    quarters = {'2022-01-01':'2022-03-31', '2022-04-01':'2022-06-30','2022-07-01':'2022-09-30','2022-10-01':'2022-12-31'} 
    for start, end in quarters.items():
        #print(start,end)
        sql = "select max(high) as high,min(low) as low,round(max(high)-min(low)) as diff from stockdata where symbol='"+symbol+"' and dateval>='"+start+"' and dateval<='"+end+"'"
        # Executing the query
        cursor.execute(sql)
        # Fetching 1st row from the table
        result = cursor.fetchall()
        for row in result:
            print(symbol,start,end,row[0],row[1],row[2])
            insertData(symbol,start,end,row[0],row[1],row[2])
        

def insertData(symbol,start,end,high,low,diff):
    insert_stmt = (
       "INSERT INTO quarter(csymbol,high,low,diff,qstart,qend)"
       "VALUES (%s, %s, %s, %s,%s,%s)"
    )
    data = (symbol,high,low,diff,start,end)
    cursor.execute(insert_stmt, data)
    conn.commit()
   
def send_to_telegram(message):
    apiToken = '5624906546:AAHrfJwHVcNgJjwCltjYm9YR2qlxUWUCJIA'
    chatID = '@stockalerts5'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message,'parse_mode':'HTML'})
        #print(response.text)
    except Exception as e:
        print(e)

def updatepoints():
    qry = 'update intraday o set o.points = (select movement from companies where csymbol=o.cname)'
    cursor.execute(qry)
    conn.commit()

def stockalerts():
    sql = """SELECT DISTINCT(name),cname,otype,price,derivative,volume,points FROM intraday WHERE dateval = '%s' order by otype asc,volume desc""" % (dateval)
    # Executing the query
    cursor.execute(sql)
    # Fetching 1st row from the table
    result = cursor.fetchall()
    for row in result:
      name = row[0]
      cname= row[1]
      otype= row[2]
      price= row[3]
      derivative= row[4]
      volume = row[5]
      points = row[6]
      msg =  otype+' '+cname+' <b>with sl=</b> '+str(price)+' traded volume  '+str(volume)+' movement '+str(points)
      print(msg)
      send_to_telegram(msg)

# Retrieving single row


sql = "SELECT cname,csymbol,options from companies where options='1' order by id asc"
# Executing the query
cursor.execute(sql)
# Fetching 1st row from the table
result = cursor.fetchall()
for row in result:
    company = row[0]
    name = row[1]
    quarter_diff(name)


        

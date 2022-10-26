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

positions = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
arr = []
cnames = []
prices = []
dateval = datetime.today().strftime('%Y-%m-%d')


def plotGraph():
    my_conn = create_engine("mysql+mysqldb://root:root@localhost/deepak")
    query="SELECT concat(cname,'  ',price) as cname,price FROM options"    
    df = pd.read_sql(query,my_conn)
    print(df)
    df.plot.barh(x="cname", y="price")
    plot.show()


def nse_custom_function_secfno(symbol,type):
    endp = len(positions['data'])

    for x in range(0, endp):
        if(positions['data'][x]['symbol']==symbol.upper()):
            data = positions['data'][x]
            print(data)
            ropen = data['open']
            rhigh = data['dayHigh']
            rlow = data['dayLow']
            volume = data['totalTradedVolume']
            close = data['lastPrice']
            status = 'failure'
            if(type=="Sell"):
            	if(rhigh > close):
            		status = 'success'
            elif(type=="Buy"):
            	if(rlow < close):
            		status = 'success'
            updateclose(symbol,data['lastPrice'],status)
            


   
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
    qry = 'update options o set o.points = (select movement from companies where csymbol=o.cname)'
    cursor.execute(qry)
    conn.commit()

def updateclose(csymbol,close,status):
    qry = "update options o set o.close = "+close+" where o.cname='"+csymbol+"' and o.dateval='"+dateval+"'"
    qry1 = "update options o set o.status = '"+status+"' where o.cname='"+csymbol+"' and o.dateval='"+dateval+"'"
    print(qry)
    cursor.execute(qry)
    cursor.execute(qry1)
    conn.commit()
    print(qry)
    cursor.execute(qry)
    conn.commit()

def stockalerts():
    sql = """SELECT DISTINCT(name),cname,otype,price,derivative,volume,points FROM options WHERE dateval = '%s' order by otype asc,volume desc""" % (dateval)
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


sql = "SELECT cname,otype from options where dateval='"+dateval+"'"
print(sql)
# Executing the query
cursor.execute(sql)
# Fetching 1st row from the table
result = cursor.fetchall()
for row in result:
    symbol = row[0]
    otype = row[1]
    nse_custom_function_secfno(symbol,otype)
        

# {
#     'symbol': 'RBLBANK',
#     'identifier': '',
#     'series': 'EQ',
#     'open': '129.45',
#     'dayHigh': '134.4',
#     'dayLow': '129',
#     'lastPrice': '132.9',
#     'previousClose': '128.8',
#     'change': 4.1,
#     'pChange': 3.18,
#     'totalTradedVolume': 23246984,
#     'totalTradedValue': 3077900681.6,
#     'lastUpdateTime': '13-SEP-2022',
#     'yearHigh': '221.3',
#     'yearLow': '74.15',
#     'nearWKH': 39.945774966109354,
#     'nearWKL': -79.23128792987187,
#     'perChange365d': -33.71,
#     'date365dAgo': '14-Oct-2021',
#     'chart365dPath': 'https://static.nseindia.com/sparklines/365d/RBLBANK-EQ.jpg',
#     'date30dAgo': '16-Sep-2022',
#     'perChange30d': 2.17,
#     'chart30dPath': 'https://static.nseindia.com/sparklines/30d/RBLBANK-EQ.jpg',
#     'chartTodayPath': 'https://static.nseindia.com/sparklines/today/RBLBANKEQN.jpg',
#     'meta': {
#         'symbol': 'RBLBANK',
#         'companyName': 'RBL Bank Limited',
#         'activeSeries': ['EQ'],
#         'debtSeries': [],
#         'tempSuspendedSeries': [],
#         'isFNOSec': True,
#         'isCASec': False,
#         'isSLBSec': True,
#         'isDebtSec': False,
#         'isSuspended': False,
#         'isETFSec': False,
#         'isDelisted': False,
#         'isin': 'INE976G01028'
#     }
# }


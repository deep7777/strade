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


def nse_custom_function_secfno(symbol,options,attribute="lastPrice"):
    endp = len(positions['data'])
    option = '0'
    if(options == 1):
        option = '1'

    for x in range(0, endp):
        if(positions['data'][x]['symbol']==symbol.upper()):
            data = positions['data'][x]
            ropen = data['open']
            rhigh = data['dayHigh']
            rlow = data['dayLow']
            volume = data['totalTradedVolume']
            if(ropen == rhigh):
                str =  'Sell '+' '+symbol+' '+option+' '+data['open']+' '+data['dayHigh']+' '+data['lastPrice']
                cnames.append(symbol)
                prices.append(data['open'])
                insertData(str,'Sell',symbol,data['open'],option,volume)
                return str
            elif(ropen == rlow):
                str =  'Buy'+' '+symbol+' '+option+' '+data['open']+' '+data['dayLow']+' '+data['lastPrice']
                cnames.append(symbol)
                prices.append(data['open'])
                insertData(str,'Buy',symbol,data['open'],option,volume)
                return str
            else:
                return ''

def insertData(getData,otype,cname,price,option,volume):
    insert_stmt = (
       "INSERT INTO options(name, dateval, otype,cname,price,derivative,volume)"
       "VALUES (%s, %s, %s, %s,%s,%s,%s)"
    )
    data = (getData,dateval,otype,cname,price,option,volume)
    cursor.execute(insert_stmt, data)
    #conn.commit()
   
def send_to_telegram(message):
    apiToken = '5624906546:AAHrfJwHVcNgJjwCltjYm9YR2qlxUWUCJIA'
    chatID = '@stockalerts5'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message,'parse_mode':'HTML'})
        #print(response.text)
    except Exception as e:
        print(e)

def stockalerts():
    sql = """SELECT DISTINCT(name),cname,otype,price,derivative,volume FROM options WHERE dateval = '%s' order by otype asc,volume desc""" % (dateval)
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
      msg =  otype+' '+cname+' <b>with sl=</b> '+str(price)+' traded volume  '+str(volume)
      print(msg)
      send_to_telegram(msg)

# Retrieving single row

sql = 'SELECT cname,csymbol,options from companies order by id asc'
# Executing the query
cursor.execute(sql)
# Fetching 1st row from the table
result = cursor.fetchall()
for row in result:
    company = row[0]
    name = row[1]
    options = row[2]
    nse_custom_function_secfno(name,options)
        

stockalerts()

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


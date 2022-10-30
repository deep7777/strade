from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS

from bson import ObjectId

import pymongo
import mysql.connector

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")    
mydb = myclient["strade"]

# Settings
CORS(app)

conn = mysql.connector.connect(user='root', password='root',
                               host='127.0.0.1', database='deepak')

# Creating a cursor object using the cursor() method

cursor = conn.cursor()


def intra(result):
    intraday = []
    for row in result:
        intraday.append({
            'id': row[0],
            'name': row[1],
            'cname': row[2],
            'otype': row[3],
            'price': row[4],
            'derivative': row[5],
            'dateval': row[6],
            'volume': row[7],
            'points': row[8],
            'close': row[9],
            'status': row[10],
        })
    return intraday  

def kbs(result):
    kb = []
    for row in result:
        print(row)
        kb.append({
            'id': row[0],
            'dateval': row[1],
            'symbol': row[2],
            'series': row[3],
            'prevclose': row[4],
            'open': row[5],
            'high': row[6],
            'low': row[7],
            'last': row[8],
            'close': row[9],
            'vwap': row[10],
        })
    return kb  
      
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/companies")
def getCompanies():
    companies = []
    mydb = myclient["strade"]
    mycol = mydb["companies"]
    mydoc = mycol.find()
    for doc in mydoc:
        print(ObjectId(doc['_id']))
        companies.append({
            '_id': str(ObjectId(doc['_id'])),
            'symbol': doc['symbol'],
            'cname': doc['cname'],
            'mcap': doc['mcap']
        })
    print(companies)    
    return companies

@app.route("/intraday")
def allintraday():
    sql = "select id,name,cname,otype,price,derivative, date_format(dateval, '%d-%m-%Y') as dateval,volume,points,close,status from intraday order by dateval desc"
    cursor.execute(sql)
    result = cursor.fetchall()
    return intra(result)
    

@app.route("/intraday/<dateval>")
def intraday(dateval=None):
    sql = "select id,name,cname,otype,price,derivative,dateval,volume,points,close,status from intraday where dateval='"+dateval+"'"
    cursor.execute(sql)
    result = cursor.fetchall()
    return intra(result)

@app.route("/kb")
def kb():
    sql = "select id, dateval, symbol, series, prevclose, open, high, low, last, close, vwap, volume, turnover, trades, deliverablevolume, deliverable from stockdata where dvlen!=(select len from companies where csymbol=symbol) and dateval>='2022-10-21'"
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall() 
    return kbs(result)



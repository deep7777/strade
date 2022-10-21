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

sql = 'SELECT cname,csymbol from companies where options=1'

# Executing the query

cursor.execute(sql)

# Fetching 1st row from the table

result = cursor.fetchone()
print(result)

# Fetching 1st row from the table

result = cursor.fetchall()
print(result)

file1 = open('5min.csv', 'w')
for row in result:
    print(row[1])
    name = row[1]
    data = yf.download(row[1] + '.NS', start = "2022-09-26" , end = "2022-09-30",period='1d', interval='1h')
    df = pd.DataFrame(data)
    file1.write("\n")
    file1.write(row[1])
    file1.write("\n")
    file1.write(df.to_string())
    file1.write("\n")

    for index, row in df.iterrows():
        rows = name,' ',index,' ',row.Volume, row.Open
        print(rows)

# Closing the connection

file1.close()
conn.close()


# import pandas lib as pd
import pandas as pd
import pymongo
import db
import numpy
myclient = db.getclient()
mydb = myclient["strade"]
mycol = mydb["companies"]

# read by default 1st sheet of an excel file
df = pd.read_excel('MCAP31032022.xlsx')
pd.DataFrame(df)
mylist = []

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def insertData(mylist):
	x = mycol.insert_many(mylist)
	print(x.inserted_ids)

for index, row in df.iterrows():
	if(row[3]):
		mylist.append({ "symbol": row[1], "cname": row[2],'mcap':row[3]})
					
insertData(mylist)
	
	
  

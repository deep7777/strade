import pymongo
import db

myclient = db.getclient()
mydb = myclient["strade"]
mycol = mydb["companies"]
print(mydb.list_collection_names())

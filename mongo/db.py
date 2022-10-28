import pymongo

def getclient():
	return pymongo.MongoClient("mongodb://localhost:27017/")	
	
def getdb():
	myclient = getclient()
	mydb = myclient["strade"]
	return mydb


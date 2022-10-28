import db
myclient = db.getclient()
mydb = myclient["strade"]
print(mydb)
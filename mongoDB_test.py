import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.fort_knox
col = db.banks

the_query = {'gold_cnt':  {$gt:5,$lt:10}}
mydoc = col.find(the_query)

total = 0;
for i in mydoc:
	total = total + 1

print(total)

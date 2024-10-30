from flask import Flask
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

clientMongo = MongoClient("mongodb://mongo:27017/")
database = clientMongo.testDB
collection = database.requestsMg


@app.route('/')
def index():
    collection.insert_one({"timestamp": datetime.now()})
    total = collection.count_documents({})
    return f'Total requests: {total}'


@app.route('/show')
def allRequests():
    reqList = []
    temp = collection.find({})
    for item in temp:
        reqList.append(str(item)+'<br>')
    return listForResponse(reqList)


@app.route('/clear')
def doClear():
    collection.delete_many({})
    total = collection.count_documents({})
    return f'All clear, boss! <br>Reset all requests. Current number of requests is: {total}'


def listForResponse(targetList):
    s = ""
    for item in targetList:
        s += str(item) + '\n'
    return s

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

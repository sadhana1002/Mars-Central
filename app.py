import missiontomars
import pymongo
from flask import Flask, jsonify, render_template

client = pymongo.MongoClient()
db = client.marsdb
collection = db.marsdb.marscollection


app = Flask(__name__)

@app.route("/")
def home():
    data = list(collection.find({}).sort("date", pymongo.DESCENDING).limit(1))
    latest_data = data[0]
    return render_template('index.html',mars=latest_data)


@app.route("/scrape")
def scrape():
    
    scraped_data = missiontomars.scrape()
    collection.insert_one(scraped_data)
    data = collection.find_one({})
    print(data)
    return render_template('index.html',mars=scraped_data)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
# use flask pymongo to set up connection to db
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    #access info from db
    mars_data = mongo.db.marsData.find_one()
    #print(mars_data)
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
    #reference db collection
    marsTable = mongo.db.marsData

    # drop table if exists
    mongo.db.marsData.drop()

    #call scrape mars script
    mars_data = scrape_mars.scrape_all()

    #take dictionary and load into mongoDB
    marsTable.insert_one(mars_data)
    
    #go back to index route
    return redirect("/")

if __name__ == "__main__":
    app.run()


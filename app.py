# Import modules
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# create flask app

app = Flask(__name__)

# connect to mongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# set a route to querry Mongo and pass to HTML
@app.route("/")
def home():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars =mars)

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_featured_image()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_hemisphere()

    mongo.db.collection.update({}, mars_data, upsert=True)

    return redirect("/", code= 302)

if __name__ == "__main__":
    app.run(debug=True)

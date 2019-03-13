import os
from flask import Flask, render_template, url_for, redirect, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'cookbook_trisport'
app.config["MONGO_URI"] = 'mongodb://<dbuser>:<dbpassword>@ds159185.mlab.com:59185/cookbook_trisport'


mongo = PyMongo(app)




@app.route('/')
@app.route('/nutrition')
def nutrition():
    return render_template('index.html',
                          recipes = mongo.db.recipes.find())
                          
@app.route('/get_recipes') 
def get_recipes():
    return render_template('recipes.html',
                           recipes = mongo.db.recipes.find())
    
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
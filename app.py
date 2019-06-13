import pymongo 
import os
from flask import Flask, render_template, url_for, redirect, session, request, flash, jsonify
import json
import pymongo
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson import json_util
from bson.json_util import dumps


app = Flask(__name__)

recipe_schema_id = "5c9bbf7ee7179a0e408e3177"
form_schema_id = ""


app.secret_key = "mir_tri"

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = os.getenv('MONGO_DB_NAME','cookbook_trisport')
MONGO_URI = os.getenv('MONGODB_URI')
app.config["MONGO_DBNAME"] = 'cookbook_trisport'
app.config["MONGO_URI"] = 'mongodb://mirof:Vanilia123@ds159185.mlab.com:59185/cookbook_trisport'
COLLECTION_NAME = 'recipes'
FIELDS = {'meal_type': True, 'sport_type': True, 'race_day': True, 'vegan_meal': True, '_id': False}


mongo = PyMongo(app)             #constructor method

# Collections

users_collections = mongo.db.users
recipes_collection = mongo.db.recipes
forms_collection = mongo.db.forms


 



@app.route('/')
@app.route('/get_ready')
def get_ready():
    return render_template('getready.html', recipes=mongo.db.recipes.find()) #supply recipes collection
                          
                          
@app.route('/get_recipes', methods=['GET']) # images for my recepies and see all my recipes after adding them
def get_recipes():
    return render_template('recipes.html', recipes=mongo.db.recipes.find())
    

    
@app.route('/find_recipes')
def find_recipes_json():
    recipes = mongo.db.recipes.find()
    json_recipes = []
    for recipe in recipes:
        json_recipes.append(recipe)
    json_recipes = json.dumps(json_recipes, default=json_util.default)
    return json_recipes
    
    
    
@app.route('/recipedescription/<recipe_id>')
def recipedescription(recipe_id):
    this_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    return render_template('recipedescription.html', recipe=this_recipe)
                          

@app.route('/add_recipe')  #only for display my recipes in my form
def add_recipe():
    
# {
#    "_id": {
#       "$oid": "5c9bbf7ee7179a0e408e3177"
#    },
#    "author_name": "",
#    "recipe_name": "",
#    "meal_type_name": "",
#    "sport_type_name": "",
#    "race_day_name": "",
#    "description": "",
#    "image_recipe": "",
#    "vegan_type_meal": "",
#    "due_date": ""
#}   
    if request.url.startswith('http://'):
        request.url = request.url.replace('http://', 'https://', 1)
    print('url when add_recipe: ', request.url)

    return render_template('add_recipe.html',
                          recipe={},
                          author_name=mongo.db.author_name.find(),
                          meal_type=mongo.db.meal_type.find(),
                          sport_type=mongo.db.sport_type.find(),
                          race_day=mongo.db.race_day.find(),
                          vegan_meal=mongo.db.vegan_meal.find(),
                          recipes=mongo.db.recipes.find()
                          )
                          
                          
    
                          
                          
@app.route('/edit_recipe/<recipe_id>')    #edit_recipe to my database
def insert_my_recipe(recipe_id):
    this_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('edit_recipe.html', recipe=this_recipe)
    



@app.route('/submit_to_database', methods=['POST'])
def submit_to_database():
    print(request.form.to_dict())
    recipes=mongo.db.recipes
    recipes.insert_one(request.form.to_dict())     #or (request.json)
    return redirect(url_for('get_recipes'))
                                                    #return('', 204) # what is 204
    
                          
                          
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    logged_in = False
    if request.method == 'GET' and not 'username' in session:
        return render_template('login.html', logged_in=logged_in)
    elif request.method == 'GET' and 'username' in session:
        logged_in = True
        recipes = mongo.db.recipes.find()
        
        recipes_dics = {}
        
        for i, recipe in enumerate(recipes):
            recipe.pop('_id', None)
            recipes_dics[i] = recipe
            
        recipes_dics = json.dumps(recipes_dics)
        
        return render_template('login.html', 
                               username=session['username'],
                               logged_in=logged_in,
                               recipes=recipes_dics)
    if request.method == 'POST':
        session['username'] = request.form["username"]
        logged_in = True
        recipes=mongo.db.recipes.find()
        recipes_dics = {}
        
        for i, recipe in enumerate(recipes):
            recipe.pop('_id', None)
            recipes_dics[i] = recipe
            
        recipes_dics = json.dumps(recipes_dics)
            
        return render_template('login.html',
                              username=session['username'],
                              logged_in=logged_in,
                              recipes=recipes_dics)   
                              
@app.route('/log_out')
def log_out():
    print('logged out')
    session.clear()
    return redirect(url_for('get_ready'))
        
        
    
    
@app.route('/search_form', methods=['GET', 'POST'])      #render template
def search_form():
    forms = forms_collection.find()
    
    return render_template('search_form.html')
    
        






@app.route('/my_recipes', methods=['GET', 'POST'])
def my_recipes():
    if not 'username' in session:
        return redirect('/log_in')
    else:
        recipes = mongo.db.recipes.find()
        return render_template('my_recipes.html',
                           username=session['username'],
                           recipes=recipes)  
                           
                           
@app.route('/dashboard')
def dashboard():
    forms = forms_collection.find()
    
    return render_template('dashboard.html')
    



@app.route('/contact_us')
def contact_us():
    return render_template("contactus.html")
                          
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
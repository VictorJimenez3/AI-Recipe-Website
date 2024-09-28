from flask import Flask, app, redirect, render_template, request
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json

app = Flask(__name__)

# MongoDB setup

uri = "mongodb+srv://vmj:RuEIzEBBBpqoWj13@cluster0.eulfz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
users_collection = client['users']

@app.route('/')
def index():
    # Render the form template
    return render_template('templates/index.html')

if __name__ == '__main__':
    app.run(debug=True)

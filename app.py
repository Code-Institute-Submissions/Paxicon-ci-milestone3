import os
from flask import Flask, render_template, redirect, request, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5000,
            debug=True)

from re import I
from sys import audit
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy  import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!' #will be different on the hosted version
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from studyforums import routes
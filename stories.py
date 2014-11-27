import os
from settings import db_config
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(db_config)
db = SQLAlchemy(app)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    author = db.Column(db.String(100))
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    body = db.Column(db.Text)



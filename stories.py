import os, sys, datetime
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
    story = db.relationship('Story', db.backref('comments', lazy='dynamic'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stories/')
def show_stories():
    stories = Story.query.all()
    return render_template('articles.html',stories=stories)

@app.route('/stories/<story_id>')
def show_story(story_id):
    story_list = Story.query.filter_by(id=story_id)
    if story_list.length > 0:
        return render_template('article.html',story=story_list.first())
    else:
        return error_404()

@app.route('/add_story/', methods=['GET','POST'])
def add_story():
    if request.method == 'POST':
        story = Story()
        story.title = request.form['title']
        story.body = request.form['body']
        story.author = request.form['author']
        story.pub_date = datetime.datetime.now()
        db.session.add(story)
        db.commit()
        return render_template('story_added.html')
    else:
        return render_template('add_story.html')

def error_404():
    return render_template('404.html')

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'initdb':
        db.create_all()
    else:
        app.run()


import os, sys, datetime
from settings import db_config
from flask import Flask, request, session, g, redirect, url_for, abort
from flask import render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(db_config)
db = SQLAlchemy(app)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='story', lazy='dynamic')
    score = db.Column(db.Integer, default=0)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', lazy='dynamic')
    body = db.Column(db.Text)
    score = db.Column(db.Integer, default=0)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Integer)
    name = db.Column(db.String(100))
    stories = db.relationship('Story', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    upvotes = db.relationship('Upvote', backref='author', lazy='dynamic')

class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/')
def home():
    return render_template('index.html', stories=Story.query.all())

@app.route('/stories/')
def show_stories():
    stories = Story.query.all()
    return render_template('stories.html',stories=stories)

@app.route('/stories/<story_id>/')
def show_story(story_id):
    story_list = Story.query.filter_by(id=story_id)
    if story_list.count() > 0:
        return render_template('story.html',story=story_list.first())
    else:
        return error_404()

@app.route('/stories/<story_id>/comment/', methods=['POST'])
def comment_story(story_id):
    username = request.form['author']
    user_list = User.query.filter_by(name=username)

    story_list = Story.query.filter_by(id=story_id)
    if story_list.count() > 0:
        comment = Comment()
        comment.body = request.form['body']
        comment.story = story_list.first()
        if user_list.count() > 0:
            comment.author = user_list.first()
        else:
            user = User()
            user.name = username
            db.session.add(user)
            comment.author = user

        if request.form['reply_comment'].isdigit():
            comment_id = int(request.form['reply_comment'])
            comment_list = Comment.query.filter_by(id=comment_id)
            if comment_list.count() > 0:
                comment.comment_id = comment_list.first().id
                comment.story = None

        db.session.add(comment)
        db.session.commit()

        return show_story(story_id)
    else:
        return error_404()

@app.route('/stories/<story_id>/upvote/', methods=['POST'])
def upvote_story(story_id):
    upvote = Upvote()
    
    username = request.form['author']
    user = User.query.filter_by(name=username).first()
    if user is not None:
        upvote.author = user
    else:
        return error_404()
    
    if 'comment' in request.form and request.form['comment'].isdigit():
        comment = Comment.query.filter_by(id=int(request.form['comment'])).first()
        if comment is not None:
            upvote.comment_id = comment.id
        else:
            return error_404()
    else:
        story = Story.query.filter_by(id=story_id).first()
        if story is not None:
            upvote.story_id = story.id
        else:
            return error_404()
    
    if Upvote.query.filter_by(comment_id=upvote.comment_id, story_id=upvote.story_id, user_id=user.id).count() > 1:
        del upvote
        return show_story(story_id)
    else:
        #increment the score of the associated comment/story
        if upvote.story_id is not None:
            story = Story.query.filter_by(id=upvote.story_id).first()
            story.score += 1
        elif upvote.comment_id is not None:
            comment = Comment.query.filter_by(id=upvote.comment_id).first()
            comment.score += 1

        db.session.add(upvote)
        db.session.commit()
        return show_story(story_id)

@app.route('/add_story/', methods=['GET','POST'])
def add_story():
    # add a story to the database
    if request.method == 'POST':
        # create a new story
        story = Story()
        story.title = request.form['title']
        story.body = request.form['body']
        story.pub_date = datetime.datetime.now()
        user_list = User.query.filter_by(name=request.form['author'])

        # find the author by name.
        if user_list.count() > 0:
            story.author = user_list.first()

        #if the author does not exist, create a new one
        else:
            author = User()
            author.name = request.form['author']
            db.session.add(author)
            story.author = author

        db.session.add(story)
        db.session.commit()
        return render_template('story_added.html')

    # ask the user to create a story if the request is not a POST request
    else:
        return render_template('add_story.html')

@app.route('/users/<username>/')
def show_user(username):
    user_list = User.query.filter_by(name=username)
    if user_list.count() == 0:
        return error_404()
    else:
        return render_template('user.html', user = user_list.first())

def error_404():
    return render_template('404.html')

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'initdb':
        db.create_all()
    else:
        app.run()


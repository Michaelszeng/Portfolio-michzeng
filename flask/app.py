"""
Use Powershell Terminal.

ACTIVATE VIRTUALENV:
>.\env\Scripts\activate

RUN SERVER:
>flask run
"""

import os
from datetime import datetime

from flask import Flask, render_template, send_from_directory, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__, static_url_path='', static_folder='client/public')
load_dotenv()   # this library helps load in the settings in .flaskenv

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
db = SQLAlchemy(app)

CORS(app)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(3200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id




@app.route("/", methods=['GET'])
def index():
    return {"JSON": ["1", "2", "3"]}

@app.route("/project/<project_name>", methods=['GET', 'POST'])
def project(project_name):
    if request.method == 'POST':    #Need to use POST request if retreiving new content from html
        content = request.form['new_content']
        email = request.form['new_email']
        new_task = Comment(content=content, email=email)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/project/' + project_name)
        except:
            return 'The website did an oopsie. Failed to post comment.'

@app.route("/delete/<int:comment_id>", methods=['GET'])
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get_or_404(comment_id)  #Get task by id (or 404 if not found)
    try:
        db.session.delete(comment_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "The website did an oopsie. Failed to delete comment."

@app.route("/test")
def test():
    return {"JSON": ["1", "2"]}